# ext/declarative/base.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php
"""Internal implementation for declarative."""
from __future__ import absolute_import

import collections
import weakref

from sqlalchemy.orm import attributes
from sqlalchemy.orm import instrumentation
from . import clsregistry
from . import exc as orm_exc
from . import mapper as mapperlib
from .attributes import InstrumentedAttribute
from .attributes import QueryableAttribute
from .base import _is_mapped_class
from .base import InspectionAttr
from .descriptor_props import CompositeProperty
from .descriptor_props import SynonymProperty
from .interfaces import MapperProperty
from .mapper import Mapper as mapper
from .properties import ColumnProperty
from .util import class_mapper
from .. import event
from .. import exc
from .. import util
from ..sql import expression
from ..sql.schema import Column
from ..sql.schema import Table
from ..util import topological


def _declared_mapping_info(cls):
    # deferred mapping
    if _DeferredMapperConfig.has_cls(cls):
        return _DeferredMapperConfig.config_for_cls(cls)
    # regular mapping
    elif _is_mapped_class(cls):
        return class_mapper(cls, configure=False)
    else:
        return None


def _resolve_for_abstract_or_classical(cls):
    if cls is object:
        return None

    if cls.__dict__.get("__abstract__", False):
        for sup in cls.__bases__:
            sup = _resolve_for_abstract_or_classical(sup)
            if sup is not None:
                return sup
        else:
            return None
    else:
        clsmanager = _dive_for_cls_manager(cls)

        if clsmanager:
            return clsmanager.class_
        else:
            return cls


def _get_immediate_cls_attr(cls, attrname, strict=False):
    """return an attribute of the class that is either present directly
    on the class, e.g. not on a superclass, or is from a superclass but
    this superclass is a non-mapped mixin, that is, not a descendant of
    the declarative base and is also not classically mapped.

    This is used to detect attributes that indicate something about
    a mapped class independently from any mapped classes that it may
    inherit from.

    """

    # the rules are different for this name than others,
    # make sure we've moved it out.  transitional
    assert attrname != "__abstract__"

    if not issubclass(cls, object):
        return None

    if attrname in cls.__dict__:
        return getattr(cls, attrname)

    for base in cls.__mro__[1:]:
        _is_classicial_inherits = _dive_for_cls_manager(base)

        if attrname in base.__dict__ and (
            base is cls
            or (
                (base in cls.__bases__ if strict else True)
                and not _is_classicial_inherits
            )
        ):
            return getattr(base, attrname)
    else:
        return None


def _dive_for_cls_manager(cls):
    # because the class manager registration is pluggable,
    # we need to do the search for every class in the hierarchy,
    # rather than just a simple "cls._sa_class_manager"

    # python 2 old style class
    if not hasattr(cls, "__mro__"):
        return None

    for base in cls.__mro__:
        manager = attributes.manager_of_class(base)
        if manager:
            return manager
    return None


def _as_declarative(registry, cls, dict_):

    # declarative scans the class for attributes.  no table or mapper
    # args passed separately.

    return _MapperConfig.setup_mapping(registry, cls, dict_, None, {})


def _mapper(registry, cls, table, mapper_kw):
    _ImperativeMapperConfig(registry, cls, table, mapper_kw)
    return cls.__mapper__


@util.preload_module("sqlalchemy.orm.decl_api")
def _is_declarative_props(obj):
    declared_attr = util.preloaded.orm_decl_api.declared_attr

    return isinstance(obj, (declared_attr, util.classproperty))


def _check_declared_props_nocascade(obj, name, cls):
    if _is_declarative_props(obj):
        if getattr(obj, "_cascading", False):
            util.warn(
                "@declared_attr.cascading is not supported on the %s "
                "attribute on class %s.  This attribute invokes for "
                "subclasses in any case." % (name, cls)
            )
        return True
    else:
        return False


