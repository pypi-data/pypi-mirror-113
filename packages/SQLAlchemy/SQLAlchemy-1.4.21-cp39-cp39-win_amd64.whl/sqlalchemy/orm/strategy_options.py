# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""

"""

from . import util as orm_util
from .attributes import QueryableAttribute
from .base import _class_to_mapper
from .base import _is_aliased_class
from .base import _is_mapped_class
from .base import InspectionAttr
from .interfaces import LoaderOption
from .interfaces import MapperProperty
from .interfaces import PropComparator
from .path_registry import _DEFAULT_TOKEN
from .path_registry import _WILDCARD_TOKEN
from .path_registry import PathRegistry
from .path_registry import TokenRegistry
from .util import _orm_full_deannotate
from .. import exc as sa_exc
from .. import inspect
from .. import util
from ..sql import and_
from ..sql import coercions
from ..sql import roles
from ..sql import visitors
from ..sql.base import _generative
from ..sql.base import Generative


class Load(Generative, LoaderOption):
    """Represents loader options which modify the state of a
    :class:`_query.Query` in order to affect how various mapped attributes are
    loaded.

    The :class:`_orm.Load` object is in most cases used implicitly behind the
    scenes when one makes use of a query option like :func:`_orm.joinedload`,
    :func:`.defer`, or similar.   However, the :class:`_orm.Load` object
    can also be used directly, and in some cases can be useful.

    To use :class:`_orm.Load` directly, instantiate it with the target mapped
    class as the argument.   This style of usage is
    useful when dealing with a :class:`_query.Query`
    that has multiple entities::

        myopt = Load(MyClass).joinedload("widgets")

    The above ``myopt`` can now be used with :meth:`_query.Query.options`,
    where it
    will only take effect for the ``MyClass`` entity::

        session.query(MyClass, MyOtherClass).options(myopt)

    One case where :class:`_orm.Load`
    is useful as public API is when specifying
    "wildcard" options that only take effect for a certain class::

        session.query(Order).options(Load(Order).lazyload('*'))

    Above, all relationships on ``Order`` will be lazy-loaded, but other
    attributes on those descendant objects will load using their normal
    loader strategy.

    .. seealso::

        :ref:`deferred_options`

        :ref:`deferred_loading_w_multiple`

        :ref:`relationship_loader_options`

    """

    _cache_key_traversal = [
        ("path", visitors.ExtendedInternalTraversal.dp_has_cache_key),
        ("strategy", visitors.ExtendedInternalTraversal.dp_plain_obj),
        ("_of_type", visitors.ExtendedInternalTraversal.dp_multi),
        ("_extra_criteria", visitors.InternalTraversal.dp_clauseelement_list),
        (
            "_context_cache_key",
            visitors.ExtendedInternalTraversal.dp_has_cache_key_tuples,
        ),
        (
            "local_opts",
            visitors.ExtendedInternalTraversal.dp_string_multi_dict,
        ),
    ]

    def __init__(self, entity):
        insp = inspect(entity)
        insp._post_inspect

        self.path = insp._path_registry
        # note that this .context is shared among all descendant
        # Load objects
        self.context = util.OrderedDict()
        self.local_opts = {}
        self.is_class_strategy = False

    @classmethod
    def for_existing_path(cls, path):
        load = cls.__new__(cls)
        load.path = path
        load.context = {}
        load.local_opts = {}
        load._of_type = None
        load._extra_criteria = ()
        return load

    def _generate_extra_criteria(self, context):
        """Apply the current bound parameters in a QueryContext to the
        "extra_criteria" stored with this Load object.

        Load objects are typically pulled from the cached version of
        the statement from a QueryContext.  The statement currently being
        executed will have new values (and keys) for bound parameters in the
        extra criteria which need to be applied by loader strategies when
        they handle this criteria for a result set.

        """

        assert (
            self._extra_criteria
        ), "this should only be called if _extra_criteria is present"

        orig_query = context.compile_state.select_statement
        current_query = context.query

        # NOTE: while it seems like we should not do the "apply" operation
        # here if orig_query is current_query, skipping it in the "optimized"
        # case causes the query to be different from a cache key perspective,
        # because we are creating a copy of the criteria which is no longer
        # the same identity of the _extra_criteria in the loader option
        # itself.  cache key logic produces a different key for
        # (A, copy_of_A) vs. (A, A), because in the latter case it shortens
        # the second part of the key to just indicate on identity.

        # if orig_query is current_query:
        # not cached yet.   just do the and_()
        #    return and_(*self._extra_criteria)

        k1 = orig_query._generate_cache_key()
        k2 = current_query._generate_cache_key()

        return k2._apply_params_to_element(k1, and_(*self._extra_criteria))

    @property
    def _context_cache_key(self):
        serialized = []
        if self.context is None:
            return []
        for (key, loader_path), obj in self.context.items():
            if key != "loader":
                continue
            serialized.append(loader_path + (obj,))
        return serialized

    def _generate(self):
        cloned = super(Load, self)._generate()
        cloned.local_opts = {}
        return cloned

    is_opts_only = False
    is_class_strategy = False
    strategy = None
    propagate_to_loaders = False
    _of_type = None
    _extra_criteria = ()

    def process_compile_state_replaced_entities(
        self, compile_state, mapper_entities
    ):
        if not compile_state.compile_options._enable_eagerloads:
            return

        # process is being run here so that the options given are validated
        # against what the lead entities were, as well as to accommodate
        # for the entities having been replaced with equivalents
        self._process(
            compile_state,
            mapper_entities,
            not bool(compile_state.current_path),
        )

    def process_compile_state(self, compile_state):
        if not compile_state.compile_options._enable_eagerloads:
            return

        self._process(
            compile_state,
            compile_state._lead_mapper_entities,
            not bool(compile_state.current_path),
        )

    def _process(self, compile_state, mapper_entities, raiseerr):
        is_refresh = compile_state.compile_options._for_refresh_state
        current_path = compile_state.current_path
        if current_path:
            for (token, start_path), loader in self.context.items():
                if is_refresh and not loader.propagate_to_loaders:
                    continue
                chopped_start_path = self._chop_path(start_path, current_path)
                if chopped_start_path is not None:
                    compile_state.attributes[
                        (token, chopped_start_path)
                    ] = loader
        else:
            compile_state.attributes.update(self.context)

    def _generate_path(
        self,
        path,
        attr,
        for_strategy,
        wildcard_key,
        raiseerr=True,
        polymorphic_entity_context=None,
    ):
        existing_of_type = self._of_type
        self._of_type = None
        if raiseerr and not path.has_entity:
            if isinstance(path, TokenRegistry):
                raise sa_exc.ArgumentError(
                    "Wildcard token cannot be followed by another entity"
                )
            else:
                raise sa_exc.ArgumentError(
                    "Mapped attribute '%s' does not "
                    "refer to a mapped entity" % (path.prop,)
                )

        if isinstance(attr, util.string_types):
            default_token = attr.endswith(_DEFAULT_TOKEN)
            attr_str_name = attr
            if attr.endswith(_WILDCARD_TOKEN) or default_token:
                if default_token:
                    self.propagate_to_loaders = False
                if wildcard_key:
                    attr = "%s:%s" % (wildcard_key, attr)

                # TODO: AliasedInsp inside the path for of_type is not
                # working for a with_polymorphic entity because the
                # relationship loaders don't render the with_poly into the
                # path.  See #4469 which will try to improve this
                if existing_of_type and not existing_of_type.is_aliased_class:
                    path = path.parent[existing_of_type]
                path = path.token(attr)
                self.path = path
                return path

            if existing_of_type:
                ent = inspect(existing_of_type)
            else:
                ent = path.entity

            util.warn_deprecated_20(
                "Using strings to indicate column or "
                "relationship paths in loader options is deprecated "
                "and will be removed in SQLAlchemy 2.0.  Please use "
                "the class-bound attribute directly."
            )
            try:
                # use getattr on the class to work around
                # synonyms, hybrids, etc.
                attr = getattr(ent.class_, attr)
            except AttributeError as err:
                if raiseerr:
                    util.raise_(
                        sa_exc.ArgumentError(
                            'Can\'t find property named "%s" on '
                            "%s in this Query." % (attr, ent)
                        ),
                        replace_context=err,
                    )
                else:
                    return None
            else:
                try:
                    attr = found_property = attr.property
                except AttributeError as ae:
                    if not isinstance(attr, MapperProperty):
                        util.raise_(
                            sa_exc.ArgumentError(
                                'Expected attribute "%s" on %s to be a '
                                "mapped attribute; "
                                "instead got %s object."
                                % (attr_str_name, ent, type(attr))
                            ),
                            replace_context=ae,
                        )
                    else:
                        raise

            path = path[attr]
        else:
            insp = inspect(attr)

            if insp.is_mapper or insp.is_aliased_class:
                # TODO: this does not appear to be a valid codepath.  "attr"
                # would never be a mapper.  This block is present in 1.2
                # as well however does not seem to be accessed in any tests.
                if not orm_util._entity_corresponds_to_use_path_impl(
                    attr.parent, path[-1]
                ):
                    if raiseerr:
                        raise sa_exc.ArgumentError(
                            "Attribute '%s' does not "
                            "link from element '%s'" % (attr, path.entity)
                        )
                    else:
                        return None
            elif insp.is_property:
                prop = found_property = attr
                path = path[prop]
            elif insp.is_attribute:
                prop = found_property = attr.property

                if not orm_util._entity_corresponds_to_use_path_impl(
                    attr.parent, path[-1]
                ):
                    if raiseerr:
                        raise sa_exc.ArgumentError(
                            'Attribute "%s" does not '
                            'link from element "%s".%s'
                            % (
                                attr,
                                path.entity,
                                (
                                    "  Did you mean to use "
                                    "%s.of_type(%s)?"
                                    % (path[-2], attr.class_.__name__)
                                    if len(path) > 1
                                    and path.entity.is_mapper
                                    and attr.parent.is_aliased_class
                                    else ""
                                ),
                            )
                        )
                    else:
                        return None

                if attr._extra_criteria:
                    self._extra_criteria = attr._extra_criteria

                if getattr(attr, "_of_type", None):
                    ac = attr._of_type
                    ext_info = of_type_info = inspect(ac)

                    if polymorphic_entity_context is None:
                        polymorphic_entity_context = self.context

                    existing = path.entity_path[prop].get(
                        polymorphic_entity_context, "path_with_polymorphic"
                    )

                    if not ext_info.is_aliased_class:
                        ac = orm_util.with_polymorphic(
                            ext_info.mapper.base_mapper,
                            ext_info.mapper,
                            aliased=True,
                            _use_mapper_path=True,
                            _existing_alias=inspect(existing)
                            if existing is not None
                            else None,
                        )

                        ext_info = inspect(ac)

                    path.entity_path[prop].set(
                        polymorphic_entity_context, "path_with_polymorphic", ac
                    )

                    path = path[prop][ext_info]

                    self._of_type = of_type_info

                else:
                    path = path[prop]

        if for_strategy is not None:
            found_property._get_strategy(for_strategy)
        if path.has_entity:
            path = path.entity_path
        self.path = path
        return path

    def __str__(self):
        return "Load(strategy=%r)" % (self.strategy,)

    def _coerce_strat(self, strategy):
        if strategy is not None:
            strategy = tuple(sorted(strategy.items()))
        return strategy

    def _apply_to_parent(self, parent, applied, bound):
        raise NotImplementedError(
            "Only 'unbound' loader options may be used with the "
            "Load.options() method"
        )

    @_generative
    def options(self, *opts):
        r"""Apply a series of options as sub-options to this
        :class:`_orm.Load`
        object.

        E.g.::

            query = session.query(Author)
            query = query.options(
                        joinedload(Author.book).options(
                            load_only("summary", "excerpt"),
                            joinedload(Book.citations).options(
                                joinedload(Citation.author)
                            )
                        )
                    )

        :param \*opts: A series of loader option objects (ultimately
         :class:`_orm.Load` objects) which should be applied to the path
         specified by this :class:`_orm.Load` object.

        .. versionadded:: 1.3.6

        .. seealso::

            :func:`.defaultload`

            :ref:`relationship_loader_options`

            :ref:`deferred_loading_w_multiple`

        """
        apply_cache = {}
        bound = not isinstance(self, _UnboundLoad)
        if bound:
            raise NotImplementedError(
                "The options() method is currently only supported "
                "for 'unbound' loader options"
            )
        for opt in opts:
            opt._apply_to_parent(self, apply_cache, bound)

    @_generative
    def set_relationship_strategy(
        self, attr, strategy, propagate_to_loaders=True
    ):
        strategy = self._coerce_strat(strategy)
        self.propagate_to_loaders = propagate_to_loaders
        cloned = self._clone_for_bind_strategy(attr, strategy, "relationship")
        self.path = cloned.path
        self._of_type = cloned._of_type
        self._extra_criteria = cloned._extra_criteria
        cloned.is_class_strategy = self.is_class_strategy = False
        self.propagate_to_loaders = cloned.propagate_to_loaders

    @_generative
    def set_column_strategy(self, attrs, strategy, opts=None, opts_only=False):
        strategy = self._coerce_strat(strategy)
        self.is_class_strategy = False
        for attr in attrs:
            cloned = self._clone_for_bind_strategy(
                attr, strategy, "column", opts_only=opts_only, opts=opts
            )
            cloned.propagate_to_loaders = True

    @_generative
    def set_generic_strategy(self, attrs, strategy):
        strategy = self._coerce_strat(strategy)
        for attr in attrs:
            cloned = self._clone_for_bind_strategy(attr, strategy, None)
            cloned.propagate_to_loaders = True

    @_generative
    def set_class_strategy(self, strategy, opts):
        strategy = self._coerce_strat(strategy)
        cloned = self._clone_for_bind_strategy(None, strategy, None)
        cloned.is_class_strategy = True
        cloned.propagate_to_loaders = True
        cloned.local_opts.update(opts)

    def _clone_for_bind_strategy(
        self, attr, strategy, wildcard_key, opts_only=False, opts=None
    ):
        """Create an anonymous clone of the Load/_UnboundLoad that is suitable
        to be placed in the context / _to_bind collection of this Load
        object.   The clone will then lose references to context/_to_bind
        in order to not create reference cycles.

        """
        cloned = self._generate()
        cloned._generate_path(self.path, attr, strategy, wildcard_key)
        cloned.strategy = strategy

        cloned.local_opts = self.local_opts
        if opts:
            cloned.local_opts.update(opts)
        if opts_only:
            cloned.is_opts_only = True

        if strategy or cloned.is_opts_only:
            cloned._set_path_strategy()
        return cloned

    def _set_for_path(self, context, path, replace=True, merge_opts=False):
        if merge_opts or not replace:
            existing = path.get(context, "loader")
            if existing:
                if merge_opts:
                    existing.local_opts.update(self.local_opts)
                    existing._extra_criteria += self._extra_criteria
            else:
                path.set(context, "loader", self)
        else:
            existing = path.get(context, "loader")
            path.set(context, "loader", self)
            if existing and existing.is_opts_only:
                self.local_opts.update(existing.local_opts)
                existing._extra_criteria += self._extra_criteria

    def _set_path_strategy(self):
        if not self.is_class_strategy and self.path.has_entity:
            effective_path = self.path.parent
        else:
            effective_path = self.path

        if effective_path.is_token:
            for path in effective_path.generate_for_superclasses():
                self._set_for_path(
                    self.context,
                    path,
                    replace=True,
                    merge_opts=self.is_opts_only,
                )
        else:
            self._set_for_path(
                self.context,
                effective_path,
                replace=True,
                merge_opts=self.is_opts_only,
            )

        # remove cycles; _set_path_strategy is always invoked on an
        # anonymous clone of the Load / UnboundLoad object since #5056
        self.context = None

    def __getstate__(self):
        d = self.__dict__.copy()

        # can't pickle this right now; warning is raised by strategies
        d["_extra_criteria"] = ()

        if d["context"] is not None:
            d["context"] = PathRegistry.serialize_context_dict(
                d["context"], ("loader",)
            )
        d["path"] = self.path.serialize()
        return d

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.path = PathRegistry.deserialize(self.path)
        if self.context is not None:
            self.context = PathRegistry.deserialize_context_dict(self.context)

    def _chop_path(self, to_chop, path):
        i = -1

        for i, (c_token, p_token) in enumerate(zip(to_chop, path.path)):
            if isinstance(c_token, util.string_types):
                # TODO: this is approximated from the _UnboundLoad
                # version and probably has issues, not fully covered.

                if i == 0 and c_token.endswith(":" + _DEFAULT_TOKEN):
                    return to_chop
                elif (
                    c_token != "relationship:%s" % (_WILDCARD_TOKEN,)
                    and c_token != p_token.key
                ):
                    return None

            if c_token is p_token:
                continue
            elif (
                isinstance(c_token, InspectionAttr)
                and c_token.is_mapper
                and p_token.is_mapper
                and c_token.isa(p_token)
            ):
                continue
            else:
                return None
        return to_chop[i + 1 :]


class _UnboundLoad(Load):
    """Represent a loader option that isn't tied to a root entity.

    The loader option will produce an entity-linked :class:`_orm.Load`
    object when it is passed :meth:`_query.Query.options`.

    This provides compatibility with the traditional system
    of freestanding options, e.g. ``joinedload('x.y.z')``.

    """

    def __init__(self):
        self.path = ()
        self._to_bind = []
        self.local_opts = {}
        self._extra_criteria = ()

    _cache_key_traversal = [
        ("path", visitors.ExtendedInternalTraversal.dp_multi_list),
        ("strategy", visitors.ExtendedInternalTraversal.dp_plain_obj),
        ("_to_bind", visitors.ExtendedInternalTraversal.dp_has_cache_key_list),
        ("_extra_criteria", visitors.InternalTraversal.dp_clauseelement_list),
        (
            "local_opts",
            visitors.ExtendedInternalTraversal.dp_string_multi_dict,
        ),
    ]

    _is_chain_link = False

    def _set_path_strategy(self):
        self._to_bind.append(self)

        # remove cycles; _set_path_strategy is always invoked on an
        # anonymous clone of the Load / UnboundLoad object since #5056
        self._to_bind = None

    def _apply_to_parent(self, parent, applied, bound, to_bind=None):
        if self in applied:
            return applied[self]

        if to_bind is None:
            to_bind = self._to_bind

        cloned = self._generate()

        applied[self] = cloned

        cloned.strategy = self.strategy
        if self.path:
            attr = self.path[-1]
            if isinstance(attr, util.string_types) and attr.endswith(
                _DEFAULT_TOKEN
            ):
                attr = attr.split(":")[0] + ":" + _WILDCARD_TOKEN
            cloned._generate_path(
                parent.path + self.path[0:-1], attr, self.strategy, None
            )

        # these assertions can go away once the "sub options" API is
        # mature
        assert cloned.propagate_to_loaders == self.propagate_to_loaders
        assert cloned.is_class_strategy == self.is_class_strategy
        assert cloned.is_opts_only == self.is_opts_only

        new_to_bind = {
            elem._apply_to_parent(parent, applied, bound, to_bind)
            for elem in to_bind
        }
        cloned._to_bind = parent._to_bind
        cloned._to_bind.extend(new_to_bind)
        cloned.local_opts.update(self.local_opts)

        return cloned

    def _generate_path(self, path, attr, for_strategy, wildcard_key):
        if (
            wildcard_key
            and isinstance(attr, util.string_types)
            and attr in (_WILDCARD_TOKEN, _DEFAULT_TOKEN)
        ):
            if attr == _DEFAULT_TOKEN:
                self.propagate_to_loaders = False
            attr = "%s:%s" % (wildcard_key, attr)
        if path and _is_mapped_class(path[-1]) and not self.is_class_strategy:
            path = path[0:-1]
        if attr:
            path = path + (attr,)
        self.path = path
        self._extra_criteria = getattr(attr, "_extra_criteria", ())

        return path

    def __getstate__(self):
        d = self.__dict__.copy()

        # can't pickle this right now; warning is raised by strategies
        d["_extra_criteria"] = ()

        d["path"] = self._serialize_path(self.path, filter_aliased_class=True)
        return d

    def __setstate__(self, state):
        ret = []
        for key in state["path"]:
            if isinstance(key, tuple):
                if len(key) == 2:
                    # support legacy
                    cls, propkey = key
                    of_type = None
                else:
                    cls, propkey, of_type = key
                prop = getattr(cls, propkey)
                if of_type:
                    prop = prop.of_type(of_type)
                ret.append(prop)
            else:
                ret.append(key)
        state["path"] = tuple(ret)
        self.__dict__ = state

    def _process(self, compile_state, mapper_entities, raiseerr):
        dedupes = compile_state.attributes["_unbound_load_dedupes"]
        is_refresh = compile_state.compile_options._for_refresh_state
        for val in self._to_bind:
            if val not in dedupes:
                dedupes.add(val)
                if is_refresh and not val.propagate_to_loaders:
                    continue
                val._bind_loader(
                    [ent.entity_zero for ent in mapper_entities],
                    compile_state.current_path,
                    compile_state.attributes,
                    raiseerr,
                )

    @classmethod
    def _from_keys(cls, meth, keys, chained, kw):
        opt = _UnboundLoad()

        def _split_key(key):
            if isinstance(key, util.string_types):
                # coerce fooload('*') into "default loader strategy"
                if key == _WILDCARD_TOKEN:
                    return (_DEFAULT_TOKEN,)
                # coerce fooload(".*") into "wildcard on default entity"
                elif key.startswith("." + _WILDCARD_TOKEN):
                    key = key[1:]
                return key.split(".")
            else:
                return (key,)

        all_tokens = [token for key in keys for token in _split_key(key)]

        for token in all_tokens[0:-1]:
            # set _is_chain_link first so that clones of the
            # object also inherit this flag
            opt._is_chain_link = True
            if chained:
                opt = meth(opt, token, **kw)
            else:
                opt = opt.defaultload(token)

        opt = meth(opt, all_tokens[-1], **kw)
        opt._is_chain_link = False
        return opt

    def _chop_path(self, to_chop, path):
        i = -1
        for i, (c_token, (p_entity, p_prop)) in enumerate(
            zip(to_chop, path.pairs())
        ):
            if isinstance(c_token, util.string_types):
                if i == 0 and c_token.endswith(":" + _DEFAULT_TOKEN):
                    return to_chop
                elif (
                    c_token != "relationship:%s" % (_WILDCARD_TOKEN,)
                    and c_token != p_prop.key
                ):
                    return None
            elif isinstance(c_token, PropComparator):
                if c_token.property is not p_prop or (
                    c_token._parententity is not p_entity
                    and (
                        not c_token._parententity.is_mapper
                        or not c_token._parententity.isa(p_entity)
                    )
                ):
                    return None
        else:
            i += 1

        return to_chop[i:]

    def _serialize_path(self, path, filter_aliased_class=False):
        ret = []
        for token in path:
            if isinstance(token, QueryableAttribute):
                if (
                    filter_aliased_class
                    and token._of_type
                    and inspect(token._of_type).is_aliased_class
                ):
                    ret.append((token._parentmapper.class_, token.key, None))
                else:
                    ret.append(
                        (
                            token._parentmapper.class_,
                            token.key,
                            token._of_type.entity if token._of_type else None,
                        )
                    )
            elif isinstance(token, PropComparator):
                ret.append((token._parentmapper.class_, token.key, None))
            else:
                ret.append(token)
        return ret

    def _bind_loader(self, entities, current_path, context, raiseerr):
        """Convert from an _UnboundLoad() object into a Load() object.

        The _UnboundLoad() uses an informal "path" and does not necessarily
        refer to a lead entity as it may use string tokens.   The Load()
        OTOH refers to a complete path.   This method reconciles from a
        given Query into a Load.

        Example::


            query = session.query(User).options(
                joinedload("orders").joinedload("items"))

        The above options will be an _UnboundLoad object along the lines
        of (note this is not the exact API of _UnboundLoad)::

            _UnboundLoad(
                _to_bind=[
                    _UnboundLoad(["orders"], {"lazy": "joined"}),
                    _UnboundLoad(["orders", "items"], {"lazy": "joined"}),
                ]
            )

        After this method, we get something more like this (again this is
        not exact API)::

            Load(
                User,
                (User, User.orders.property))
            Load(
                User,
                (User, User.orders.property, Order, Order.items.property))

        """

        start_path = self.path

        if self.is_class_strategy and current_path:
            start_path += (entities[0],)

        # _current_path implies we're in a
        # secondary load with an existing path

        if current_path:
            start_path = self._chop_path(start_path, current_path)

        if not start_path:
            return None

        # look at the first token and try to locate within the Query
        # what entity we are referring towards.
        token = start_path[0]

        if isinstance(token, util.string_types):
            entity = self._find_entity_basestring(entities, token, raiseerr)
        elif isinstance(token, PropComparator):
            prop = token.property
            entity = self._find_entity_prop_comparator(
                entities, prop, token._parententity, raiseerr
            )
        elif self.is_class_strategy and _is_mapped_class(token):
            entity = inspect(token)
            if entity not in entities:
                entity = None
        else:
            raise sa_exc.ArgumentError(
                "mapper option expects " "string key or list of attributes"
            )

        if not entity:
            return

        path_element = entity

        # transfer our entity-less state into a Load() object
        # with a real entity path.  Start with the lead entity
        # we just located, then go through the rest of our path
        # tokens and populate into the Load().
        loader = Load(path_element)

        if context is None:
            context = loader.context

        loader.strategy = self.strategy
        loader.is_opts_only = self.is_opts_only
        loader.is_class_strategy = self.is_class_strategy

        path = loader.path

        if not loader.is_class_strategy:
            for idx, token in enumerate(start_path):
                if not loader._generate_path(
                    loader.path,
                    token,
                    self.strategy if idx == len(start_path) - 1 else None,
                    None,
                    raiseerr,
                    polymorphic_entity_context=context,
                ):
                    return

        loader.local_opts.update(self.local_opts)

        if not loader.is_class_strategy and loader.path.has_entity:
            effective_path = loader.path.parent
        else:
            effective_path = loader.path

        # prioritize "first class" options over those
        # that were "links in the chain", e.g. "x" and "y" in
        # someload("x.y.z") versus someload("x") / someload("x.y")

        if effective_path.is_token:
            for path in effective_path.generate_for_superclasses():
                loader._set_for_path(
                    context,
                    path,
                    replace=not self._is_chain_link,
                    merge_opts=self.is_opts_only,
                )
        else:
            loader._set_for_path(
                context,
                effective_path,
                replace=not self._is_chain_link,
                merge_opts=self.is_opts_only,
            )

        return loader

    def _find_entity_prop_comparator(self, entities, prop, mapper, raiseerr):
        if _is_aliased_class(mapper):
            searchfor = mapper
        else:
            searchfor = _class_to_mapper(mapper)
        for ent in entities:
            if orm_util._entity_corresponds_to(ent, searchfor):
                return ent
        else:
            if raiseerr:
                if not list(entities):
                    raise sa_exc.ArgumentError(
                        "Query has only expression-based entities, "
                        'which do not apply to %s "%s"'
                        % (util.clsname_as_plain_name(type(prop)), prop)
                    )
                else:
                    raise sa_exc.ArgumentError(
                        'Mapped attribute "%s" does not apply to any of the '
                        "root entities in this query, e.g. %s. Please "
                        "specify the full path "
                        "from one of the root entities to the target "
                        "attribute. "
                        % (prop, ", ".join(str(x) for x in entities))
                    )
            else:
                return None

    def _find_entity_basestring(self, entities, token, raiseerr):
        if token.endswith(":" + _WILDCARD_TOKEN):
            if len(list(entities)) != 1:
                if raiseerr:
                    raise sa_exc.ArgumentError(
                        "Can't apply wildcard ('*') or load_only() "
                        "loader option to multiple entities %s. Specify "
                        "loader options for each entity individually, such "
                        "as %s."
                        % (
                            ", ".join(str(ent) for ent in entities),
                            ", ".join(
                                "Load(%s).some_option('*')" % ent
                                for ent in entities
                            ),
                        )
                    )
        elif token.endswith(_DEFAULT_TOKEN):
            raiseerr = False

        for ent in entities:
            # return only the first _MapperEntity when searching
            # based on string prop name.   Ideally object
            # attributes are used to specify more exactly.
            return ent
        else:
            if raiseerr:
                raise sa_exc.ArgumentError(
                    "Query has only expression-based entities - "
                    'can\'t find property named "%s".' % (token,)
                )
            else:
                return None


class loader_option(object):
    def __init__(self):
        pass

    def __call__(self, fn):
        self.name = name = fn.__name__
        self.fn = fn
        if hasattr(Load, name):
            raise TypeError("Load class already has a %s method." % (name))
        setattr(Load, name, fn)

        return self

    def _add_unbound_fn(self, fn):
        self._unbound_fn = fn
        fn_doc = self.fn.__doc__
        self.fn.__doc__ = """Produce a new :class:`_orm.Load` object with the