class _MapperConfig(object):
    __slots__ = ("cls", "classname", "properties", "declared_attr_reg")

    @classmethod
    def setup_mapping(cls, registry, cls_, dict_, table, mapper_kw):
        manager = attributes.manager_of_class(cls)
        if manager and manager.class_ is cls_:
            raise exc.InvalidRequestError(
                "Class %r already has been " "instrumented declaratively" % cls
            )

        if cls_.__dict__.get("__abstract__", False):
            return

        defer_map = _get_immediate_cls_attr(
            cls_, "_sa_decl_prepare_nocascade", strict=True
        ) or hasattr(cls_, "_sa_decl_prepare")

        if defer_map:
            cfg_cls = _DeferredMapperConfig
        else:
            cfg_cls = _ClassScanMapperConfig

        return cfg_cls(registry, cls_, dict_, table, mapper_kw)

    def __init__(self, registry, cls_):
        self.cls = cls_
        self.classname = cls_.__name__
        self.properties = util.OrderedDict()
        self.declared_attr_reg = {}

        instrumentation.register_class(
            self.cls,
            finalize=False,
            registry=registry,
            declarative_scan=self,
            init_method=registry.constructor,
        )

    def set_cls_attribute(self, attrname, value):

        manager = instrumentation.manager_of_class(self.cls)
        manager.install_member(attrname, value)
        return value

    def _early_mapping(self, mapper_kw):
        self.map(mapper_kw)


class _ImperativeMapperConfig(_MapperConfig):
    __slots__ = ("dict_", "local_table", "inherits")

    def __init__(
        self,
        registry,
        cls_,
        table,
        mapper_kw,
    ):
        super(_ImperativeMapperConfig, self).__init__(registry, cls_)

        self.dict_ = {}
        self.local_table = self.set_cls_attribute("__table__", table)

        with mapperlib._CONFIGURE_MUTEX:
            clsregistry.add_class(
                self.classname, self.cls, registry._class_registry
            )

            self._setup_inheritance(mapper_kw)

            self._early_mapping(mapper_kw)

    def map(self, mapper_kw=util.EMPTY_DICT):
        mapper_cls = mapper

        return self.set_cls_attribute(
            "__mapper__",
            mapper_cls(self.cls, self.local_table, **mapper_kw),
        )

    def _setup_inheritance(self, mapper_kw):
        cls = self.cls

        inherits = mapper_kw.get("inherits", None)

        if inherits is None:
            # since we search for classical mappings now, search for
            # multiple mapped bases as well and raise an error.
            inherits_search = []
            for c in cls.__bases__:
                c = _resolve_for_abstract_or_classical(c)
                if c is None:
                    continue
                if _declared_mapping_info(
                    c
                ) is not None and not _get_immediate_cls_attr(
                    c, "_sa_decl_prepare_nocascade", strict=True
                ):
                    inherits_search.append(c)

            if inherits_search:
                if len(inherits_search) > 1:
                    raise exc.InvalidRequestError(
                        "Class %s has multiple mapped bases: %r"
                        % (cls, inherits_search)
                    )
                inherits = inherits_search[0]
        elif isinstance(inherits, mapper):
            inherits = inherits.class_

        self.inherits = inherits


class _ClassScanMapperConfig(_MapperConfig):
    __slots__ = (
        "dict_",
        "local_table",
        "persist_selectable",
        "declared_columns",
        "column_copies",
        "table_args",
        "tablename",
        "mapper_args",
        "mapper_args_fn",
        "inherits",
    )

    def __init__(
        self,
        registry,
        cls_,
        dict_,
        table,
        mapper_kw,
    ):

        super(_ClassScanMapperConfig, self).__init__(registry, cls_)

        self.dict_ = dict(dict_) if dict_ else {}
        self.persist_selectable = None
        self.declared_columns = set()
        self.column_copies = {}
        self._setup_declared_events()

        self._scan_attributes()

        with mapperlib._CONFIGURE_MUTEX:
            clsregistry.add_class(
                self.classname, self.cls, registry._class_registry
            )

            self._extract_mappable_attributes()

            self._extract_declared_columns()

            self._setup_table(table)

            self._setup_inheritance(mapper_kw)

            self._early_mapping(mapper_kw)

    def _setup_declared_events(self):
        if _get_immediate_cls_attr(self.cls, "__declare_last__"):

            @event.listens_for(mapper, "after_configured")
            def after_configured():
                self.cls.__declare_last__()

        if _get_immediate_cls_attr(self.cls, "__declare_first__"):

            @event.listens_for(mapper, "before_configured")
            def before_configured():
                self.cls.__declare_first__()

    def _cls_attr_override_checker(self, cls):
        """Produce a function that checks if a class has overridden an
        attribute, taking SQLAlchemy-enabled dataclass fields into account.

        """
        sa_dataclass_metadata_key = _get_immediate_cls_attr(
            cls, "__sa_dataclass_metadata_key__", None
        )

        if sa_dataclass_metadata_key is None:

            def attribute_is_overridden(key, obj):
                return getattr(cls, key) is not obj

        else:

            all_datacls_fields = {
                f.name: f.metadata[sa_dataclass_metadata_key]
                for f in util.dataclass_fields(cls)
                if sa_dataclass_metadata_key in f.metadata
            }
            local_datacls_fields = {
                f.name: f.metadata[sa_dataclass_metadata_key]
                for f in util.local_dataclass_fields(cls)
                if sa_dataclass_metadata_key in f.metadata
            }

            absent = object()

            def attribute_is_overridden(key, obj):
                if _is_declarative_props(obj):
                    obj = obj.fget

                # this function likely has some failure modes still if
                # someone is doing a deep mixing of the same attribute
                # name as plain Python attribute vs. dataclass field.

                ret = local_datacls_fields.get(key, absent)
                if _is_declarative_props(ret):
                    ret = ret.fget

                if ret is obj:
                    return False
                elif ret is not absent:
                    return True

                all_field = all_datacls_fields.get(key, absent)

                ret = getattr(cls, key, obj)

                if ret is obj:
                    return False

                # for dataclasses, this could be the
                # 'default' of the field.  so filter more specifically
                # for an already-mapped InstrumentedAttribute
                if ret is not absent and isinstance(
                    ret, InstrumentedAttribute
                ):
                    return True

                if all_field is obj:
                    return False
                elif all_field is not absent:
                    return True

                # can't find another attribute
                return False

        return attribute_is_overridden

    def _cls_attr_resolver(self, cls):
        """produce a function to iterate the "attributes" of a class,
        adjusting for SQLAlchemy fields embedded in dataclass fields.

        """
        sa_dataclass_metadata_key = _get_immediate_cls_attr(
            cls, "__sa_dataclass_metadata_key__", None
        )

        if sa_dataclass_metadata_key is None:

            def local_attributes_for_class():
                for name, obj in vars(cls).items():
                    yield name, obj, False

        else:
            field_names = set()

            def local_attributes_for_class():
                for field in util.local_dataclass_fields(cls):
                    if sa_dataclass_metadata_key in field.metadata:
                        field_names.add(field.name)
                        yield field.name, _as_dc_declaredattr(
                            field.metadata, sa_dataclass_metadata_key
                        ), True
                for name, obj in vars(cls).items():
                    if name not in field_names:
                        yield name, obj, False

        return local_attributes_for_class

    def _scan_attributes(self):
        cls = self.cls
        dict_ = self.dict_
        column_copies = self.column_copies
        mapper_args_fn = None
        table_args = inherited_table_args = None
        tablename = None

        attribute_is_overridden = self._cls_attr_override_checker(self.cls)

        for base in cls.__mro__:

            class_mapped = (
                base is not cls
                and _declared_mapping_info(base) is not None
                and not _get_immediate_cls_attr(
                    base, "_sa_decl_prepare_nocascade", strict=True
                )
            )

            local_attributes_for_class = self._cls_attr_resolver(base)

            if not class_mapped and base is not cls:
                self._produce_column_copies(
                    local_attributes_for_class, attribute_is_overridden
                )

            for name, obj, is_dataclass in local_attributes_for_class():
                if name == "__mapper_args__":
                    check_decl = _check_declared_props_nocascade(
                        obj, name, cls
                    )
                    if not mapper_args_fn and (not class_mapped or check_decl):
                        # don't even invoke __mapper_args__ until
                        # after we've determined everything about the
                        # mapped table.
                        # make a copy of it so a class-level dictionary
                        # is not overwritten when we update column-based
                        # arguments.
                        def mapper_args_fn():
                            return dict(cls.__mapper_args__)

                elif name == "__tablename__":
                    check_decl = _check_declared_props_nocascade(
                        obj, name, cls
                    )
                    if not tablename and (not class_mapped or check_decl):
                        tablename = cls.__tablename__
                elif name == "__table_args__":
                    check_decl = _check_declared_props_nocascade(
                        obj, name, cls
                    )
                    if not table_args and (not class_mapped or check_decl):
                        table_args = cls.__table_args__
                        if not isinstance(
                            table_args, (tuple, dict, type(None))
                        ):
                            raise exc.ArgumentError(
                                "__table_args__ value must be a tuple, "
                                "dict, or None"
                            )
                        if base is not cls:
                            inherited_table_args = True
                elif class_mapped:
                    if _is_declarative_props(obj):
                        util.warn(
                            "Regular (i.e. not __special__) "
                            "attribute '%s.%s' uses @declared_attr, "
                            "but owning class %s is mapped - "
                            "not applying to subclass %s."
                            % (base.__name__, name, base, cls)
                        )
                    continue
                elif base is not cls:
                    # we're a mixin, abstract base, or something that is
                    # acting like that for now.
                    if isinstance(obj, Column):
                        # already copied columns to the mapped class.
                        continue
                    elif isinstance(obj, MapperProperty):
                        raise exc.InvalidRequestError(
                            "Mapper properties (i.e. deferred,"
                            "column_property(), relationship(), etc.) must "
                            "be declared as @declared_attr callables "
                            "on declarative mixin classes.  For dataclass "
                            "field() objects, use a lambda:"
                        )
                    elif _is_declarative_props(obj):
                        if obj._cascading:
                            if name in dict_:
                                # unfortunately, while we can use the user-
                                # defined attribute here to allow a clean
                                # override, if there's another
                                # subclass below then it still tries to use
                                # this.  not sure if there is enough
                                # information here to add this as a feature
                                # later on.
                                util.warn(
                                    "Attribute '%s' on class %s cannot be "
                                    "processed due to "
                                    "@declared_attr.cascading; "
                                    "skipping" % (name, cls)
                                )
                            dict_[name] = column_copies[
                                obj
                            ] = ret = obj.__get__(obj, cls)
                            setattr(cls, name, ret)
                        else:
                            if is_dataclass:
                                # access attribute using normal class access
                                # first, to see if it's been mapped on a
                                # superclass.   note if the dataclasses.field()
                                # has "default", this value can be anything.
                                ret = getattr(cls, name, None)

                                # so, if it's anything that's not ORM
                                # mapped, assume we should invoke the
                                # declared_attr
                                if not isinstance(ret, InspectionAttr):
                                    ret = obj.fget()
                            else:
                                # access attribute using normal class access.
                                # if the declared attr already took place
                                # on a superclass that is mapped, then
                                # this is no longer a declared_attr, it will
                                # be the InstrumentedAttribute
                                ret = getattr(cls, name)

                            # correct for proxies created from hybrid_property
                            # or similar.  note there is no known case that
                            # produces nested proxies, so we are only
                            # looking one level deep right now.
                            if (
                                isinstance(ret, InspectionAttr)
                                and ret._is_internal_proxy
                                and not isinstance(
                                    ret.original_property, MapperProperty
                                )
                            ):
                                ret = ret.descriptor

                            dict_[name] = column_copies[obj] = ret
                        if (
                            isinstance(ret, (Column, MapperProperty))
                            and ret.doc is None
                        ):
                            ret.doc = obj.__doc__
                    # here, the attribute is some other kind of property that
                    # we assume is not part of the declarative mapping.
                    # however, check for some more common mistakes
                    else:
                        self._warn_for_decl_attributes(base, name, obj)
                elif is_dataclass and (
                    name not in dict_ or dict_[name] is not obj
                ):
                    # here, we are definitely looking at the target class
                    # and not a superclass.   this is currently a
                    # dataclass-only path.  if the name is only
                    # a dataclass field and isn't in local cls.__dict__,
                    # put the object there.
                    # assert that the dataclass-enabled resolver agrees
                    # with what we are seeing

                    assert not attribute_is_overridden(name, obj)

                    if _is_declarative_props(obj):
                        obj = obj.fget()

                    dict_[name] = obj

        if inherited_table_args and not tablename:
            table_args = None

        self.table_args = table_args
        self.tablename = tablename
        self.mapper_args_fn = mapper_args_fn

    def _warn_for_decl_attributes(self, cls, key, c):
        if isinstance(c, expression.ColumnClause):
            util.warn(
                "Attribute '%s' on class %s appears to be a non-schema "
                "'sqlalchemy.sql.column()' "
                "object; this won't be part of the declarative mapping"
                % (key, cls)
            )

    def _produce_column_copies(
        self, attributes_for_class, attribute_is_overridden
    ):
        cls = self.cls
        dict_ = self.dict_
        column_copies = self.column_copies
        # copy mixin columns to the mapped class

        for name, obj, is_dataclass in attributes_for_class():
            if isinstance(obj, Column):
                if attribute_is_overridden(name, obj):
                    # if column has been overridden
                    # (like by the InstrumentedAttribute of the
                    # superclass), skip
                    continue
                elif obj.foreign_keys:
                    raise exc.InvalidRequestError(
                        "Columns with foreign keys to other columns "
                        "must be declared as @declared_attr callables "
                        "on declarative mixin classes.  For dataclass "
                        "field() objects, use a lambda:."
                    )
                elif name not in dict_ and not (
                    "__table__" in dict_
                    and (obj.name or name) in dict_["__table__"].c
                ):
                    column_copies[obj] = copy_ = obj._copy()
                    copy_._creation_order = obj._creation_order
                    setattr(cls, name, copy_)
                    dict_[name] = copy_

    def _extract_mappable_attributes(self):
        cls = self.cls
        dict_ = self.dict_

        our_stuff = self.properties

        late_mapped = _get_immediate_cls_attr(
            cls, "_sa_decl_prepare_nocascade", strict=True
        )

        for k in list(dict_):

            if k in ("__table__", "__tablename__", "__mapper_args__"):
                continue

            value = dict_[k]
            if _is_declarative_props(value):
                if value._cascading:
                    util.warn(
                        "Use of @declared_attr.cascading only applies to "
                        "Declarative 'mixin' and 'abstract' classes.  "
                        "Currently, this flag is ignored on mapped class "
                        "%s" % self.cls
                    )

                value = getattr(cls, k)

            elif (
                isinstance(value, QueryableAttribute)
                and value.class_ is not cls
                and value.key != k
            ):
                # detect a QueryableAttribute that's already mapped being
                # assigned elsewhere in userland, turn into a synonym()
                value = SynonymProperty(value.key)
                setattr(cls, k, value)

            if (
                isinstance(value, tuple)
                and len(value) == 1
                and isinstance(value[0], (Column, MapperProperty))
            ):
                util.warn(
                    "Ignoring declarative-like tuple value of attribute "
                    "'%s': possibly a copy-and-paste error with a comma "
                    "accidentally placed at the end of the line?" % k
                )
                continue
            elif not isinstance(value, (Column, MapperProperty)):
                # using @declared_attr for some object that
                # isn't Column/MapperProperty; remove from the dict_
                # and place the evaluated value onto the class.
                if not k.startswith("__"):
                    dict_.pop(k)
                    self._warn_for_decl_attributes(cls, k, value)
                    if not late_mapped:
                        setattr(cls, k, value)
                continue
            # we expect to see the name 'metadata' in some valid cases;
            # however at this point we see it's assigned to something trying
            # to be mapped, so raise for that.
            elif k == "metadata":
                raise exc.InvalidRequestError(
                    "Attribute name 'metadata' is reserved "
                    "for the MetaData instance when using a "
                    "declarative base class."
                )
            our_stuff[k] = value

    def _extract_declared_columns(self):
        our_stuff = self.properties

        # set up attributes in the order they were created
        util.sort_dictionary(
            our_stuff, key=lambda key: our_stuff[key]._creation_order
        )

        # extract columns from the class dict
        declared_columns = self.declared_columns
        name_to_prop_key = collections.defaultdict(set)
        for key, c in list(our_stuff.items()):
            if isinstance(c, (ColumnProperty, CompositeProperty)):
                for col in c.columns:
                    if isinstance(col, Column) and col.table is None:
                        _undefer_column_name(key, col)
                        if not isinstance(c, CompositeProperty):
                            name_to_prop_key[col.name].add(key)
                        declared_columns.add(col)
            elif isinstance(c, Column):
                _undefer_column_name(key, c)
                name_to_prop_key[c.name].add(key)
                declared_columns.add(c)
                # if the column is the same name as the key,
                # remove it from the explicit properties dict.
                # the normal rules for assigning column-based properties
                # will take over, including precedence of columns
                # in multi-column ColumnProperties.
                if key == c.key:
                    del our_stuff[key]

        for name, keys in name_to_prop_key.items():
            if len(keys) > 1:
                util.warn(
                    "On class %r, Column object %r named "
                    "directly multiple times, "
                    "only one will be used: %s. "
                    "Consider using orm.synonym instead"
                    % (self.classname, name, (", ".join(sorted(keys))))
                )

    def _setup_table(self, table=None):
        cls = self.cls
        tablename = self.tablename
        table_args = self.table_args
        dict_ = self.dict_
        declared_columns = self.declared_columns

        manager = attributes.manager_of_class(cls)

        declared_columns = self.declared_columns = sorted(
            declared_columns, key=lambda c: c._creation_order
        )

        if "__table__" not in dict_ and table is None:
            if hasattr(cls, "__table_cls__"):
                table_cls = util.unbound_method_to_callable(cls.__table_cls__)
            else:
                table_cls = Table

            if tablename is not None:

                args, table_kw = (), {}
                if table_args:
                    if isinstance(table_args, dict):
                        table_kw = table_args
                    elif isinstance(table_args, tuple):
                        if isinstance(table_args[-1], dict):
                            args, table_kw = table_args[0:-1], table_args[-1]
                        else:
                            args = table_args

                autoload_with = dict_.get("__autoload_with__")
                if autoload_with:
                    table_kw["autoload_with"] = autoload_with

                autoload = dict_.get("__autoload__")
                if autoload:
                    table_kw["autoload"] = True

                table = self.set_cls_attribute(
                    "__table__",
                    table_cls(
                        tablename,
                        self._metadata_for_cls(manager),
                        *(tuple(declared_columns) + tuple(args)),
                        **table_kw
                    ),
                )
        else:
            if table is None:
                table = cls.__table__
            if declared_columns:
                for c in declared_columns:
                    if not table.c.contains_column(c):
                        raise exc.ArgumentError(
                            "Can't add additional column %r when "
                            "specifying __table__" % c.key
                        )
        self.local_table = table

    def _metadata_for_cls(self, manager):
        if hasattr(self.cls, "metadata"):
            return self.cls.metadata
        else:
            return manager.registry.metadata

    def _setup_inheritance(self, mapper_kw):
        table = self.local_table
        cls = self.cls
        table_args = self.table_args
        declared_columns = self.declared_columns

        inherits = mapper_kw.get("inherits", None)

        if inherits is None:
            # since we search for classical mappings now, search for
            # multiple mapped bases as well and raise an error.
            inherits_search = []
            for c in cls.__bases__:
                c = _resolve_for_abstract_or_classical(c)
                if c is None:
                    continue
                if _declared_mapping_info(
                    c
                ) is not None and not _get_immediate_cls_attr(
                    c, "_sa_decl_prepare_nocascade", strict=True
                ):
                    if c not in inherits_search:
                        inherits_search.append(c)

            if inherits_search:
                if len(inherits_search) > 1:
                    raise exc.InvalidRequestError(
                        "Class %s has multiple mapped bases: %r"
                        % (cls, inherits_search)
                    )
                inherits = inherits_search[0]
        elif isinstance(inherits, mapper):
            inherits = inherits.class_

        self.inherits = inherits

        if (
            table is None
            and self.inherits is None
            and not _get_immediate_cls_attr(cls, "__no_table__")
        ):

            raise exc.InvalidRequestError(
                "Class %r does not have a __table__ or __tablename__ "
                "specified and does not inherit from an existing "
                "table-mapped class." % cls
            )
        elif self.inherits:
            inherited_mapper = _declared_mapping_info(self.inherits)
            inherited_table = inherited_mapper.local_table
            inherited_persist_selectable = inherited_mapper.persist_selectable

            if table is None:
                # single table inheritance.
                # ensure no table args
                if table_args:
                    raise exc.ArgumentError(
                        "Can't place __table_args__ on an inherited class "
                        "with no table."
                    )
                # add any columns declared here to the inherited table.
                for c in declared_columns:
                    if c.name in inherited_table.c:
                        if inherited_table.c[c.name] is c:
                            continue
                        raise exc.ArgumentError(
                            "Column '%s' on class %s conflicts with "
                            "existing column '%s'"
                            % (c, cls, inherited_table.c[c.name])
                        )
                    if c.primary_key:
                        raise exc.ArgumentError(
                            "Can't place primary key columns on an inherited "
                            "class with no table."
                        )
                    inherited_table.append_column(c)
                    if (
                        inherited_persist_selectable is not None
                        and inherited_persist_selectable is not inherited_table
                    ):
                        inherited_persist_selectable._refresh_for_new_column(c)

    def _prepare_mapper_arguments(self, mapper_kw):
        properties = self.properties

        if self.mapper_args_fn:
            mapper_args = self.mapper_args_fn()
        else:
            mapper_args = {}

        if mapper_kw:
            mapper_args.update(mapper_kw)

        if "properties" in mapper_args:
            properties = dict(properties)
            properties.update(mapper_args["properties"])

        # make sure that column copies are used rather
        # than the original columns from any mixins
        for k in ("version_id_col", "polymorphic_on"):
            if k in mapper_args:
                v = mapper_args[k]
                mapper_args[k] = self.column_copies.get(v, v)

        if "inherits" in mapper_args:
            inherits_arg = mapper_args["inherits"]
            if isinstance(inherits_arg, mapper):
                inherits_arg = inherits_arg.class_

            if inherits_arg is not self.inherits:
                raise exc.InvalidRequestError(
                    "mapper inherits argument given for non-inheriting "
                    "class %s" % (mapper_args["inherits"])
                )

        if self.inherits:
            mapper_args["inherits"] = self.inherits

        if self.inherits and not mapper_args.get("concrete", False):
            # single or joined inheritance
            # exclude any cols on the inherited table which are
            # not mapped on the parent class, to avoid
            # mapping columns specific to sibling/nephew classes
            inherited_mapper = _declared_mapping_info(self.inherits)
            inherited_table = inherited_mapper.local_table

            if "exclude_properties" not in mapper_args:
                mapper_args["exclude_properties"] = exclude_properties = set(
                    [
                        c.key
                        for c in inherited_table.c
                        if c not in inherited_mapper._columntoproperty
                    ]
                ).union(inherited_mapper.exclude_properties or ())
                exclude_properties.difference_update(
                    [c.key for c in self.declared_columns]
                )

            # look through columns in the current mapper that
            # are keyed to a propname different than the colname
            # (if names were the same, we'd have popped it out above,
            # in which case the mapper makes this combination).
            # See if the superclass has a similar column property.
            # If so, join them together.
            for k, col in list(properties.items()):
                if not isinstance(col, expression.ColumnElement):
                    continue
                if k in inherited_mapper._props:
                    p = inherited_mapper._props[k]
                    if isinstance(p, ColumnProperty):
                        # note here we place the subclass column
                        # first.  See [ticket:1892] for background.
                        properties[k] = [col] + p.columns
        result_mapper_args = mapper_args.copy()
        result_mapper_args["properties"] = properties
        self.mapper_args = result_mapper_args

    def map(self, mapper_kw=util.EMPTY_DICT):
        self._prepare_mapper_arguments(mapper_kw)
        if hasattr(self.cls, "__mapper_cls__"):
            mapper_cls = util.unbound_method_to_callable(
                self.cls.__mapper_cls__
            )
        else:
            mapper_cls = mapper

        return self.set_cls_attribute(
            "__mapper__",
            mapper_cls(self.cls, self.local_table, **self.mapper_args),
        )