:func:`_orm.%(name)s` option applied.

See :func:`_orm.%(name)s` for usage examples.

""" % {
            "name": self.name
        }

        fn.__doc__ = fn_doc
        return self

    def _add_unbound_all_fn(self, fn):
        fn.__doc__ = """Produce a standalone "all" option for
:func:`_orm.%(name)s`.

.. deprecated:: 0.9

    The :func:`_orm.%(name)s_all` function is deprecated, and will be removed
    in a future release.  Please use method chaining with
    :func:`_orm.%(name)s` instead, as in::

        session.query(MyClass).options(
            %(name)s("someattribute").%(name)s("anotherattribute")
        )

""" % {
            "name": self.name
        }
        fn = util.deprecated(
            # This is used by `baked_lazyload_all` was only deprecated in
            # version 1.2 so this must stick around until that is removed
            "0.9",
            "The :func:`.%(name)s_all` function is deprecated, and will be "
            "removed in a future release.  Please use method chaining with "
            ":func:`.%(name)s` instead" % {"name": self.name},
            add_deprecation_to_docstring=False,
        )(fn)

        self._unbound_all_fn = fn
        return self


@loader_option()
def contains_eager(loadopt, attr, alias=None):
    r"""Indicate that the given attribute should be eagerly loaded from
    columns stated manually in the query.

    This function is part of the :class:`_orm.Load` interface and supports
    both method-chained and standalone operation.

    The option is used in conjunction with an explicit join that loads
    the desired rows, i.e.::

        sess.query(Order).\
                join(Order.user).\
                options(contains_eager(Order.user))

    The above query would join from the ``Order`` entity to its related
    ``User`` entity, and the returned ``Order`` objects would have the
    ``Order.user`` attribute pre-populated.

    It may also be used for customizing the entries in an eagerly loaded
    collection; queries will normally want to use the
    :meth:`_query.Query.populate_existing` method assuming the primary
    collection of parent objects may already have been loaded::

        sess.query(User).\
            join(User.addresses).\
            filter(Address.email_address.like('%@aol.com')).\
            options(contains_eager(User.addresses)).\
            populate_existing()

    See the section :ref:`contains_eager` for complete usage details.

    .. seealso::

        :ref:`loading_toplevel`

        :ref:`contains_eager`

    """
    if alias is not None:
        if not isinstance(alias, str):
            info = inspect(alias)
            alias = info.selectable

        else:
            util.warn_deprecated(
                "Passing a string name for the 'alias' argument to "
                "'contains_eager()` is deprecated, and will not work in a "
                "future release.  Please use a sqlalchemy.alias() or "
                "sqlalchemy.orm.aliased() construct.",
                version="1.4",
            )

    elif getattr(attr, "_of_type", None):
        ot = inspect(attr._of_type)
        alias = ot.selectable

    cloned = loadopt.set_relationship_strategy(
        attr, {"lazy": "joined"}, propagate_to_loaders=False
    )
    cloned.local_opts["eager_from_alias"] = alias
    return cloned


@contains_eager._add_unbound_fn
def contains_eager(*keys, **kw):
    return _UnboundLoad()._from_keys(
        _UnboundLoad.contains_eager, keys, True, kw
    )


@loader_option()
def load_only(loadopt, *attrs):
    """Indicate that for a particular entity, only the given list
    of column-based attribute names should be loaded; all others will be
    deferred.

    This function is part of the :class:`_orm.Load` interface and supports
    both method-chained and standalone operation.

    Example - given a class ``User``, load only the ``name`` and ``fullname``
    attributes::

        session.query(User).options(load_only("name", "fullname"))

    Example - given a relationship ``User.addresses -> Address``, specify
    subquery loading for the ``User.addresses`` collection, but on each
    ``Address`` object load only the ``email_address`` attribute::

        session.query(User).options(
                subqueryload("addresses").load_only("email_address")
        )

    For a :class:`_query.Query` that has multiple entities,
    the lead entity can be
    specifically referred to using the :class:`_orm.Load` constructor::

        session.query(User, Address).join(User.addresses).options(
                    Load(User).load_only("name", "fullname"),
                    Load(Address).load_only("email_address")
                )

     .. note:: This method will still load a :class:`_schema.Column` even
        if the column property is defined with ``deferred=True``
        for the :func:`.column_property` function.

    .. versionadded:: 0.9.0

    """
    cloned = loadopt.set_column_strategy(
        attrs, {"deferred": False, "instrument": True}
    )
    cloned.set_column_strategy(
        "*", {"deferred": True, "instrument": True}, {"undefer_pks": True}
    )
    return cloned


@load_only._add_unbound_fn
def load_only(*attrs):
    return _UnboundLoad().load_only(*attrs)


@loader_option()
def joinedload(loadopt, attr, innerjoin=None):
    """Indicate that the given attribute should be loaded using joined
    eager loading.

    This function is part of the :class:`_orm.Load` interface and supports
    both method-chained and standalone operation.

    examples::

        # joined-load the "orders" collection on "User"
        query(User).options(joinedload(User.orders))

        # joined-load Order.items and then Item.keywords
        query(Order).options(
            joinedload(Order.items).joinedload(Item.keywords))

        # lazily load Order.items, but when Items are loaded,
        # joined-load the keywords collection
        query(Order).options(
            lazyload(Order.items).joinedload(Item.keywords))

    :param innerjoin: if ``True``, indicates that the joined eager load should
     use an inner join instead of the default of left outer join::

        query(Order).options(joinedload(Order.user, innerjoin=True))

     In order to chain multiple eager joins together where some may be
     OUTER and others INNER, right-nested joins are used to link them::

        query(A).options(
            joinedload(A.bs, innerjoin=False).
                joinedload(B.cs, innerjoin=True)
        )

     The above query, linking A.bs via "outer" join and B.cs via "inner" join
     would render the joins as "a LEFT OUTER JOIN (b JOIN c)".   When using
     older versions of SQLite (< 3.7.16), this form of JOIN is translated to
     use full subqueries as this syntax is otherwise not directly supported.

     The ``innerjoin`` flag can also be stated with the term ``"unnested"``.
     This indicates that an INNER JOIN should be used, *unless* the join
     is linked to a LEFT OUTER JOIN to the left, in which case it
     will render as LEFT OUTER JOIN.  For example, supposing ``A.bs``
     is an outerjoin::

        query(A).options(
            joinedload(A.bs).
                joinedload(B.cs, innerjoin="unnested")
        )

     The above join will render as "a LEFT OUTER JOIN b LEFT OUTER JOIN c",
     rather than as "a LEFT OUTER JOIN (b JOIN c)".

     .. note:: The "unnested" flag does **not** affect the JOIN rendered
        from a many-to-many association table, e.g. a table configured
        as :paramref:`_orm.relationship.secondary`, to the target table; for
        correctness of results, these joins are always INNER and are
        therefore right-nested if linked to an OUTER join.

     .. versionchanged:: 1.0.0 ``innerjoin=True`` now implies
        ``innerjoin="nested"``, whereas in 0.9 it implied
        ``innerjoin="unnested"``.  In order to achieve the pre-1.0 "unnested"
        inner join behavior, use the value ``innerjoin="unnested"``.
        See :ref:`migration_3008`.

    .. note::

        The joins produced by :func:`_orm.joinedload` are **anonymously
        aliased**.  The criteria by which the join proceeds cannot be
        modified, nor can the :class:`_query.Query`
        refer to these joins in any way,
        including ordering.  See :ref:`zen_of_eager_loading` for further
        detail.

        To produce a specific SQL JOIN which is explicitly available, use
        :meth:`_query.Query.join`.
        To combine explicit JOINs with eager loading
        of collections, use :func:`_orm.contains_eager`; see
        :ref:`contains_eager`.

    .. seealso::

        :ref:`loading_toplevel`

        :ref:`joined_eager_loading`

    """
    loader = loadopt.set_relationship_strategy(attr, {"lazy": "joined"})
    if innerjoin is not None:
        loader.local_opts["innerjoin"] = innerjoin
    return loader


@joinedload._add_unbound_fn
def joinedload(*keys, **kw):
    return _UnboundLoad._from_keys(_UnboundLoad.joinedload, keys, False, kw)


@loader_option()
def subqueryload(loadopt, attr):
    """Indicate that the given attribute should be loaded using
    subquery eager loading.

    This function is part of the :class:`_orm.Load` interface and supports
    both method-chained and standalone operation.

    examples::

        # subquery-load the "orders" collection on "User"
        query(User).options(subqueryload(User.orders))

        # subquery-load Order.items and then Item.keywords
        query(Order).options(
            subqueryload(Order.items).subqueryload(Item.keywords))

        # lazily load Order.items, but when Items are loaded,
        # subquery-load the keywords collection
        query(Order).options(
            lazyload(Order.items).subqueryload(Item.keywords))


    .. seealso::

        :ref:`loading_toplevel`

        :ref:`subquery_eager_loading`

    """
    return loadopt.set_relationship_strategy(attr, {"lazy": "subquery"})


@subqueryload._add_unbound_fn
def subqueryload(*keys):
    return _UnboundLoad._from_keys(_UnboundLoad.subqueryload, keys, False, {})


@loader_option()
def selectinload(loadopt, attr):
    """Indicate that the given attribute should be loaded using
    SELECT IN eager loading.

    This function is part of the :class:`_orm.Load` interface and supports
    both method-chained and standalone operation.

    examples::

        # selectin-load the "orders" collection on "User"
        query(User).options(selectinload(User.orders))

        # selectin-load Order.items and then Item.keywords
        query(Order).options(
            selectinload(Order.items).selectinload(Item.keywords))

        # lazily load Order.items, but when Items are loaded,
        # selectin-load the keywords collection
        query(Order).options(
            lazyload(Order.items).selectinload(Item.keywords))

    .. versionadded:: 1.2

    .. seealso::

        :ref:`loading_toplevel`

        :ref:`selectin_eager_loading`

    """
    return loadopt.set_relationship_strategy(attr, {"lazy": "selectin"})


@selectinload._add_unbound_fn
def selectinload(*keys):
    return _UnboundLoad._from_keys(_UnboundLoad.selectinload, keys, False, {})


@loader_option()
def lazyload(loadopt, attr):
    """Indicate that the given attribute should be loaded using "lazy"
    loading.

    This function is part of the :class:`_orm.Load` interface and supports
    both method-chained and standalone operation.

    .. seealso::

        :ref:`loading_toplevel`

        :ref:`lazy_loading`

    """
    return loadopt.set_relationship_strategy(attr, {"lazy": "select"})


@lazyload._add_unbound_fn
def lazyload(*keys):
    return _UnboundLoad._from_keys(_UnboundLoad.lazyload, keys, False, {})


@loader_option()
def immediateload(loadopt, attr):
    """Indicate that the given attribute should be loaded using
    an immediate load with a per-attribute SELECT statement.

    The load is achieved using the "lazyloader" strategy and does not
    fire off any additional eager loaders.

    The :func:`.immediateload` option is superseded in general
    by the :func:`.selectinload` option, which performs the same task
    more efficiently by emitting a SELECT for all loaded objects.

    This function is part of the :class:`_orm.Load` interface and supports
    both method-chained and standalone operation.

    .. seealso::

        :ref:`loading_toplevel`

        :ref:`selectin_eager_loading`

    """
    loader = loadopt.set_relationship_strategy(attr, {"lazy": "immediate"})
    return loader


@immediateload._add_unbound_fn
def immediateload(*keys):
    return _UnboundLoad._from_keys(_UnboundLoad.immediateload, keys, False, {})


@loader_option()
def noload(loadopt, attr):
    """Indicate that the given relationship attribute should remain unloaded.

    The relationship attribute will return ``None`` when accessed without
    producing any loading effect.

    This function is part of the :class:`_orm.Load` interface and supports
    both method-chained and standalone operation.

    :func:`_orm.noload` applies to :func:`_orm.relationship` attributes; for
    column-based attributes, see :func:`_orm.defer`.

    .. note:: Setting this loading strategy as the default strategy
        for a relationship using the :paramref:`.orm.relationship.lazy`
        parameter may cause issues with flushes, such if a delete operation
        needs to load related objects and instead ``None`` was returned.

    .. seealso::

        :ref:`loading_toplevel`

    """

    return loadopt.set_relationship_strategy(attr, {"lazy": "noload"})


@noload._add_unbound_fn
def noload(*keys):
    return _UnboundLoad._from_keys(_UnboundLoad.noload, keys, False, {})


@loader_option()
def raiseload(loadopt, attr, sql_only=False):
    """Indicate that the given attribute should raise an error if accessed.

    A relationship attribute configured with :func:`_orm.raiseload` will
    raise an :exc:`~sqlalchemy.exc.InvalidRequestError` upon access.   The
    typical way this is useful is when an application is attempting to ensure
    that all relationship attributes that are accessed in a particular context
    would have been already loaded via eager loading.  Instead of having
    to read through SQL logs to ensure lazy loads aren't occurring, this
    strategy will cause them to raise immediately.

    :func:`_orm.raiseload` applies to :func:`_orm.relationship`
    attributes only.
    In order to apply raise-on-SQL behavior to a column-based attribute,
    use the :paramref:`.orm.defer.raiseload` parameter on the :func:`.defer`
    loader option.

    :param sql_only: if True, raise only if the lazy load would emit SQL, but
     not if it is only checking the identity map, or determining that the
     related value should just be None due to missing keys.  When False, the
     strategy will raise for all varieties of relationship loading.

    This function is part of the :class:`_orm.Load` interface and supports
    both method-chained and standalone operation.


    .. versionadded:: 1.1

    .. seealso::

        :ref:`loading_toplevel`

        :ref:`prevent_lazy_with_raiseload`

        :ref:`deferred_raiseload`

    """

    return loadopt.set_relationship_strategy(
        attr, {"lazy": "raise_on_sql" if sql_only else "raise"}
    )


@raiseload._add_unbound_fn
def raiseload(*keys, **kw):
    return _UnboundLoad._from_keys(_UnboundLoad.raiseload, keys, False, kw)


@loader_option()
def defaultload(loadopt, attr):
    """Indicate an attribute should load using its default loader style.

    This method is used to link to other loader options further into
    a chain of attributes without altering the loader style of the links
    along the chain.  For example, to set joined eager loading for an
    element of an element::

        session.query(MyClass).options(
            defaultload(MyClass.someattribute).
            joinedload(MyOtherClass.someotherattribute)
        )

    :func:`.defaultload` is also useful for setting column-level options
    on a related class, namely that of :func:`.defer` and :func:`.undefer`::

        session.query(MyClass).options(
            defaultload(MyClass.someattribute).
            defer("some_column").
            undefer("some_other_column")
        )

    .. seealso::

        :meth:`_orm.Load.options` - allows for complex hierarchical
        loader option structures with less verbosity than with individual
        :func:`.defaultload` directives.

        :ref:`relationship_loader_options`

        :ref:`deferred_loading_w_multiple`

    """
    return loadopt.set_relationship_strategy(attr, None)


@defaultload._add_unbound_fn
def defaultload(*keys):
    return _UnboundLoad._from_keys(_UnboundLoad.defaultload, keys, False, {})


@loader_option()
def defer(loadopt, key, raiseload=False):
    r"""Indicate that the given column-oriented attribute should be deferred,
    e.g. not loaded until accessed.

    This function is part of the :class:`_orm.Load` interface and supports
    both method-chained and standalone operation.

    e.g.::

        from sqlalchemy.orm import defer

        session.query(MyClass).options(
                            defer("attribute_one"),
                            defer("attribute_two"))

        session.query(MyClass).options(
                            defer(MyClass.attribute_one),
                            defer(MyClass.attribute_two))

    To specify a deferred load of an attribute on a related class,
    the path can be specified one token at a time, specifying the loading
    style for each link along the chain.  To leave the loading style
    for a link unchanged, use :func:`_orm.defaultload`::

        session.query(MyClass).options(defaultload("someattr").defer("some_column"))

    A :class:`_orm.Load` object that is present on a certain path can have
    :meth:`_orm.Load.defer` called multiple times,
    each will operate on the same
    parent entity::


        session.query(MyClass).options(
                        defaultload("someattr").
                            defer("some_column").
                            defer("some_other_column").
                            defer("another_column")
            )

    :param key: Attribute to be deferred.

    :param raiseload: raise :class:`.InvalidRequestError` if the column
     value is to be loaded from emitting SQL.   Used to prevent unwanted
     SQL from being emitted.

     .. versionadded:: 1.4

     .. seealso::

        :ref:`deferred_raiseload`

    :param \*addl_attrs: This option supports the old 0.8 style
     of specifying a path as a series of attributes, which is now superseded
     by the method-chained style.

        .. deprecated:: 0.9  The \*addl_attrs on :func:`_orm.defer` is
           deprecated and will be removed in a future release.   Please
           use method chaining in conjunction with defaultload() to
           indicate a path.


    .. seealso::

        :ref:`deferred`

        :func:`_orm.undefer`

    """
    strategy = {"deferred": True, "instrument": True}
    if raiseload:
        strategy["raiseload"] = True
    return loadopt.set_column_strategy((key,), strategy)


@defer._add_unbound_fn
def defer(key, *addl_attrs, **kw):
    if addl_attrs:
        util.warn_deprecated(
            "The *addl_attrs on orm.defer is deprecated.  Please use "
            "method chaining in conjunction with defaultload() to "
            "indicate a path.",
            version="1.3",
        )
    return _UnboundLoad._from_keys(
        _UnboundLoad.defer, (key,) + addl_attrs, False, kw
    )


@loader_option()
def undefer(loadopt, key):
    r"""Indicate that the given column-oriented attribute should be undeferred,
    e.g. specified within the SELECT statement of the entity as a whole.

    The column being undeferred is typically set up on the mapping as a
    :func:`.deferred` attribute.

    This function is part of the :class:`_orm.Load` interface and supports
    both method-chained and standalone operation.

    Examples::

        # undefer two columns
        session.query(MyClass).options(undefer("col1"), undefer("col2"))

        # undefer all columns specific to a single class using Load + *
        session.query(MyClass, MyOtherClass).options(
            Load(MyClass).undefer("*"))

        # undefer a column on a related object
        session.query(MyClass).options(
            defaultload(MyClass.items).undefer('text'))

    :param key: Attribute to be undeferred.

    :param \*addl_attrs: This option supports the old 0.8 style
     of specifying a path as a series of attributes, which is now superseded
     by the method-chained style.

        .. deprecated:: 0.9  The \*addl_attrs on :func:`_orm.undefer` is
           deprecated and will be removed in a future release.   Please
           use method chaining in conjunction with defaultload() to
           indicate a path.

    .. seealso::

        :ref:`deferred`

        :func:`_orm.defer`

        :func:`_orm.undefer_group`

    """
    return loadopt.set_column_strategy(
        (key,), {"deferred": False, "instrument": True}
    )


@undefer._add_unbound_fn
def undefer(key, *addl_attrs):
    if addl_attrs:
        util.warn_deprecated(
            "The *addl_attrs on orm.undefer is deprecated.  Please use "
            "method chaining in conjunction with defaultload() to "
            "indicate a path.",
            version="1.3",
        )
    return _UnboundLoad._from_keys(
        _UnboundLoad.undefer, (key,) + addl_attrs, False, {}
    )


@loader_option()
def undefer_group(loadopt, name):
    """Indicate that columns within the given deferred group name should be
    undeferred.

    The columns being undeferred are set up on the mapping as
    :func:`.deferred` attributes and include a "group" name.

    E.g::

        session.query(MyClass).options(undefer_group("large_attrs"))

    To undefer a group of attributes on a related entity, the path can be
    spelled out using relationship loader options, such as
    :func:`_orm.defaultload`::

        session.query(MyClass).options(
            defaultload("someattr").undefer_group("large_attrs"))

    .. versionchanged:: 0.9.0 :func:`_orm.undefer_group` is now specific to a
       particular entity load path.

    .. seealso::

        :ref:`deferred`

        :func:`_orm.defer`

        :func:`_orm.undefer`

    """
    return loadopt.set_column_strategy(
        "*", None, {"undefer_group_%s" % name: True}, opts_only=True
    )


@undefer_group._add_unbound_fn
def undefer_group(name):
    return _UnboundLoad().undefer_group(name)


@loader_option()
def with_expression(loadopt, key, expression):
    r"""Apply an ad-hoc SQL expression to a "deferred expression" attribute.

    This option is used in conjunction with the :func:`_orm.query_expression`
    mapper-level construct that indicates an attribute which should be the
    target of an ad-hoc SQL expression.

    E.g.::


        sess.query(SomeClass).options(
            with_expression(SomeClass.x_y_expr, SomeClass.x + SomeClass.y)
        )

    .. versionadded:: 1.2

    :param key: Attribute to be undeferred.

    :param expr: SQL expression to be applied to the attribute.

    .. note:: the target attribute is populated only if the target object
       is **not currently loaded** in the current :class:`_orm.Session`
       unless the :meth:`_query.Query.populate_existing` method is used.
       Please refer to :ref:`mapper_querytime_expression` for complete
       usage details.

    .. seealso::

        :ref:`mapper_querytime_expression`

    """

    expression = coercions.expect(
        roles.LabeledColumnExprRole, _orm_full_deannotate(expression)
    )

    return loadopt.set_column_strategy(
        (key,), {"query_expression": True}, opts={"expression": expression}
    )


@with_expression._add_unbound_fn
def with_expression(key, expression):
    return _UnboundLoad._from_keys(
        _UnboundLoad.with_expression, (key,), False, {"expression": expression}
    )


@loader_option()
def selectin_polymorphic(loadopt, classes):
    """Indicate an eager load should take place for all attributes
    specific to a subclass.

    This uses an additional SELECT with IN against all matched primary
    key values, and is the per-query analogue to the ``"selectin"``
    setting on the :paramref:`.mapper.polymorphic_load` parameter.

    .. versionadded:: 1.2

    .. seealso::

        :ref:`polymorphic_selectin`

    """
    loadopt.set_class_strategy(
        {"selectinload_polymorphic": True},
        opts={
            "entities": tuple(
                sorted((inspect(cls) for cls in classes), key=id)
            )
        },
    )
    return loadopt


@selectin_polymorphic._add_unbound_fn
def selectin_polymorphic(base_cls, classes):
    ul = _UnboundLoad()
    ul.is_class_strategy = True
    ul.path = (inspect(base_cls),)
    ul.selectin_polymorphic(classes)
    return ul