@util.preload_module("sqlalchemy.orm.decl_api")
def _as_dc_declaredattr(field_metadata, sa_dataclass_metadata_key):
    # wrap lambdas inside dataclass fields inside an ad-hoc declared_attr.
    # we can't write it because field.metadata is immutable :( so we have
    # to go through extra trouble to compare these
    decl_api = util.preloaded.orm_decl_api
    obj = field_metadata[sa_dataclass_metadata_key]
    if callable(obj) and not isinstance(obj, decl_api.declared_attr):
        return decl_api.declared_attr(obj)
    else:
        return obj


class _DeferredMapperConfig(_ClassScanMapperConfig):
    _configs = util.OrderedDict()

    def _early_mapping(self, mapper_kw):
        pass

    @property
    def cls(self):
        return self._cls()

    @cls.setter
    def cls(self, class_):
        self._cls = weakref.ref(class_, self._remove_config_cls)
        self._configs[self._cls] = self

    @classmethod
    def _remove_config_cls(cls, ref):
        cls._configs.pop(ref, None)

    @classmethod
    def has_cls(cls, class_):
        # 2.6 fails on weakref if class_ is an old style class
        return isinstance(class_, type) and weakref.ref(class_) in cls._configs

    @classmethod
    def raise_unmapped_for_cls(cls, class_):
        if hasattr(class_, "_sa_raise_deferred_config"):
            class_._sa_raise_deferred_config()

        raise orm_exc.UnmappedClassError(
            class_,
            msg="Class %s has a deferred mapping on it.  It is not yet "
            "usable as a mapped class." % orm_exc._safe_cls_name(class_),
        )

    @classmethod
    def config_for_cls(cls, class_):
        return cls._configs[weakref.ref(class_)]

    @classmethod
    def classes_for_base(cls, base_cls, sort=True):
        classes_for_base = [
            m
            for m, cls_ in [(m, m.cls) for m in cls._configs.values()]
            if cls_ is not None and issubclass(cls_, base_cls)
        ]

        if not sort:
            return classes_for_base

        all_m_by_cls = dict((m.cls, m) for m in classes_for_base)

        tuples = []
        for m_cls in all_m_by_cls:
            tuples.extend(
                (all_m_by_cls[base_cls], all_m_by_cls[m_cls])
                for base_cls in m_cls.__bases__
                if base_cls in all_m_by_cls
            )
        return list(topological.sort(tuples, classes_for_base))

    def map(self, mapper_kw=util.EMPTY_DICT):
        self._configs.pop(self._cls, None)
        return super(_DeferredMapperConfig, self).map(mapper_kw)


def _add_attribute(cls, key, value):
    """add an attribute to an existing declarative class.

    This runs through the logic to determine MapperProperty,
    adds it to the Mapper, adds a column to the mapped Table, etc.

    """

    if "__mapper__" in cls.__dict__:
        if isinstance(value, Column):
            _undefer_column_name(key, value)
            cls.__table__.append_column(value, replace_existing=True)
            cls.__mapper__.add_property(key, value)
        elif isinstance(value, ColumnProperty):
            for col in value.columns:
                if isinstance(col, Column) and col.table is None:
                    _undefer_column_name(key, col)
                    cls.__table__.append_column(col, replace_existing=True)
            cls.__mapper__.add_property(key, value)
        elif isinstance(value, MapperProperty):
            cls.__mapper__.add_property(key, value)
        elif isinstance(value, QueryableAttribute) and value.key != key:
            # detect a QueryableAttribute that's already mapped being
            # assigned elsewhere in userland, turn into a synonym()
            value = SynonymProperty(value.key)
            cls.__mapper__.add_property(key, value)
        else:
            type.__setattr__(cls, key, value)
            cls.__mapper__._expire_memoizations()
    else:
        type.__setattr__(cls, key, value)


def _del_attribute(cls, key):

    if (
        "__mapper__" in cls.__dict__
        and key in cls.__dict__
        and not cls.__mapper__._dispose_called
    ):
        value = cls.__dict__[key]
        if isinstance(
            value, (Column, ColumnProperty, MapperProperty, QueryableAttribute)
        ):
            raise NotImplementedError(
                "Can't un-map individual mapped attributes on a mapped class."
            )
        else:
            type.__delattr__(cls, key)
            cls.__mapper__._expire_memoizations()
    else:
        type.__delattr__(cls, key)


def _declarative_constructor(self, **kwargs):
    """A simple constructor that allows initialization from kwargs.

    Sets attributes on the constructed instance using the names and
    values in ``kwargs``.

    Only keys that are present as
    attributes of the instance's class are allowed. These could be,
    for example, any mapped columns or relationships.
    """
    cls_ = type(self)
    for k in kwargs:
        if not hasattr(cls_, k):
            raise TypeError(
                "%r is an invalid keyword argument for %s" % (k, cls_.__name__)
            )
        setattr(self, k, kwargs[k])


_declarative_constructor.__name__ = "__init__"


def _undefer_column_name(key, column):
    if column.key is None:
        column.key = key
    if column.name is None:
        column.name = key
