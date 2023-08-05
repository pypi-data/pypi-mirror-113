# sql/elements.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""Core SQL expression elements, including :class:`_expression.ClauseElement`,
:class:`_expression.ColumnElement`, and derived classes.

"""

from __future__ import unicode_literals

import itertools
import operator
import re

from . import coercions
from . import operators
from . import roles
from . import traversals
from . import type_api
from .annotation import Annotated
from .annotation import SupportsWrappingAnnotations
from .base import _clone
from .base import _generative
from .base import Executable
from .base import HasMemoized
from .base import Immutable
from .base import NO_ARG
from .base import PARSE_AUTOCOMMIT
from .base import SingletonConstant
from .coercions import _document_text_coercion
from .traversals import HasCopyInternals
from .traversals import MemoizedHasCacheKey
from .traversals import NO_CACHE
from .visitors import cloned_traverse
from .visitors import InternalTraversal
from .visitors import traverse
from .visitors import Traversible
from .. import exc
from .. import inspection
from .. import util


def collate(expression, collation):
    """Return the clause ``expression COLLATE collation``.

    e.g.::

        collate(mycolumn, 'utf8_bin')

    produces::

        mycolumn COLLATE utf8_bin

    The collation expression is also quoted if it is a case sensitive
    identifier, e.g. contains uppercase characters.

    .. versionchanged:: 1.2 quoting is automatically applied to COLLATE
       expressions if they are case sensitive.

    """

    expr = coercions.expect(roles.ExpressionElementRole, expression)
    return BinaryExpression(
        expr, CollationClause(collation), operators.collate, type_=expr.type
    )


def between(expr, lower_bound, upper_bound, symmetric=False):
    """Produce a ``BETWEEN`` predicate clause.

    E.g.::

        from sqlalchemy import between
        stmt = select(users_table).where(between(users_table.c.id, 5, 7))

    Would produce SQL resembling::

        SELECT id, name FROM user WHERE id BETWEEN :id_1 AND :id_2

    The :func:`.between` function is a standalone version of the
    :meth:`_expression.ColumnElement.between` method available on all
    SQL expressions, as in::

        stmt = select(users_table).where(users_table.c.id.between(5, 7))

    All arguments passed to :func:`.between`, including the left side
    column expression, are coerced from Python scalar values if a
    the value is not a :class:`_expression.ColumnElement` subclass.
    For example,
    three fixed values can be compared as in::

        print(between(5, 3, 7))

    Which would produce::

        :param_1 BETWEEN :param_2 AND :param_3

    :param expr: a column expression, typically a
     :class:`_expression.ColumnElement`
     instance or alternatively a Python scalar expression to be coerced
     into a column expression, serving as the left side of the ``BETWEEN``
     expression.

    :param lower_bound: a column or Python scalar expression serving as the
     lower bound of the right side of the ``BETWEEN`` expression.

    :param upper_bound: a column or Python scalar expression serving as the
     upper bound of the right side of the ``BETWEEN`` expression.

    :param symmetric: if True, will render " BETWEEN SYMMETRIC ". Note
     that not all databases support this syntax.

     .. versionadded:: 0.9.5

    .. seealso::

        :meth:`_expression.ColumnElement.between`

    """
    expr = coercions.expect(roles.ExpressionElementRole, expr)
    return expr.between(lower_bound, upper_bound, symmetric=symmetric)


def literal(value, type_=None):
    r"""Return a literal clause, bound to a bind parameter.

    Literal clauses are created automatically when non-
    :class:`_expression.ClauseElement` objects (such as strings, ints, dates,
    etc.) are
    used in a comparison operation with a :class:`_expression.ColumnElement`
    subclass,
    such as a :class:`~sqlalchemy.schema.Column` object.  Use this function
    to force the generation of a literal clause, which will be created as a
    :class:`BindParameter` with a bound value.

    :param value: the value to be bound. Can be any Python object supported by
        the underlying DB-API, or is translatable via the given type argument.

    :param type\_: an optional :class:`~sqlalchemy.types.TypeEngine` which
        will provide bind-parameter translation for this literal.

    """
    return coercions.expect(roles.LiteralValueRole, value, type_=type_)


def outparam(key, type_=None):
    """Create an 'OUT' parameter for usage in functions (stored procedures),
    for databases which support them.

    The ``outparam`` can be used like a regular function parameter.
    The "output" value will be available from the
    :class:`~sqlalchemy.engine.CursorResult` object via its ``out_parameters``
    attribute, which returns a dictionary containing the values.

    """
    return BindParameter(key, None, type_=type_, unique=False, isoutparam=True)


def not_(clause):
    """Return a negation of the given clause, i.e. ``NOT(clause)``.

    The ``~`` operator is also overloaded on all
    :class:`_expression.ColumnElement` subclasses to produce the
    same result.

    """
    return operators.inv(coercions.expect(roles.ExpressionElementRole, clause))


@inspection._self_inspects
class ClauseElement(
    roles.SQLRole,
    SupportsWrappingAnnotations,
    MemoizedHasCacheKey,
    HasCopyInternals,
    Traversible,
):
    """Base class for elements of a programmatically constructed SQL
    expression.

    """

    __visit_name__ = "clause"

    _propagate_attrs = util.immutabledict()
    """like annotations, however these propagate outwards liberally
    as SQL constructs are built, and are set up at construction time.

    """

    supports_execution = False

    stringify_dialect = "default"

    _from_objects = []
    bind = None
    description = None
    _is_clone_of = None

    is_clause_element = True
    is_selectable = False

    _is_textual = False
    _is_from_clause = False
    _is_returns_rows = False
    _is_text_clause = False
    _is_from_container = False
    _is_select_container = False
    _is_select_statement = False
    _is_bind_parameter = False
    _is_clause_list = False
    _is_lambda_element = False

    _order_by_label_element = None

    _cache_key_traversal = None

    def _set_propagate_attrs(self, values):
        # usually, self._propagate_attrs is empty here.  one case where it's
        # not is a subquery against ORM select, that is then pulled as a
        # property of an aliased class.   should all be good

        # assert not self._propagate_attrs

        self._propagate_attrs = util.immutabledict(values)
        return self

    def _clone(self, **kw):
        """Create a shallow copy of this ClauseElement.

        This method may be used by a generative API.  Its also used as
        part of the "deep" copy afforded by a traversal that combines
        the _copy_internals() method.

        """
        skip = self._memoized_keys
        c = self.__class__.__new__(self.__class__)
        c.__dict__ = {k: v for k, v in self.__dict__.items() if k not in skip}

        # this is a marker that helps to "equate" clauses to each other
        # when a Select returns its list of FROM clauses.  the cloning
        # process leaves around a lot of remnants of the previous clause
        # typically in the form of column expressions still attached to the
        # old table.
        c._is_clone_of = self

        return c

    def _negate_in_binary(self, negated_op, original_op):
        """a hook to allow the right side of a binary expression to respond
        to a negation of the binary expression.

        Used for the special case of expanding bind parameter with IN.

        """
        return self

    def _with_binary_element_type(self, type_):
        """in the context of binary expression, convert the type of this
        object to the one given.

        applies only to :class:`_expression.ColumnElement` classes.

        """
        return self

    @property
    def _constructor(self):
        """return the 'constructor' for this ClauseElement.

        This is for the purposes for creating a new object of
        this type.   Usually, its just the element's __class__.
        However, the "Annotated" version of the object overrides
        to return the class of its proxied element.

        """
        return self.__class__

    @HasMemoized.memoized_attribute
    def _cloned_set(self):
        """Return the set consisting all cloned ancestors of this
        ClauseElement.

        Includes this ClauseElement.  This accessor tends to be used for
        FromClause objects to identify 'equivalent' FROM clauses, regardless
        of transformative operations.

        """
        s = util.column_set()
        f = self

        # note this creates a cycle, asserted in test_memusage. however,
        # turning this into a plain @property adds tends of thousands of method
        # calls to Core / ORM performance tests, so the small overhead
        # introduced by the relatively small amount of short term cycles
        # produced here is preferable
        while f is not None:
            s.add(f)
            f = f._is_clone_of
        return s

    @property
    def entity_namespace(self):
        raise AttributeError(
            "This SQL expression has no entity namespace "
            "with which to filter from."
        )

    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop("_is_clone_of", None)
        d.pop("_generate_cache_key", None)
        return d

    def _execute_on_connection(
        self, connection, multiparams, params, execution_options, _force=False
    ):
        if _force or self.supports_execution:
            return connection._execute_clauseelement(
                self, multiparams, params, execution_options
            )
        else:
            raise exc.ObjectNotExecutableError(self)

    def unique_params(self, *optionaldict, **kwargs):
        """Return a copy with :func:`_expression.bindparam` elements
        replaced.

        Same functionality as :meth:`_expression.ClauseElement.params`,
        except adds `unique=True`
        to affected bind parameters so that multiple statements can be
        used.

        """
        return self._replace_params(True, optionaldict, kwargs)

    def params(self, *optionaldict, **kwargs):
        """Return a copy with :func:`_expression.bindparam` elements
        replaced.

        Returns a copy of this ClauseElement with
        :func:`_expression.bindparam`
        elements replaced with values taken from the given dictionary::

          >>> clause = column('x') + bindparam('foo')
          >>> print(clause.compile().params)
          {'foo':None}
          >>> print(clause.params({'foo':7}).compile().params)
          {'foo':7}

        """
        return self._replace_params(False, optionaldict, kwargs)

    def _replace_params(self, unique, optionaldict, kwargs):
        if len(optionaldict) == 1:
            kwargs.update(optionaldict[0])
        elif len(optionaldict) > 1:
            raise exc.ArgumentError(
                "params() takes zero or one positional dictionary argument"
            )

        def visit_bindparam(bind):
            if bind.key in kwargs:
                bind.value = kwargs[bind.key]
                bind.required = False
            if unique:
                bind._convert_to_unique()

        return cloned_traverse(
            self, {"maintain_key": True}, {"bindparam": visit_bindparam}
        )

    def compare(self, other, **kw):
        r"""Compare this :class:`_expression.ClauseElement` to
        the given :class:`_expression.ClauseElement`.

        Subclasses should override the default behavior, which is a
        straight identity comparison.

        \**kw are arguments consumed by subclass ``compare()`` methods and
        may be used to modify the criteria for comparison
        (see :class:`_expression.ColumnElement`).

        """
        return traversals.compare(self, other, **kw)

    def self_group(self, against=None):
        """Apply a 'grouping' to this :class:`_expression.ClauseElement`.

        This method is overridden by subclasses to return a "grouping"
        construct, i.e. parenthesis.   In particular it's used by "binary"
        expressions to provide a grouping around themselves when placed into a
        larger expression, as well as by :func:`_expression.select`
        constructs when placed into the FROM clause of another
        :func:`_expression.select`.  (Note that subqueries should be
        normally created using the :meth:`_expression.Select.alias` method,
        as many
        platforms require nested SELECT statements to be named).

        As expressions are composed together, the application of
        :meth:`self_group` is automatic - end-user code should never
        need to use this method directly.  Note that SQLAlchemy's
        clause constructs take operator precedence into account -
        so parenthesis might not be needed, for example, in
        an expression like ``x OR (y AND z)`` - AND takes precedence
        over OR.

        The base :meth:`self_group` method of
        :class:`_expression.ClauseElement`
        just returns self.
        """
        return self

    def _ungroup(self):
        """Return this :class:`_expression.ClauseElement`
        without any groupings.
        """

        return self

    @util.preload_module("sqlalchemy.engine.default")
    @util.preload_module("sqlalchemy.engine.url")
    def compile(self, bind=None, dialect=None, **kw):
        """Compile this SQL expression.

        The return value is a :class:`~.Compiled` object.
        Calling ``str()`` or ``unicode()`` on the returned value will yield a
        string representation of the result. The
        :class:`~.Compiled` object also can return a
        dictionary of bind parameter names and values
        using the ``params`` accessor.

        :param bind: An ``Engine`` or ``Connection`` from which a
            ``Compiled`` will be acquired. This argument takes precedence over
            this :class:`_expression.ClauseElement`'s bound engine, if any.

        :param column_keys: Used for INSERT and UPDATE statements, a list of
            column names which should be present in the VALUES clause of the
            compiled statement. If ``None``, all columns from the target table
            object are rendered.

        :param dialect: A ``Dialect`` instance from which a ``Compiled``
            will be acquired. This argument takes precedence over the `bind`
            argument as well as this :class:`_expression.ClauseElement`
            's bound engine,
            if any.

        :param compile_kwargs: optional dictionary of additional parameters
            that will be passed through to the compiler within all "visit"
            methods.  This allows any custom flag to be passed through to
            a custom compilation construct, for example.  It is also used
            for the case of passing the ``literal_binds`` flag through::

                from sqlalchemy.sql import table, column, select

                t = table('t', column('x'))

                s = select(t).where(t.c.x == 5)

                print(s.compile(compile_kwargs={"literal_binds": True}))

            .. versionadded:: 0.9.0

        .. seealso::

            :ref:`faq_sql_expression_string`

        """

        if not dialect:
            if bind:
                dialect = bind.dialect
            elif self.bind:
                dialect = self.bind.dialect
            else:
                if self.stringify_dialect == "default":
                    default = util.preloaded.engine_default
                    dialect = default.StrCompileDialect()
                else:
                    url = util.preloaded.engine_url
                    dialect = url.URL.create(
                        self.stringify_dialect
                    ).get_dialect()()

        return self._compiler(dialect, **kw)

    def _compile_w_cache(
        self,
        dialect,
        compiled_cache=None,
        column_keys=None,
        for_executemany=False,
        schema_translate_map=None,
        **kw
    ):
        if compiled_cache is not None and dialect._supports_statement_cache:
            elem_cache_key = self._generate_cache_key()
        else:
            elem_cache_key = None

        if elem_cache_key:
            cache_key, extracted_params = elem_cache_key
            key = (
                dialect,
                cache_key,
                tuple(column_keys),
                bool(schema_translate_map),
                for_executemany,
            )
            compiled_sql = compiled_cache.get(key)

            if compiled_sql is None:
                cache_hit = dialect.CACHE_MISS
                compiled_sql = self._compiler(
                    dialect,
                    cache_key=elem_cache_key,
                    column_keys=column_keys,
                    for_executemany=for_executemany,
                    schema_translate_map=schema_translate_map,
                    **kw
                )
                compiled_cache[key] = compiled_sql
            else:
                cache_hit = dialect.CACHE_HIT
        else:
            extracted_params = None
            compiled_sql = self._compiler(
                dialect,
                cache_key=elem_cache_key,
                column_keys=column_keys,
                for_executemany=for_executemany,
                schema_translate_map=schema_translate_map,
                **kw
            )

            if not dialect._supports_statement_cache:
                cache_hit = dialect.NO_DIALECT_SUPPORT
            elif compiled_cache is None:
                cache_hit = dialect.CACHING_DISABLED
            else:
                cache_hit = dialect.NO_CACHE_KEY

        return compiled_sql, extracted_params, cache_hit

    def _compiler(self, dialect, **kw):
        """Return a compiler appropriate for this ClauseElement, given a
        Dialect."""

        return dialect.statement_compiler(dialect, self, **kw)

    def __str__(self):
        if util.py3k:
            return str(self.compile())
        else:
            return unicode(self.compile()).encode(  # noqa
                "ascii", "backslashreplace"
            )  # noqa

    def __invert__(self):
        # undocumented element currently used by the ORM for
        # relationship.contains()
        if hasattr(self, "negation_clause"):
            return self.negation_clause
        else:
            return self._negate()

    def _negate(self):
        return UnaryExpression(
            self.self_group(against=operators.inv), operator=operators.inv
        )

    def __bool__(self):
        raise TypeError("Boolean value of this clause is not defined")

    __nonzero__ = __bool__

    def __repr__(self):
        friendly = self.description
        if friendly is None:
            return object.__repr__(self)
        else:
            return "<%s.%s at 0x%x; %s>" % (
                self.__module__,
                self.__class__.__name__,
                id(self),
                friendly,
            )


class ColumnElement(
    roles.ColumnArgumentOrKeyRole,
    roles.StatementOptionRole,
    roles.WhereHavingRole,
    roles.BinaryElementRole,
    roles.OrderByRole,
    roles.ColumnsClauseRole,
    roles.LimitOffsetRole,
    roles.DMLColumnRole,
    roles.DDLConstraintColumnRole,
    roles.DDLExpressionRole,
    operators.ColumnOperators,
    ClauseElement,
):
    """Represent a column-oriented SQL expression suitable for usage in the
    "columns" clause, WHERE clause etc. of a statement.

    While the most familiar kind of :class:`_expression.ColumnElement` is the
    :class:`_schema.Column` object, :class:`_expression.ColumnElement`
    serves as the basis
    for any unit that may be present in a SQL expression, including
    the expressions themselves, SQL functions, bound parameters,
    literal expressions, keywords such as ``NULL``, etc.
    :class:`_expression.ColumnElement`
    is the ultimate base class for all such elements.

    A wide variety of SQLAlchemy Core functions work at the SQL expression
    level, and are intended to accept instances of
    :class:`_expression.ColumnElement` as
    arguments.  These functions will typically document that they accept a
    "SQL expression" as an argument.  What this means in terms of SQLAlchemy
    usually refers to an input which is either already in the form of a
    :class:`_expression.ColumnElement` object,
    or a value which can be **coerced** into
    one.  The coercion rules followed by most, but not all, SQLAlchemy Core
    functions with regards to SQL expressions are as follows:

        * a literal Python value, such as a string, integer or floating
          point value, boolean, datetime, ``Decimal`` object, or virtually
          any other Python object, will be coerced into a "literal bound
          value".  This generally means that a :func:`.bindparam` will be
          produced featuring the given value embedded into the construct; the
          resulting :class:`.BindParameter` object is an instance of
          :class:`_expression.ColumnElement`.
          The Python value will ultimately be sent
          to the DBAPI at execution time as a parameterized argument to the
          ``execute()`` or ``executemany()`` methods, after SQLAlchemy
          type-specific converters (e.g. those provided by any associated
          :class:`.TypeEngine` objects) are applied to the value.

        * any special object value, typically ORM-level constructs, which
          feature an accessor called ``__clause_element__()``.  The Core
          expression system looks for this method when an object of otherwise
          unknown type is passed to a function that is looking to coerce the
          argument into a :class:`_expression.ColumnElement` and sometimes a
          :class:`_expression.SelectBase` expression.
          It is used within the ORM to
          convert from ORM-specific objects like mapped classes and
          mapped attributes into Core expression objects.

        * The Python ``None`` value is typically interpreted as ``NULL``,
          which in SQLAlchemy Core produces an instance of :func:`.null`.

    A :class:`_expression.ColumnElement` provides the ability to generate new
    :class:`_expression.ColumnElement`
    objects using Python expressions.  This means that Python operators
    such as ``==``, ``!=`` and ``<`` are overloaded to mimic SQL operations,
    and allow the instantiation of further :class:`_expression.ColumnElement`
    instances
    which are composed from other, more fundamental
    :class:`_expression.ColumnElement`
    objects.  For example, two :class:`.ColumnClause` objects can be added
    together with the addition operator ``+`` to produce
    a :class:`.BinaryExpression`.
    Both :class:`.ColumnClause` and :class:`.BinaryExpression` are subclasses
    of :class:`_expression.ColumnElement`::

        >>> from sqlalchemy.sql import column
        >>> column('a') + column('b')
        <sqlalchemy.sql.expression.BinaryExpression object at 0x101029dd0>
        >>> print(column('a') + column('b'))
        a + b

    .. seealso::

        :class:`_schema.Column`

        :func:`_expression.column`

    """

    __visit_name__ = "column_element"
    primary_key = False
    foreign_keys = []
    _proxies = ()

    _tq_label = None
    """The named label that can be used to target
    this column in a result set in a "table qualified" context.

    This label is almost always the label used when
    rendering <expr> AS <label> in a SELECT statement when using
    the LABEL_STYLE_TABLENAME_PLUS_COL label style, which is what the legacy
    ORM ``Query`` object uses as well.

    For a regular Column bound to a Table, this is typically the label
    <tablename>_<columnname>.  For other constructs, different rules
    may apply, such as anonymized labels and others.

    .. versionchanged:: 1.4.21 renamed from ``._label``

    """

    key = None
    """The 'key' that in some circumstances refers to this object in a
    Python namespace.

    This typically refers to the "key" of the column as present in the
    ``.c`` collection of a selectable, e.g. ``sometable.c["somekey"]`` would
    return a :class:`_schema.Column` with a ``.key`` of "somekey".

    """

    @HasMemoized.memoized_attribute
    def _tq_key_label(self):
        """A label-based version of 'key' that in some circumstances refers
        to this object in a Python namespace.


        _tq_key_label comes into play when a select() statement is constructed
        with apply_labels(); in this case, all Column objects in the ``.c``
        collection are rendered as <tablename>_<columnname> in SQL; this is
        essentially the value of ._label. But to locate those columns in the
        ``.c`` collection, the name is along the lines of <tablename>_<key>;
        that's the typical value of .key_label.

        .. versionchanged:: 1.4.21 renamed from ``._key_label``

        """
        return self._proxy_key

    @property
    def _key_label(self):
        """legacy; renamed to _tq_key_label"""
        return self._tq_key_label

    @property
    def _label(self):
        """legacy; renamed to _tq_label"""
        return self._tq_label

    @property
    def _non_anon_label(self):
        """the 'name' that naturally applies this element when rendered in
        SQL.

        Concretely, this is the "name" of a column or a label in a
        SELECT statement; ``<columnname>`` and ``<labelname>`` below::

            SELECT <columnmame> FROM table

            SELECT column AS <labelname> FROM table

        Above, the two names noted will be what's present in the DBAPI
        ``cursor.description`` as the names.

        If this attribute returns ``None``, it means that the SQL element as
        written does not have a 100% fully predictable "name" that would appear
        in the ``cursor.description``. Examples include SQL functions, CAST
        functions, etc. While such things do return names in
        ``cursor.description``, they are only predictable on a
        database-specific basis; e.g. an expression like ``MAX(table.col)`` may
        appear as the string ``max`` on one database (like PostgreSQL) or may
        appear as the whole expression ``max(table.col)`` on SQLite.

        The default implementation looks for a ``.name`` attribute on the
        object, as has been the precedent established in SQLAlchemy for many
        years.  An exception is made on the ``FunctionElement`` subclass
        so that the return value is always ``None``.

        .. versionadded:: 1.4.21



        """
        return getattr(self, "name", None)

    _render_label_in_columns_clause = True
    """A flag used by select._columns_plus_names that helps to determine
    we are actually going to render in terms of "SELECT <col> AS <label>".
    This flag can be returned as False for some Column objects that want
    to be rendered as simple "SELECT <col>"; typically columns that don't have
    any parent table and are named the same as what the label would be
    in any case.

    """

    _resolve_label = None
    """The name that should be used to identify this ColumnElement in a
    select() object when "label resolution" logic is used; this refers
    to using a string name in an expression like order_by() or group_by()
    that wishes to target a labeled expression in the columns clause.

    The name is distinct from that of .name or ._label to account for the case
    where anonymizing logic may be used to change the name that's actually
    rendered at compile time; this attribute should hold onto the original
    name that was user-assigned when producing a .label() construct.

    """

    _allow_label_resolve = True
    """A flag that can be flipped to prevent a column from being resolvable
    by string label name."""

    _is_implicitly_boolean = False

    _alt_names = ()

    def self_group(self, against=None):
        if (
            against in (operators.and_, operators.or_, operators._asbool)
            and self.type._type_affinity is type_api.BOOLEANTYPE._type_affinity
        ):
            return AsBoolean(self, operators.is_true, operators.is_false)
        elif against in (operators.any_op, operators.all_op):
            return Grouping(self)
        else:
            return self

    def _negate(self):
        if self.type._type_affinity is type_api.BOOLEANTYPE._type_affinity:
            return AsBoolean(self, operators.is_false, operators.is_true)
        else:
            return super(ColumnElement, self)._negate()

    @util.memoized_property
    def type(self):
        return type_api.NULLTYPE

    @HasMemoized.memoized_attribute
    def comparator(self):
        try:
            comparator_factory = self.type.comparator_factory
        except AttributeError as err:
            util.raise_(
                TypeError(
                    "Object %r associated with '.type' attribute "
                    "is not a TypeEngine class or object" % self.type
                ),
                replace_context=err,
            )
        else:
            return comparator_factory(self)

    def __getattr__(self, key):
        try:
            return getattr(self.comparator, key)
        except AttributeError as err:
            util.raise_(
                AttributeError(
                    "Neither %r object nor %r object has an attribute %r"
                    % (
                        type(self).__name__,
                        type(self.comparator).__name__,
                        key,
                    )
                ),
                replace_context=err,
            )

    def operate(self, op, *other, **kwargs):
        return op(self.comparator, *other, **kwargs)

    def reverse_operate(self, op, other, **kwargs):
        return op(other, self.comparator, **kwargs)

    def _bind_param(self, operator, obj, type_=None, expanding=False):
        return BindParameter(
            None,
            obj,
            _compared_to_operator=operator,
            type_=type_,
            _compared_to_type=self.type,
            unique=True,
            expanding=expanding,
        )

    @property
    def expression(self):
        """Return a column expression.

        Part of the inspection interface; returns self.

        """
        return self

    @property
    def _select_iterable(self):
        return (self,)

    @util.memoized_property
    def base_columns(self):
        return util.column_set(c for c in self.proxy_set if not c._proxies)

    @util.memoized_property
    def proxy_set(self):
        s = util.column_set([self])
        for c in self._proxies:
            s.update(c.proxy_set)
        return s

    def _uncached_proxy_set(self):
        """An 'uncached' version of proxy set.

        This is so that we can read annotations from the list of columns
        without breaking the caching of the above proxy_set.

        """
        s = util.column_set([self])
        for c in self._proxies:
            s.update(c._uncached_proxy_set())
        return s

    def shares_lineage(self, othercolumn):
        """Return True if the given :class:`_expression.ColumnElement`
        has a common ancestor to this :class:`_expression.ColumnElement`."""

        return bool(self.proxy_set.intersection(othercolumn.proxy_set))

    def _compare_name_for_result(self, other):
        """Return True if the given column element compares to this one
        when targeting within a result row."""

        return (
            hasattr(other, "name")
            and hasattr(self, "name")
            and other.name == self.name
        )

    @HasMemoized.memoized_attribute
    def _proxy_key(self):
        if self._annotations and "proxy_key" in self._annotations:
            return self._annotations["proxy_key"]

        name = self.key
        if not name:
            # there's a bit of a seeming contradiction which is that the
            # "_non_anon_label" of a column can in fact be an
            # "_anonymous_label"; this is when it's on a column that is
            # proxying for an anonymous expression in a subquery.
            name = self._non_anon_label

        if isinstance(name, _anonymous_label):
            return None
        else:
            return name

    @HasMemoized.memoized_attribute
    def _expression_label(self):
        """a suggested label to use in the case that the column has no name,
        which should be used if possible as the explicit 'AS <label>'
        where this expression would normally have an anon label.

        this is essentially mostly what _proxy_key does except it returns
        None if the column has a normal name that can be used.

        """

        if getattr(self, "name", None) is not None:
            return None
        elif self._annotations and "proxy_key" in self._annotations:
            return self._annotations["proxy_key"]
        else:
            return None

    def _make_proxy(
        self, selectable, name=None, key=None, name_is_truncatable=False, **kw
    ):
        """Create a new :class:`_expression.ColumnElement` representing this
        :class:`_expression.ColumnElement` as it appears in the select list of
        a descending selectable.

        """
        if name is None:
            name = self._anon_name_label
            if key is None:
                key = self._proxy_key
        else:
            key = name

        co = ColumnClause(
            coercions.expect(roles.TruncatedLabelRole, name)
            if name_is_truncatable
            else name,
            type_=getattr(self, "type", None),
            _selectable=selectable,
        )

        co._propagate_attrs = selectable._propagate_attrs
        co._proxies = [self]
        if selectable._is_clone_of is not None:
            co._is_clone_of = selectable._is_clone_of.columns.get(key)
        return key, co

    def cast(self, type_):
        """Produce a type cast, i.e. ``CAST(<expression> AS <type>)``.

        This is a shortcut to the :func:`_expression.cast` function.

        .. seealso::

            :ref:`coretutorial_casts`

            :func:`_expression.cast`

            :func:`_expression.type_coerce`

        .. versionadded:: 1.0.7

        """
        return Cast(self, type_)

    def label(self, name):
        """Produce a column label, i.e. ``<columnname> AS <name>``.

        This is a shortcut to the :func:`_expression.label` function.

        If 'name' is ``None``, an anonymous label name will be generated.

        """
        return Label(name, self, self.type)

    def _anon_label(self, seed):
        while self._is_clone_of is not None:
            self = self._is_clone_of

        # as of 1.4 anonymous label for ColumnElement uses hash(), not id(),
        # as the identifier, because a column and its annotated version are
        # the same thing in a SQL statement
        if isinstance(seed, _anonymous_label):
            return _anonymous_label.safe_construct(
                hash(self), "", enclosing_label=seed
            )

        return _anonymous_label.safe_construct(hash(self), seed or "anon")

    @util.memoized_property
    def _anon_name_label(self):
        """Provides a constant 'anonymous label' for this ColumnElement.

        This is a label() expression which will be named at compile time.
        The same label() is returned each time ``anon_label`` is called so
        that expressions can reference ``anon_label`` multiple times,
        producing the same label name at compile time.

        The compiler uses this function automatically at compile time
        for expressions that are known to be 'unnamed' like binary
        expressions and function calls.

        .. versionchanged:: 1.4.9 - this attribute was not intended to be
           public and is renamed to _anon_name_label.  anon_name exists
           for backwards compat

        """
        name = getattr(self, "name", None)
        return self._anon_label(name)

    @util.memoized_property
    def _anon_key_label(self):
        """Provides a constant 'anonymous key label' for this ColumnElement.

        Compare to ``anon_label``, except that the "key" of the column,
        if available, is used to generate the label.

        This is used when a deduplicating key is placed into the columns
        collection of a selectable.

        .. versionchanged:: 1.4.9 - this attribute was not intended to be
           public and is renamed to _anon_key_label.  anon_key_label exists
           for backwards compat

        """
        return self._anon_label(self._proxy_key)

    @property
    @util.deprecated(
        "1.4",
        "The :attr:`_expression.ColumnElement.anon_label` attribute is now "
        "private, and the public accessor is deprecated.",
    )
    def anon_label(self):
        return self._anon_name_label

    @property
    @util.deprecated(
        "1.4",
        "The :attr:`_expression.ColumnElement.anon_key_label` attribute is "
        "now private, and the public accessor is deprecated.",
    )
    def anon_key_label(self):
        return self._anon_key_label

    @util.memoized_property
    def _dedupe_anon_label(self):
        """label to apply to a column that is anon labeled, but repeated
        in the SELECT, so that we have to make an "extra anon" label that
        disambiguates it from the previous appearance.

        these labels come out like "foo_bar_id__1" and have double underscores
        in them.

        """
        label = getattr(self, "name", None)

        # current convention is that if the element doesn't have a
        # ".name" (usually because it is not NamedColumn), we try to
        # use a "table qualified" form for the "dedupe anon" label,
        # based on the notion that a label like
        # "CAST(casttest.v1 AS DECIMAL) AS casttest_v1__1" looks better than
        # "CAST(casttest.v1 AS DECIMAL) AS anon__1"

        if label is None:
            return self._dedupe_anon_tq_label
        else:
            return self._anon_label(label + "_")

    @util.memoized_property
    def _anon_tq_label(self):
        return self._anon_label(getattr(self, "_tq_label", None))

    @util.memoized_property
    def _anon_tq_key_label(self):
        return self._anon_label(getattr(self, "_tq_key_label", None))

    @util.memoized_property
    def _dedupe_anon_tq_label(self):
        label = getattr(self, "_tq_label", None) or "anon"
        return self._anon_label(label + "_")


class WrapsColumnExpression(object):
    """Mixin that defines a :class:`_expression.ColumnElement`
    as a wrapper with special
    labeling behavior for an expression that already has a name.

    .. versionadded:: 1.4

    .. seealso::

        :ref:`change_4449`


    """

    @property
    def wrapped_column_expression(self):
        raise NotImplementedError()

    @property
    def _tq_label(self):
        wce = self.wrapped_column_expression
        if hasattr(wce, "_tq_label"):
            return wce._tq_label
        else:
            return None

    _label = _tq_label

    @property
    def _non_anon_label(self):
        return None

    @property
    def _anon_name_label(self):
        wce = self.wrapped_column_expression

        # this logic tries to get the WrappedColumnExpression to render
        # with "<expr> AS <name>", where "<name>" is the natural name
        # within the expression itself.   e.g. "CAST(table.foo) AS foo".
        if not wce._is_text_clause:
            nal = wce._non_anon_label
            if nal:
                return nal
            elif hasattr(wce, "_anon_name_label"):
                return wce._anon_name_label
        return super(WrapsColumnExpression, self)._anon_name_label

    @property
    def _dedupe_anon_label(self):
        wce = self.wrapped_column_expression
        nal = wce._non_anon_label
        if nal:
            return self._anon_label(nal + "_")
        else:
            return self._dedupe_anon_tq_label


class BindParameter(roles.InElementRole, ColumnElement):
    r"""Represent a "bound expression".

    :class:`.BindParameter` is invoked explicitly using the
    :func:`.bindparam` function, as in::

        from sqlalchemy import bindparam

        stmt = select(users_table).\
                    where(users_table.c.name == bindparam('username'))

    Detailed discussion of how :class:`.BindParameter` is used is
    at :func:`.bindparam`.

    .. seealso::

        :func:`.bindparam`

    """

    __visit_name__ = "bindparam"

    _traverse_internals = [
        ("key", InternalTraversal.dp_anon_name),
        ("type", InternalTraversal.dp_type),
        ("callable", InternalTraversal.dp_plain_dict),
        ("value", InternalTraversal.dp_plain_obj),
    ]

    _is_crud = False
    _is_bind_parameter = True
    _key_is_anon = False

    # bindparam implements its own _gen_cache_key() method however
    # we check subclasses for this flag, else no cache key is generated
    inherit_cache = True

    def __init__(
        self,
        key,
        value=NO_ARG,
        type_=None,
        unique=False,
        required=NO_ARG,
        quote=None,
        callable_=None,
        expanding=False,
        isoutparam=False,
        literal_execute=False,
        _compared_to_operator=None,
        _compared_to_type=None,
        _is_crud=False,
    ):
        r"""Produce a "bound expression".

        The return value is an instance of :class:`.BindParameter`; this
        is a :class:`_expression.ColumnElement`
        subclass which represents a so-called
        "placeholder" value in a SQL expression, the value of which is
        supplied at the point at which the statement in executed against a
        database connection.

        In SQLAlchemy, the :func:`.bindparam` construct has
        the ability to carry along the actual value that will be ultimately
        used at expression time.  In this way, it serves not just as
        a "placeholder" for eventual population, but also as a means of
        representing so-called "unsafe" values which should not be rendered
        directly in a SQL statement, but rather should be passed along
        to the :term:`DBAPI` as values which need to be correctly escaped
        and potentially handled for type-safety.

        When using :func:`.bindparam` explicitly, the use case is typically
        one of traditional deferment of parameters; the :func:`.bindparam`
        construct accepts a name which can then be referred to at execution
        time::

            from sqlalchemy import bindparam

            stmt = select(users_table).\
                        where(users_table.c.name == bindparam('username'))

        The above statement, when rendered, will produce SQL similar to::

            SELECT id, name FROM user WHERE name = :username

        In order to populate the value of ``:username`` above, the value
        would typically be applied at execution time to a method
        like :meth:`_engine.Connection.execute`::

            result = connection.execute(stmt, username='wendy')

        Explicit use of :func:`.bindparam` is also common when producing
        UPDATE or DELETE statements that are to be invoked multiple times,
        where the WHERE criterion of the statement is to change on each
        invocation, such as::

            stmt = (users_table.update().
                    where(user_table.c.name == bindparam('username')).
                    values(fullname=bindparam('fullname'))
                    )

            connection.execute(
                stmt, [{"username": "wendy", "fullname": "Wendy Smith"},
                       {"username": "jack", "fullname": "Jack Jones"},
                       ]
            )

        SQLAlchemy's Core expression system makes wide use of
        :func:`.bindparam` in an implicit sense.   It is typical that Python
        literal values passed to virtually all SQL expression functions are
        coerced into fixed :func:`.bindparam` constructs.  For example, given
        a comparison operation such as::

            expr = users_table.c.name == 'Wendy'

        The above expression will produce a :class:`.BinaryExpression`
        construct, where the left side is the :class:`_schema.Column` object
        representing the ``name`` column, and the right side is a
        :class:`.BindParameter` representing the literal value::

            print(repr(expr.right))
            BindParameter('%(4327771088 name)s', 'Wendy', type_=String())

        The expression above will render SQL such as::

            user.name = :name_1

        Where the ``:name_1`` parameter name is an anonymous name.  The
        actual string ``Wendy`` is not in the rendered string, but is carried
        along where it is later used within statement execution.  If we
        invoke a statement like the following::

            stmt = select(users_table).where(users_table.c.name == 'Wendy')
            result = connection.execute(stmt)

        We would see SQL logging output as::

            SELECT "user".id, "user".name
            FROM "user"
            WHERE "user".name = %(name_1)s
            {'name_1': 'Wendy'}

        Above, we see that ``Wendy`` is passed as a parameter to the database,
        while the placeholder ``:name_1`` is rendered in the appropriate form
        for the target database, in this case the PostgreSQL database.

        Similarly, :func:`.bindparam` is invoked automatically when working
        with :term:`CRUD` statements as far as the "VALUES" portion is
        concerned.   The :func:`_expression.insert` construct produces an
        ``INSERT`` expression which will, at statement execution time, generate
        bound placeholders based on the arguments passed, as in::

            stmt = users_table.insert()
            result = connection.execute(stmt, name='Wendy')

        The above will produce SQL output as::

            INSERT INTO "user" (name) VALUES (%(name)s)
            {'name': 'Wendy'}

        The :class:`_expression.Insert` construct, at
        compilation/execution time, rendered a single :func:`.bindparam`
        mirroring the column name ``name`` as a result of the single ``name``
        parameter we passed to the :meth:`_engine.Connection.execute` method.

        :param key:
          the key (e.g. the name) for this bind param.
          Will be used in the generated
          SQL statement for dialects that use named parameters.  This
          value may be modified when part of a compilation operation,
          if other :class:`BindParameter` objects exist with the same
          key, or if its length is too long and truncation is
          required.

        :param value:
          Initial value for this bind param.  Will be used at statement
          execution time as the value for this parameter passed to the
          DBAPI, if no other value is indicated to the statement execution
          method for this particular parameter name.  Defaults to ``None``.

        :param callable\_:
          A callable function that takes the place of "value".  The function
          will be called at statement execution time to determine the
          ultimate value.   Used for scenarios where the actual bind
          value cannot be determined at the point at which the clause
          construct is created, but embedded bind values are still desirable.

        :param type\_:
          A :class:`.TypeEngine` class or instance representing an optional
          datatype for this :func:`.bindparam`.  If not passed, a type
          may be determined automatically for the bind, based on the given
          value; for example, trivial Python types such as ``str``,
          ``int``, ``bool``
          may result in the :class:`.String`, :class:`.Integer` or
          :class:`.Boolean` types being automatically selected.

          The type of a :func:`.bindparam` is significant especially in that
          the type will apply pre-processing to the value before it is
          passed to the database.  For example, a :func:`.bindparam` which
          refers to a datetime value, and is specified as holding the
          :class:`.DateTime` type, may apply conversion needed to the
          value (such as stringification on SQLite) before passing the value
          to the database.

        :param unique:
          if True, the key name of this :class:`.BindParameter` will be
          modified if another :class:`.BindParameter` of the same name
          already has been located within the containing
          expression.  This flag is used generally by the internals
          when producing so-called "anonymous" bound expressions, it
          isn't generally applicable to explicitly-named :func:`.bindparam`
          constructs.

        :param required:
          If ``True``, a value is required at execution time.  If not passed,
          it defaults to ``True`` if neither :paramref:`.bindparam.value`
          or :paramref:`.bindparam.callable` were passed.  If either of these
          parameters are present, then :paramref:`.bindparam.required`
          defaults to ``False``.

        :param quote:
          True if this parameter name requires quoting and is not
          currently known as a SQLAlchemy reserved word; this currently
          only applies to the Oracle backend, where bound names must
          sometimes be quoted.

        :param isoutparam:
          if True, the parameter should be treated like a stored procedure
          "OUT" parameter.  This applies to backends such as Oracle which
          support OUT parameters.

        :param expanding:
          if True, this parameter will be treated as an "expanding" parameter
          at execution time; the parameter value is expected to be a sequence,
          rather than a scalar value, and the string SQL statement will
          be transformed on a per-execution basis to accommodate the sequence
          with a variable number of parameter slots passed to the DBAPI.
          This is to allow statement caching to be used in conjunction with
          an IN clause.

          .. seealso::

            :meth:`.ColumnOperators.in_`

            :ref:`baked_in` - with baked queries

          .. note:: The "expanding" feature does not support "executemany"-
             style parameter sets.

          .. versionadded:: 1.2

          .. versionchanged:: 1.3 the "expanding" bound parameter feature now
             supports empty lists.


        .. seealso::

            :ref:`coretutorial_bind_param`

            :ref:`coretutorial_insert_expressions`

            :func:`.outparam`

        :param literal_execute:
          if True, the bound parameter will be rendered in the compile phase
          with a special "POSTCOMPILE" token, and the SQLAlchemy compiler will
          render the final value of the parameter into the SQL statement at
          statement execution time, omitting the value from the parameter
          dictionary / list passed to DBAPI ``cursor.execute()``.  This
          produces a similar effect as that of using the ``literal_binds``,
          compilation flag,  however takes place as the statement is sent to
          the DBAPI ``cursor.execute()`` method, rather than when the statement
          is compiled.   The primary use of this
          capability is for rendering LIMIT / OFFSET clauses for database
          drivers that can't accommodate for bound parameters in these
          contexts, while allowing SQL constructs to be cacheable at the
          compilation level.

          .. versionadded:: 1.4 Added "post compile" bound parameters

            .. seealso::

                :ref:`change_4808`.

        """

        if required is NO_ARG:
            required = value is NO_ARG and callable_ is None
        if value is NO_ARG:
            value = None

        if quote is not None:
            key = quoted_name(key, quote)

        if unique:
            self.key = _anonymous_label.safe_construct(
                id(self),
                key
                if key is not None and not isinstance(key, _anonymous_label)
                else "param",
                sanitize_key=True,
            )
            self._key_is_anon = True
        elif key:
            self.key = key
        else:
            self.key = _anonymous_label.safe_construct(id(self), "param")
            self._key_is_anon = True

        # identifying key that won't change across
        # clones, used to identify the bind's logical
        # identity
        self._identifying_key = self.key

        # key that was passed in the first place, used to
        # generate new keys
        self._orig_key = key or "param"

        self.unique = unique
        self.value = value
        self.callable = callable_
        self.isoutparam = isoutparam
        self.required = required

        # indicate an "expanding" parameter; the compiler sets this
        # automatically in the compiler _render_in_expr_w_bindparam method
        # for an IN expression
        self.expanding = expanding

        # this is another hint to help w/ expanding and is typically
        # set in the compiler _render_in_expr_w_bindparam method for an
        # IN expression
        self.expand_op = None

        self.literal_execute = literal_execute
        if _is_crud:
            self._is_crud = True

        if type_ is None:
            if expanding and value:
                check_value = value[0]
            else:
                check_value = value
            if _compared_to_type is not None:
                self.type = _compared_to_type.coerce_compared_value(
                    _compared_to_operator, check_value
                )
            else:
                self.type = type_api._resolve_value_to_type(check_value)
        elif isinstance(type_, type):
            self.type = type_()
        elif type_._is_tuple_type and value:
            if expanding:
                check_value = value[0]
            else:
                check_value = value
            self.type = type_._resolve_values_to_types(check_value)
        else:
            self.type = type_

    def _with_value(self, value, maintain_key=False, required=NO_ARG):
        """Return a copy of this :class:`.BindParameter` with the given value
        set.
        """
        cloned = self._clone(maintain_key=maintain_key)
        cloned.value = value
        cloned.callable = None
        cloned.required = required if required is not NO_ARG else self.required
        if cloned.type is type_api.NULLTYPE:
            cloned.type = type_api._resolve_value_to_type(value)
        return cloned

    @property
    def effective_value(self):
        """Return the value of this bound parameter,
        taking into account if the ``callable`` parameter
        was set.

        The ``callable`` value will be evaluated
        and returned if present, else ``value``.

        """
        if self.callable:
            return self.callable()
        else:
            return self.value

    def render_literal_execute(self):
        """Produce a copy of this bound parameter that will enable the
        :paramref:`_sql.BindParameter.literal_execute` flag.

        The :paramref:`_sql.BindParameter.literal_execute` flag will
        have the effect of the parameter rendered in the compiled SQL
        string using ``[POSTCOMPILE]`` form, which is a special form that
        is converted to be a rendering of the literal value of the parameter
        at SQL execution time.    The rationale is to support caching
        of SQL statement strings that can embed per-statement literal values,
        such as LIMIT and OFFSET parameters, in the final SQL string that
        is passed to the DBAPI.   Dialects in particular may want to use
        this method within custom compilation schemes.

        .. versionadded:: 1.4.5

        .. seealso::

            :ref:`engine_thirdparty_caching`

        """
        return self.__class__(
            self.key,
            self.value,
            type_=self.type,
            literal_execute=True,
        )

    def _negate_in_binary(self, negated_op, original_op):
        if self.expand_op is original_op:
            bind = self._clone()
            bind.expand_op = negated_op
            return bind
        else:
            return self

    def _with_binary_element_type(self, type_):
        c = ClauseElement._clone(self)
        c.type = type_
        return c

    def _clone(self, maintain_key=False, **kw):
        c = ClauseElement._clone(self, **kw)
        if not maintain_key and self.unique:
            c.key = _anonymous_label.safe_construct(
                id(c), c._orig_key or "param", sanitize_key=True
            )
        return c

    def _gen_cache_key(self, anon_map, bindparams):
        _gen_cache_ok = self.__class__.__dict__.get("inherit_cache", False)

        if not _gen_cache_ok:
            if anon_map is not None:
                anon_map[NO_CACHE] = True
            return None

        idself = id(self)
        if idself in anon_map:
            return (anon_map[idself], self.__class__)
        else:
            # inline of
            # id_ = anon_map[idself]
            anon_map[idself] = id_ = str(anon_map.index)
            anon_map.index += 1

        if bindparams is not None:
            bindparams.append(self)

        return (
            id_,
            self.__class__,
            self.type._static_cache_key,
            self.key % anon_map if self._key_is_anon else self.key,
        )

    def _convert_to_unique(self):
        if not self.unique:
            self.unique = True
            self.key = _anonymous_label.safe_construct(
                id(self), self._orig_key or "param", sanitize_key=True
            )

    def __getstate__(self):
        """execute a deferred value for serialization purposes."""

        d = self.__dict__.copy()
        v = self.value
        if self.callable:
            v = self.callable()
            d["callable"] = None
        d["value"] = v
        return d

    def __setstate__(self, state):
        if state.get("unique", False):
            state["key"] = _anonymous_label.safe_construct(
                id(self), state.get("_orig_key", "param"), sanitize_key=True
            )
        self.__dict__.update(state)

    def __repr__(self):
        return "%s(%r, %r, type_=%r)" % (
            self.__class__.__name__,
            self.key,
            self.value,
            self.type,
        )


class TypeClause(ClauseElement):
    """Handle a type keyword in a SQL statement.

    Used by the ``Case`` statement.

    """

    __visit_name__ = "typeclause"

    _traverse_internals = [("type", InternalTraversal.dp_type)]

    def __init__(self, type_):
        self.type = type_


class TextClause(
    roles.DDLConstraintColumnRole,
    roles.DDLExpressionRole,
    roles.StatementOptionRole,
    roles.WhereHavingRole,
    roles.OrderByRole,
    roles.FromClauseRole,
    roles.SelectStatementRole,
    roles.BinaryElementRole,
    roles.InElementRole,
    Executable,
    ClauseElement,
):
    """Represent a literal SQL text fragment.

    E.g.::

        from sqlalchemy import text

        t = text("SELECT * FROM users")
        result = connection.execute(t)


    The :class:`_expression.TextClause` construct is produced using the
    :func:`_expression.text`
    function; see that function for full documentation.

    .. seealso::

        :func:`_expression.text`

    """

    __visit_name__ = "textclause"

    _traverse_internals = [
        ("_bindparams", InternalTraversal.dp_string_clauseelement_dict),
        ("text", InternalTraversal.dp_string),
    ]

    _is_text_clause = True

    _is_textual = True

    _bind_params_regex = re.compile(r"(?<![:\w\x5c]):(\w+)(?!:)", re.UNICODE)
    _execution_options = Executable._execution_options.union(
        {"autocommit": PARSE_AUTOCOMMIT}
    )
    _is_implicitly_boolean = False

    _render_label_in_columns_clause = False

    _hide_froms = ()

    def __and__(self, other):
        # support use in select.where(), query.filter()
        return and_(self, other)

    @property
    def _select_iterable(self):
        return (self,)

    # help in those cases where text() is
    # interpreted in a column expression situation
    key = _label = _resolve_label = None

    _allow_label_resolve = False

    def __init__(self, text, bind=None):
        self._bind = bind
        self._bindparams = {}

        def repl(m):
            self._bindparams[m.group(1)] = BindParameter(m.group(1))
            return ":%s" % m.group(1)

        # scan the string and search for bind parameter names, add them
        # to the list of bindparams
        self.text = self._bind_params_regex.sub(repl, text)

    @classmethod
    @_document_text_coercion("text", ":func:`.text`", ":paramref:`.text.text`")
    @util.deprecated_params(
        bind=(
            "2.0",
            "The :paramref:`_sql.text.bind` argument is deprecated and "
            "will be removed in SQLAlchemy 2.0.",
        ),
    )
    def _create_text(cls, text, bind=None):
        r"""Construct a new :class:`_expression.TextClause` clause,
        representing
        a textual SQL string directly.

        E.g.::

            from sqlalchemy import text

            t = text("SELECT * FROM users")
            result = connection.execute(t)

        The advantages :func:`_expression.text`
        provides over a plain string are
        backend-neutral support for bind parameters, per-statement
        execution options, as well as
        bind parameter and result-column typing behavior, allowing
        SQLAlchemy type constructs to play a role when executing
        a statement that is specified literally.  The construct can also
        be provided with a ``.c`` collection of column elements, allowing
        it to be embedded in other SQL expression constructs as a subquery.

        Bind parameters are specified by name, using the format ``:name``.
        E.g.::

            t = text("SELECT * FROM users WHERE id=:user_id")
            result = connection.execute(t, user_id=12)

        For SQL statements where a colon is required verbatim, as within
        an inline string, use a backslash to escape::

            t = text("SELECT * FROM users WHERE name='\:username'")

        The :class:`_expression.TextClause`
        construct includes methods which can
        provide information about the bound parameters as well as the column
        values which would be returned from the textual statement, assuming
        it's an executable SELECT type of statement.  The
        :meth:`_expression.TextClause.bindparams`
        method is used to provide bound
        parameter detail, and :meth:`_expression.TextClause.columns`
        method allows
        specification of return columns including names and types::

            t = text("SELECT * FROM users WHERE id=:user_id").\
                    bindparams(user_id=7).\
                    columns(id=Integer, name=String)

            for id, name in connection.execute(t):
                print(id, name)

        The :func:`_expression.text` construct is used in cases when
        a literal string SQL fragment is specified as part of a larger query,
        such as for the WHERE clause of a SELECT statement::

            s = select(users.c.id, users.c.name).where(text("id=:user_id"))
            result = connection.execute(s, user_id=12)

        :func:`_expression.text` is also used for the construction
        of a full, standalone statement using plain text.
        As such, SQLAlchemy refers
        to it as an :class:`.Executable` object, and it supports
        the :meth:`Executable.execution_options` method.  For example,
        a :func:`_expression.text`
        construct that should be subject to "autocommit"
        can be set explicitly so using the
        :paramref:`.Connection.execution_options.autocommit` option::

            t = text("EXEC my_procedural_thing()").\
                    execution_options(autocommit=True)

        .. deprecated:: 1.4  The "autocommit" execution option is deprecated
           and will be removed in SQLAlchemy 2.0.  See
           :ref:`migration_20_autocommit` for discussion.

        :param text:
          the text of the SQL statement to be created.  Use ``:<param>``
          to specify bind parameters; they will be compiled to their
          engine-specific format.

        :param bind:
          an optional connection or engine to be used for this text query.

        .. seealso::

            :ref:`sqlexpression_text` - in the Core tutorial


        """
        return TextClause(text, bind=bind)

    @_generative
    def bindparams(self, *binds, **names_to_values):
        """Establish the values and/or types of bound parameters within
        this :class:`_expression.TextClause` construct.

        Given a text construct such as::

            from sqlalchemy import text
            stmt = text("SELECT id, name FROM user WHERE name=:name "
                        "AND timestamp=:timestamp")

        the :meth:`_expression.TextClause.bindparams`
        method can be used to establish
        the initial value of ``:name`` and ``:timestamp``,
        using simple keyword arguments::

            stmt = stmt.bindparams(name='jack',
                        timestamp=datetime.datetime(2012, 10, 8, 15, 12, 5))

        Where above, new :class:`.BindParameter` objects
        will be generated with the names ``name`` and ``timestamp``, and
        values of ``jack`` and ``datetime.datetime(2012, 10, 8, 15, 12, 5)``,
        respectively.  The types will be
        inferred from the values given, in this case :class:`.String` and
        :class:`.DateTime`.

        When specific typing behavior is needed, the positional ``*binds``
        argument can be used in which to specify :func:`.bindparam` constructs
        directly.  These constructs must include at least the ``key``
        argument, then an optional value and type::

            from sqlalchemy import bindparam
            stmt = stmt.bindparams(
                            bindparam('name', value='jack', type_=String),
                            bindparam('timestamp', type_=DateTime)
                        )

        Above, we specified the type of :class:`.DateTime` for the
        ``timestamp`` bind, and the type of :class:`.String` for the ``name``
        bind.  In the case of ``name`` we also set the default value of
        ``"jack"``.

        Additional bound parameters can be supplied at statement execution
        time, e.g.::

            result = connection.execute(stmt,
                        timestamp=datetime.datetime(2012, 10, 8, 15, 12, 5))

        The :meth:`_expression.TextClause.bindparams`
        method can be called repeatedly,
        where it will re-use existing :class:`.BindParameter` objects to add
        new information.  For example, we can call
        :meth:`_expression.TextClause.bindparams`
        first with typing information, and a
        second time with value information, and it will be combined::

            stmt = text("SELECT id, name FROM user WHERE name=:name "
                        "AND timestamp=:timestamp")
            stmt = stmt.bindparams(
                bindparam('name', type_=String),
                bindparam('timestamp', type_=DateTime)
            )
            stmt = stmt.bindparams(
                name='jack',
                timestamp=datetime.datetime(2012, 10, 8, 15, 12, 5)
            )

        The :meth:`_expression.TextClause.bindparams`
        method also supports the concept of
        **unique** bound parameters.  These are parameters that are
        "uniquified" on name at statement compilation time, so that  multiple
        :func:`_expression.text`
        constructs may be combined together without the names
        conflicting.  To use this feature, specify the
        :paramref:`.BindParameter.unique` flag on each :func:`.bindparam`
        object::

            stmt1 = text("select id from table where name=:name").bindparams(
                bindparam("name", value='name1', unique=True)
            )
            stmt2 = text("select id from table where name=:name").bindparams(
                bindparam("name", value='name2', unique=True)
            )

            union = union_all(
                stmt1.columns(column("id")),
                stmt2.columns(column("id"))
            )

        The above statement will render as::

            select id from table where name=:name_1
            UNION ALL select id from table where name=:name_2

        .. versionadded:: 1.3.11  Added support for the
           :paramref:`.BindParameter.unique` flag to work with
           :func:`_expression.text`
           constructs.

        """
        self._bindparams = new_params = self._bindparams.copy()

        for bind in binds:
            try:
                # the regex used for text() currently will not match
                # a unique/anonymous key in any case, so use the _orig_key
                # so that a text() construct can support unique parameters
                existing = new_params[bind._orig_key]
            except KeyError as err:
                util.raise_(
                    exc.ArgumentError(
                        "This text() construct doesn't define a "
                        "bound parameter named %r" % bind._orig_key
                    ),
                    replace_context=err,
                )
            else:
                new_params[existing._orig_key] = bind

        for key, value in names_to_values.items():
            try:
                existing = new_params[key]
            except KeyError as err:
                util.raise_(
                    exc.ArgumentError(
                        "This text() construct doesn't define a "
                        "bound parameter named %r" % key
                    ),
                    replace_context=err,
                )
            else:
                new_params[key] = existing._with_value(value, required=False)

    @util.preload_module("sqlalchemy.sql.selectable")
    def columns(self, *cols, **types):
        r"""Turn this :class:`_expression.TextClause` object into a
        :class:`_expression.TextualSelect`
        object that serves the same role as a SELECT
        statement.

        The :class:`_expression.TextualSelect` is part of the
        :class:`_expression.SelectBase`
        hierarchy and can be embedded into another statement by using the
        :meth:`_expression.TextualSelect.subquery` method to produce a
        :class:`.Subquery`
        object, which can then be SELECTed from.

        This function essentially bridges the gap between an entirely
        textual SELECT statement and the SQL expression language concept
        of a "selectable"::

            from sqlalchemy.sql import column, text

            stmt = text("SELECT id, name FROM some_table")
            stmt = stmt.columns(column('id'), column('name')).subquery('st')

            stmt = select(mytable).\
                    select_from(
                        mytable.join(stmt, mytable.c.name == stmt.c.name)
                    ).where(stmt.c.id > 5)

        Above, we pass a series of :func:`_expression.column` elements to the
        :meth:`_expression.TextClause.columns` method positionally.  These
        :func:`_expression.column`
        elements now become first class elements upon the
        :attr:`_expression.TextualSelect.selected_columns` column collection,
        which then
        become part of the :attr:`.Subquery.c` collection after
        :meth:`_expression.TextualSelect.subquery` is invoked.

        The column expressions we pass to
        :meth:`_expression.TextClause.columns` may
        also be typed; when we do so, these :class:`.TypeEngine` objects become
        the effective return type of the column, so that SQLAlchemy's
        result-set-processing systems may be used on the return values.
        This is often needed for types such as date or boolean types, as well
        as for unicode processing on some dialect configurations::

            stmt = text("SELECT id, name, timestamp FROM some_table")
            stmt = stmt.columns(
                        column('id', Integer),
                        column('name', Unicode),
                        column('timestamp', DateTime)
                    )

            for id, name, timestamp in connection.execute(stmt):
                print(id, name, timestamp)

        As a shortcut to the above syntax, keyword arguments referring to
        types alone may be used, if only type conversion is needed::

            stmt = text("SELECT id, name, timestamp FROM some_table")
            stmt = stmt.columns(
                        id=Integer,
                        name=Unicode,
                        timestamp=DateTime
                    )

            for id, name, timestamp in connection.execute(stmt):
                print(id, name, timestamp)

        The positional form of :meth:`_expression.TextClause.columns`
        also provides the
        unique feature of **positional column targeting**, which is
        particularly useful when using the ORM with complex textual queries. If
        we specify the columns from our model to
        :meth:`_expression.TextClause.columns`,
        the result set will match to those columns positionally, meaning the
        name or origin of the column in the textual SQL doesn't matter::

            stmt = text("SELECT users.id, addresses.id, users.id, "
                 "users.name, addresses.email_address AS email "
                 "FROM users JOIN addresses ON users.id=addresses.user_id "
                 "WHERE users.id = 1").columns(
                    User.id,
                    Address.id,
                    Address.user_id,
                    User.name,
                    Address.email_address
                 )

            query = session.query(User).from_statement(stmt).options(
                contains_eager(User.addresses))

        .. versionadded:: 1.1 the :meth:`_expression.TextClause.columns`
           method now
           offers positional column targeting in the result set when
           the column expressions are passed purely positionally.

        The :meth:`_expression.TextClause.columns` method provides a direct
        route to calling :meth:`_expression.FromClause.subquery` as well as
        :meth:`_expression.SelectBase.cte`
        against a textual SELECT statement::

            stmt = stmt.columns(id=Integer, name=String).cte('st')

            stmt = select(sometable).where(sometable.c.id == stmt.c.id)

        :param \*cols: A series of :class:`_expression.ColumnElement` objects,
         typically
         :class:`_schema.Column` objects from a :class:`_schema.Table`
         or ORM level
         column-mapped attributes, representing a set of columns that this
         textual string will SELECT from.

        :param \**types: A mapping of string names to :class:`.TypeEngine`
         type objects indicating the datatypes to use for names that are
         SELECTed from the textual string.  Prefer to use the ``*cols``
         argument as it also indicates positional ordering.

        """
        selectable = util.preloaded.sql_selectable
        positional_input_cols = [
            ColumnClause(col.key, types.pop(col.key))
            if col.key in types
            else col
            for col in cols
        ]
        keyed_input_cols = [
            ColumnClause(key, type_) for key, type_ in types.items()
        ]

        return selectable.TextualSelect(
            self,
            positional_input_cols + keyed_input_cols,
            positional=bool(positional_input_cols) and not keyed_input_cols,
        )

    @property
    def type(self):
        return type_api.NULLTYPE

    @property
    def comparator(self):
        return self.type.comparator_factory(self)

    def self_group(self, against=None):
        if against is operators.in_op:
            return Grouping(self)
        else:
            return self


class Null(SingletonConstant, roles.ConstExprRole, ColumnElement):
    """Represent the NULL keyword in a SQL statement.

    :class:`.Null` is accessed as a constant via the
    :func:`.null` function.

    """

    __visit_name__ = "null"

    _traverse_internals = []

    @util.memoized_property
    def type(self):
        return type_api.NULLTYPE

    @classmethod
    def _instance(cls):
        """Return a constant :class:`.Null` construct."""

        return Null()


Null._create_singleton()


class False_(SingletonConstant, roles.ConstExprRole, ColumnElement):
    """Represent the ``false`` keyword, or equivalent, in a SQL statement.

    :class:`.False_` is accessed as a constant via the
    :func:`.false` function.

    """

    __visit_name__ = "false"
    _traverse_internals = []

    @util.memoized_property
    def type(self):
        return type_api.BOOLEANTYPE

    def _negate(self):
        return True_()

    @classmethod
    def _instance(cls):
        """Return a :class:`.False_` construct.

        E.g.::

            >>> from sqlalchemy import false
            >>> print(select(t.c.x).where(false()))
            SELECT x FROM t WHERE false

        A backend which does not support true/false constants will render as
        an expression against 1 or 0::

            >>> print(select(t.c.x).where(false()))
            SELECT x FROM t WHERE 0 = 1

        The :func:`.true` and :func:`.false` constants also feature
        "short circuit" operation within an :func:`.and_` or :func:`.or_`
        conjunction::

            >>> print(select(t.c.x).where(or_(t.c.x > 5, true())))
            SELECT x FROM t WHERE true

            >>> print(select(t.c.x).where(and_(t.c.x > 5, false())))
            SELECT x FROM t WHERE false

        .. versionchanged:: 0.9 :func:`.true` and :func:`.false` feature
           better integrated behavior within conjunctions and on dialects
           that don't support true/false constants.

        .. seealso::

            :func:`.true`

        """

        return False_()


False_._create_singleton()


class True_(SingletonConstant, roles.ConstExprRole, ColumnElement):
    """Represent the ``true`` keyword, or equivalent, in a SQL statement.

    :class:`.True_` is accessed as a constant via the
    :func:`.true` function.

    """

    __visit_name__ = "true"

    _traverse_internals = []

    @util.memoized_property
    def type(self):
        return type_api.BOOLEANTYPE

    def _negate(self):
        return False_()

    @classmethod
    def _ifnone(cls, other):
        if other is None:
            return cls._instance()
        else:
            return other

    @classmethod
    def _instance(cls):
        """Return a constant :class:`.True_` construct.

        E.g.::

            >>> from sqlalchemy import true
            >>> print(select(t.c.x).where(true()))
            SELECT x FROM t WHERE true

        A backend which does not support true/false constants will render as
        an expression against 1 or 0::

            >>> print(select(t.c.x).where(true()))
            SELECT x FROM t WHERE 1 = 1

        The :func:`.true` and :func:`.false` constants also feature
        "short circuit" operation within an :func:`.and_` or :func:`.or_`
        conjunction::

            >>> print(select(t.c.x).where(or_(t.c.x > 5, true())))
            SELECT x FROM t WHERE true

            >>> print(select(t.c.x).where(and_(t.c.x > 5, false())))
            SELECT x FROM t WHERE false

        .. versionchanged:: 0.9 :func:`.true` and :func:`.false` feature
           better integrated behavior within conjunctions and on dialects
           that don't support true/false constants.

        .. seealso::

            :func:`.false`

        """

        return True_()


True_._create_singleton()


class ClauseList(
    roles.InElementRole,
    roles.OrderByRole,
    roles.ColumnsClauseRole,
    roles.DMLColumnRole,
    ClauseElement,
):
    """Describe a list of clauses, separated by an operator.

    By default, is comma-separated, such as a column listing.

    """

    __visit_name__ = "clauselist"

    _is_clause_list = True

    _traverse_internals = [
        ("clauses", InternalTraversal.dp_clauseelement_list),
        ("operator", InternalTraversal.dp_operator),
    ]

    def __init__(self, *clauses, **kwargs):
        self.operator = kwargs.pop("operator", operators.comma_op)
        self.group = kwargs.pop("group", True)
        self.group_contents = kwargs.pop("group_contents", True)
        if kwargs.pop("_flatten_sub_clauses", False):
            clauses = util.flatten_iterator(clauses)
        self._text_converter_role = text_converter_role = kwargs.pop(
            "_literal_as_text_role", roles.WhereHavingRole
        )
        if self.group_contents:
            self.clauses = [
                coercions.expect(
                    text_converter_role, clause, apply_propagate_attrs=self
                ).self_group(against=self.operator)
                for clause in clauses
            ]
        else:
            self.clauses = [
                coercions.expect(
                    text_converter_role, clause, apply_propagate_attrs=self
                )
                for clause in clauses
            ]
        self._is_implicitly_boolean = operators.is_boolean(self.operator)

    @classmethod
    def _construct_raw(cls, operator, clauses=None):
        self = cls.__new__(cls)
        self.clauses = clauses if clauses else []
        self.group = True
        self.operator = operator
        self.group_contents = True
        self._is_implicitly_boolean = False
        return self

    def __iter__(self):
        return iter(self.clauses)

    def __len__(self):
        return len(self.clauses)

    @property
    def _select_iterable(self):
        return itertools.chain.from_iterable(
            [elem._select_iterable for elem in self.clauses]
        )

    def append(self, clause):
        if self.group_contents:
            self.clauses.append(
                coercions.expect(self._text_converter_role, clause).self_group(
                    against=self.operator
                )
            )
        else:
            self.clauses.append(
                coercions.expect(self._text_converter_role, clause)
            )

    @property
    def _from_objects(self):
        return list(itertools.chain(*[c._from_objects for c in self.clauses]))

    def self_group(self, against=None):
        if self.group and operators.is_precedent(self.operator, against):
            return Grouping(self)
        else:
            return self


class BooleanClauseList(ClauseList, ColumnElement):
    __visit_name__ = "clauselist"
    inherit_cache = True

    def __init__(self, *arg, **kw):
        raise NotImplementedError(
            "BooleanClauseList has a private constructor"
        )

    @classmethod
    def _process_clauses_for_boolean(
        cls, operator, continue_on, skip_on, clauses
    ):
        has_continue_on = None

        convert_clauses = []

        against = operators._asbool
        lcc = 0

        for clause in clauses:
            if clause is continue_on:
                # instance of continue_on, like and_(x, y, True, z), store it
                # if we didn't find one already, we will use it if there
                # are no other expressions here.
                has_continue_on = clause
            elif clause is skip_on:
                # instance of skip_on, e.g. and_(x, y, False, z), cancels
                # the rest out
                convert_clauses = [clause]
                lcc = 1
                break
            else:
                if not lcc:
                    lcc = 1
                else:
                    against = operator
                    # technically this would be len(convert_clauses) + 1
                    # however this only needs to indicate "greater than one"
                    lcc = 2
                convert_clauses.append(clause)

        if not convert_clauses and has_continue_on is not None:
            convert_clauses = [has_continue_on]
            lcc = 1

        return lcc, [c.self_group(against=against) for c in convert_clauses]

    @classmethod
    def _construct(cls, operator, continue_on, skip_on, *clauses, **kw):
        lcc, convert_clauses = cls._process_clauses_for_boolean(
            operator,
            continue_on,
            skip_on,
            [
                coercions.expect(roles.WhereHavingRole, clause)
                for clause in util.coerce_generator_arg(clauses)
            ],
        )

        if lcc > 1:
            # multiple elements.  Return regular BooleanClauseList
            # which will link elements against the operator.
            return cls._construct_raw(operator, convert_clauses)
        elif lcc == 1:
            # just one element.  return it as a single boolean element,
            # not a list and discard the operator.
            return convert_clauses[0]
        else:
            # no elements period.  deprecated use case.  return an empty
            # ClauseList construct that generates nothing unless it has
            # elements added to it.
            util.warn_deprecated(
                "Invoking %(name)s() without arguments is deprecated, and "
                "will be disallowed in a future release.   For an empty "
                "%(name)s() construct, use %(name)s(%(continue_on)s, *args)."
                % {
                    "name": operator.__name__,
                    "continue_on": "True"
                    if continue_on is True_._singleton
                    else "False",
                },
                version="1.4",
            )
            return cls._construct_raw(operator)

    @classmethod
    def _construct_for_whereclause(cls, clauses):
        operator, continue_on, skip_on = (
            operators.and_,
            True_._singleton,
            False_._singleton,
        )

        lcc, convert_clauses = cls._process_clauses_for_boolean(
            operator,
            continue_on,
            skip_on,
            clauses,  # these are assumed to be coerced already
        )

        if lcc > 1:
            # multiple elements.  Return regular BooleanClauseList
            # which will link elements against the operator.
            return cls._construct_raw(operator, convert_clauses)
        elif lcc == 1:
            # just one element.  return it as a single boolean element,
            # not a list and discard the operator.
            return convert_clauses[0]
        else:
            return None

    @classmethod
    def _construct_raw(cls, operator, clauses=None):
        self = cls.__new__(cls)
        self.clauses = clauses if clauses else []
        self.group = True
        self.operator = operator
        self.group_contents = True
        self.type = type_api.BOOLEANTYPE
        self._is_implicitly_boolean = True
        return self

    @classmethod
    def and_(cls, *clauses):
        r"""Produce a conjunction of expressions joined by ``AND``.

        E.g.::

            from sqlalchemy import and_

            stmt = select(users_table).where(
                            and_(
                                users_table.c.name == 'wendy',
                                users_table.c.enrolled == True
                            )
                        )

        The :func:`.and_` conjunction is also available using the
        Python ``&`` operator (though note that compound expressions
        need to be parenthesized in order to function with Python
        operator precedence behavior)::

            stmt = select(users_table).where(
                            (users_table.c.name == 'wendy') &
                            (users_table.c.enrolled == True)
                        )

        The :func:`.and_` operation is also implicit in some cases;
        the :meth:`_expression.Select.where`
        method for example can be invoked multiple
        times against a statement, which will have the effect of each
        clause being combined using :func:`.and_`::

            stmt = select(users_table).\
                    where(users_table.c.name == 'wendy').\
                    where(users_table.c.enrolled == True)

        The :func:`.and_` construct must be given at least one positional
        argument in order to be valid; a :func:`.and_` construct with no
        arguments is ambiguous.   To produce an "empty" or dynamically
        generated :func:`.and_`  expression, from a given list of expressions,
        a "default" element of ``True`` should be specified::

            criteria = and_(True, *expressions)

        The above expression will compile to SQL as the expression ``true``
        or ``1 = 1``, depending on backend, if no other expressions are
        present.  If expressions are present, then the ``True`` value is
        ignored as it does not affect the outcome of an AND expression that
        has other elements.

        .. deprecated:: 1.4  The :func:`.and_` element now requires that at
           least one argument is passed; creating the :func:`.and_` construct
           with no arguments is deprecated, and will emit a deprecation warning
           while continuing to produce a blank SQL string.

        .. seealso::

            :func:`.or_`

        """
        return cls._construct(
            operators.and_, True_._singleton, False_._singleton, *clauses
        )

    @classmethod
    def or_(cls, *clauses):
        """Produce a conjunction of expressions joined by ``OR``.

        E.g.::

            from sqlalchemy import or_

            stmt = select(users_table).where(
                            or_(
                                users_table.c.name == 'wendy',
                                users_table.c.name == 'jack'
                            )
                        )

        The :func:`.or_` conjunction is also available using the
        Python ``|`` operator (though note that compound expressions
        need to be parenthesized in order to function with Python
        operator precedence behavior)::

            stmt = select(users_table).where(
                            (users_table.c.name == 'wendy') |
                            (users_table.c.name == 'jack')
                        )

        The :func:`.or_` construct must be given at least one positional
        argument in order to be valid; a :func:`.or_` construct with no
        arguments is ambiguous.   To produce an "empty" or dynamically
        generated :func:`.or_`  expression, from a given list of expressions,
        a "default" element of ``False`` should be specified::

            or_criteria = or_(False, *expressions)

        The above expression will compile to SQL as the expression ``false``
        or ``0 = 1``, depending on backend, if no other expressions are
        present.  If expressions are present, then the ``False`` value is
        ignored as it does not affect the outcome of an OR expression which
        has other elements.

        .. deprecated:: 1.4  The :func:`.or_` element now requires that at
           least one argument is passed; creating the :func:`.or_` construct
           with no arguments is deprecated, and will emit a deprecation warning
           while continuing to produce a blank SQL string.

        .. seealso::

            :func:`.and_`

        """
        return cls._construct(
            operators.or_, False_._singleton, True_._singleton, *clauses
        )

    @property
    def _select_iterable(self):
        return (self,)

    def self_group(self, against=None):
        if not self.clauses:
            return self
        else:
            return super(BooleanClauseList, self).self_group(against=against)

    def _negate(self):
        return ClauseList._negate(self)


and_ = BooleanClauseList.and_
or_ = BooleanClauseList.or_


class Tuple(ClauseList, ColumnElement):
    """Represent a SQL tuple."""

    __visit_name__ = "tuple"

    _traverse_internals = ClauseList._traverse_internals + []

    @util.preload_module("sqlalchemy.sql.sqltypes")
    def __init__(self, *clauses, **kw):
        """Return a :class:`.Tuple`.

        Main usage is to produce a composite IN construct using
        :meth:`.ColumnOperators.in_` ::

            from sqlalchemy import tuple_

            tuple_(table.c.col1, table.c.col2).in_(
                [(1, 2), (5, 12), (10, 19)]
            )

        .. versionchanged:: 1.3.6 Added support for SQLite IN tuples.

        .. warning::

            The composite IN construct is not supported by all backends, and is
            currently known to work on PostgreSQL, MySQL, and SQLite.
            Unsupported backends will raise a subclass of
            :class:`~sqlalchemy.exc.DBAPIError` when such an expression is
            invoked.

        """
        sqltypes = util.preloaded.sql_sqltypes

        types = kw.pop("types", None)
        if types is None:
            clauses = [
                coercions.expect(roles.ExpressionElementRole, c)
                for c in clauses
            ]
        else:
            if len(types) != len(clauses):
                raise exc.ArgumentError(
                    "Wrong number of elements for %d-tuple: %r "
                    % (len(types), clauses)
                )
            clauses = [
                coercions.expect(
                    roles.ExpressionElementRole,
                    c,
                    type_=typ if not typ._isnull else None,
                )
                for typ, c in zip(types, clauses)
            ]

        self.type = sqltypes.TupleType(*[arg.type for arg in clauses])
        super(Tuple, self).__init__(*clauses, **kw)

    @property
    def _select_iterable(self):
        return (self,)

    def _bind_param(self, operator, obj, type_=None, expanding=False):
        if expanding:
            return BindParameter(
                None,
                value=obj,
                _compared_to_operator=operator,
                unique=True,
                expanding=True,
                type_=self.type,
            )
        else:
            return Tuple(
                *[
                    BindParameter(
                        None,
                        o,
                        _compared_to_operator=operator,
                        _compared_to_type=compared_to_type,
                        unique=True,
                        type_=type_,
                    )
                    for o, compared_to_type in zip(obj, self.type.types)
                ]
            )

    def self_group(self, against=None):
        # Tuple is parenthesized by definition.
        return self


class Case(ColumnElement):
    """Represent a ``CASE`` expression.

    :class:`.Case` is produced using the :func:`.case` factory function,
    as in::

        from sqlalchemy import case

        stmt = select(users_table).\
                    where(
                        case(
                            (users_table.c.name == 'wendy', 'W'),
                            (users_table.c.name == 'jack', 'J'),
                            else_='E'
                        )
                    )

    Details on :class:`.Case` usage is at :func:`.case`.

    .. seealso::

        :func:`.case`

    """

    __visit_name__ = "case"

    _traverse_internals = [
        ("value", InternalTraversal.dp_clauseelement),
        ("whens", InternalTraversal.dp_clauseelement_tuples),
        ("else_", InternalTraversal.dp_clauseelement),
    ]

    # TODO: for Py2k removal, this will be:
    # def __init__(self, *whens, value=None, else_=None):

    def __init__(self, *whens, **kw):
        r"""Produce a ``CASE`` expression.

        The ``CASE`` construct in SQL is a conditional object that
        acts somewhat analogously to an "if/then" construct in other
        languages.  It returns an instance of :class:`.Case`.

        :func:`.case` in its usual form is passed a series of "when"
        constructs, that is, a list of conditions and results as tuples::

            from sqlalchemy import case

            stmt = select(users_table).\
                        where(
                            case(
                                (users_table.c.name == 'wendy', 'W'),
                                (users_table.c.name == 'jack', 'J'),
                                else_='E'
                            )
                        )

        The above statement will produce SQL resembling::

            SELECT id, name FROM user
            WHERE CASE
                WHEN (name = :name_1) THEN :param_1
                WHEN (name = :name_2) THEN :param_2
                ELSE :param_3
            END

        When simple equality expressions of several values against a single
        parent column are needed, :func:`.case` also has a "shorthand" format
        used via the
        :paramref:`.case.value` parameter, which is passed a column
        expression to be compared.  In this form, the :paramref:`.case.whens`
        parameter is passed as a dictionary containing expressions to be
        compared against keyed to result expressions.  The statement below is
        equivalent to the preceding statement::

            stmt = select(users_table).\
                        where(
                            case(
                                whens={"wendy": "W", "jack": "J"},
                                value=users_table.c.name,
                                else_='E'
                            )
                        )

        The values which are accepted as result values in
        :paramref:`.case.whens` as well as with :paramref:`.case.else_` are
        coerced from Python literals into :func:`.bindparam` constructs.
        SQL expressions, e.g. :class:`_expression.ColumnElement` constructs,
        are accepted
        as well.  To coerce a literal string expression into a constant
        expression rendered inline, use the :func:`_expression.literal_column`
        construct,
        as in::

            from sqlalchemy import case, literal_column

            case(
                (
                    orderline.c.qty > 100,
                    literal_column("'greaterthan100'")
                ),
                (
                    orderline.c.qty > 10,
                    literal_column("'greaterthan10'")
                ),
                else_=literal_column("'lessthan10'")
            )

        The above will render the given constants without using bound
        parameters for the result values (but still for the comparison
        values), as in::

            CASE
                WHEN (orderline.qty > :qty_1) THEN 'greaterthan100'
                WHEN (orderline.qty > :qty_2) THEN 'greaterthan10'
                ELSE 'lessthan10'
            END

        :param \*whens: The criteria to be compared against,
         :paramref:`.case.whens` accepts two different forms, based on
         whether or not :paramref:`.case.value` is used.

         .. versionchanged:: 1.4 the :func:`_sql.case`
            function now accepts the series of WHEN conditions positionally;
            passing the expressions within a list is deprecated.

         In the first form, it accepts a list of 2-tuples; each 2-tuple
         consists of ``(<sql expression>, <value>)``, where the SQL
         expression is a boolean expression and "value" is a resulting value,
         e.g.::

            case(
                (users_table.c.name == 'wendy', 'W'),
                (users_table.c.name == 'jack', 'J')
            )

         In the second form, it accepts a Python dictionary of comparison
         values mapped to a resulting value; this form requires
         :paramref:`.case.value` to be present, and values will be compared
         using the ``==`` operator, e.g.::

            case(
                {"wendy": "W", "jack": "J"},
                value=users_table.c.name
            )

        :param value: An optional SQL expression which will be used as a
          fixed "comparison point" for candidate values within a dictionary
          passed to :paramref:`.case.whens`.

        :param else\_: An optional SQL expression which will be the evaluated
          result of the ``CASE`` construct if all expressions within
          :paramref:`.case.whens` evaluate to false.  When omitted, most
          databases will produce a result of NULL if none of the "when"
          expressions evaluate to true.


        """

        if "whens" in kw:
            util.warn_deprecated_20(
                'The "whens" argument to case() is now passed as a series of '
                "positional "
                "elements, rather than as a list. "
            )
            whens = kw.pop("whens")
        else:
            whens = coercions._expression_collection_was_a_list(
                "whens", "case", whens
            )
        try:
            whens = util.dictlike_iteritems(whens)
        except TypeError:
            pass

        value = kw.pop("value", None)
        if value is not None:
            whenlist = [
                (
                    coercions.expect(
                        roles.ExpressionElementRole,
                        c,
                        apply_propagate_attrs=self,
                    ).self_group(),
                    coercions.expect(roles.ExpressionElementRole, r),
                )
                for (c, r) in whens
            ]
        else:
            whenlist = [
                (
                    coercions.expect(
                        roles.ColumnArgumentRole, c, apply_propagate_attrs=self
                    ).self_group(),
                    coercions.expect(roles.ExpressionElementRole, r),
                )
                for (c, r) in whens
            ]

        if whenlist:
            type_ = list(whenlist[-1])[-1].type
        else:
            type_ = None

        if value is None:
            self.value = None
        else:
            self.value = coercions.expect(roles.ExpressionElementRole, value)

        self.type = type_
        self.whens = whenlist

        else_ = kw.pop("else_", None)
        if else_ is not None:
            self.else_ = coercions.expect(roles.ExpressionElementRole, else_)
        else:
            self.else_ = None

        if kw:
            raise TypeError("unknown arguments: %s" % (", ".join(sorted(kw))))

    @property
    def _from_objects(self):
        return list(
            itertools.chain(*[x._from_objects for x in self.get_children()])
        )


def literal_column(text, type_=None):
    r"""Produce a :class:`.ColumnClause` object that has the
    :paramref:`_expression.column.is_literal` flag set to True.

    :func:`_expression.literal_column` is similar to
    :func:`_expression.column`, except that
    it is more often used as a "standalone" column expression that renders
    exactly as stated; while :func:`_expression.column`
    stores a string name that
    will be assumed to be part of a table and may be quoted as such,
    :func:`_expression.literal_column` can be that,
    or any other arbitrary column-oriented
    expression.

    :param text: the text of the expression; can be any SQL expression.
      Quoting rules will not be applied. To specify a column-name expression
      which should be subject to quoting rules, use the :func:`column`
      function.

    :param type\_: an optional :class:`~sqlalchemy.types.TypeEngine`
      object which will
      provide result-set translation and additional expression semantics for
      this column. If left as ``None`` the type will be :class:`.NullType`.

    .. seealso::

        :func:`_expression.column`

        :func:`_expression.text`

        :ref:`sqlexpression_literal_column`

    """
    return ColumnClause(text, type_=type_, is_literal=True)


class Cast(WrapsColumnExpression, ColumnElement):
    """Represent a ``CAST`` expression.

    :class:`.Cast` is produced using the :func:`.cast` factory function,
    as in::

        from sqlalchemy import cast, Numeric

        stmt = select(cast(product_table.c.unit_price, Numeric(10, 4)))

    Details on :class:`.Cast` usage is at :func:`.cast`.

    .. seealso::

        :ref:`coretutorial_casts`

        :func:`.cast`

        :func:`.type_coerce` - an alternative to CAST that coerces the type
        on the Python side only, which is often sufficient to generate the
        correct SQL and data coercion.

    """

    __visit_name__ = "cast"

    _traverse_internals = [
        ("clause", InternalTraversal.dp_clauseelement),
        ("typeclause", InternalTraversal.dp_clauseelement),
    ]

    def __init__(self, expression, type_):
        r"""Produce a ``CAST`` expression.

        :func:`.cast` returns an instance of :class:`.Cast`.

        E.g.::

            from sqlalchemy import cast, Numeric

            stmt = select(cast(product_table.c.unit_price, Numeric(10, 4)))

        The above statement will produce SQL resembling::

            SELECT CAST(unit_price AS NUMERIC(10, 4)) FROM product

        The :func:`.cast` function performs two distinct functions when
        used.  The first is that it renders the ``CAST`` expression within
        the resulting SQL string.  The second is that it associates the given
        type (e.g. :class:`.TypeEngine` class or instance) with the column
        expression on the Python side, which means the expression will take
        on the expression operator behavior associated with that type,
        as well as the bound-value handling and result-row-handling behavior
        of the type.

        .. versionchanged:: 0.9.0 :func:`.cast` now applies the given type
           to the expression such that it takes effect on the bound-value,
           e.g. the Python-to-database direction, in addition to the
           result handling, e.g. database-to-Python, direction.

        An alternative to :func:`.cast` is the :func:`.type_coerce` function.
        This function performs the second task of associating an expression
        with a specific type, but does not render the ``CAST`` expression
        in SQL.

        :param expression: A SQL expression, such as a
         :class:`_expression.ColumnElement`
         expression or a Python string which will be coerced into a bound
         literal value.

        :param type\_: A :class:`.TypeEngine` class or instance indicating
         the type to which the ``CAST`` should apply.

        .. seealso::

            :ref:`coretutorial_casts`

            :func:`.type_coerce` - an alternative to CAST that coerces the type
            on the Python side only, which is often sufficient to generate the
            correct SQL and data coercion.


        """
        self.type = type_api.to_instance(type_)
        self.clause = coercions.expect(
            roles.ExpressionElementRole,
            expression,
            type_=self.type,
            apply_propagate_attrs=self,
        )
        self.typeclause = TypeClause(self.type)

    @property
    def _from_objects(self):
        return self.clause._from_objects

    @property
    def wrapped_column_expression(self):
        return self.clause


class TypeCoerce(WrapsColumnExpression, ColumnElement):
    """Represent a Python-side type-coercion wrapper.

    :class:`.TypeCoerce` supplies the :func:`_expression.type_coerce`
    function; see that function for usage details.

    .. versionchanged:: 1.1 The :func:`.type_coerce` function now produces
       a persistent :class:`.TypeCoerce` wrapper object rather than
       translating the given object in place.

    .. seealso::

        :func:`_expression.type_coerce`

        :func:`.cast`

    """

    __visit_name__ = "type_coerce"

    _traverse_internals = [
        ("clause", InternalTraversal.dp_clauseelement),
        ("type", InternalTraversal.dp_type),
    ]

    def __init__(self, expression, type_):
        r"""Associate a SQL expression with a particular type, without rendering
        ``CAST``.

        E.g.::

            from sqlalchemy import type_coerce

            stmt = select(type_coerce(log_table.date_string, StringDateTime()))

        The above construct will produce a :class:`.TypeCoerce` object, which
        does not modify the rendering in any way on the SQL side, with the
        possible exception of a generated label if used in a columns clause
        context::

            SELECT date_string AS date_string FROM log

        When result rows are fetched, the ``StringDateTime`` type processor
        will be applied to result rows on behalf of the ``date_string`` column.

        .. note:: the :func:`.type_coerce` construct does not render any
           SQL syntax of its own, including that it does not imply
           parenthesization.   Please use :meth:`.TypeCoerce.self_group`
           if explicit parenthesization is required.

        In order to provide a named label for the expression, use
        :meth:`_expression.ColumnElement.label`::

            stmt = select(
                type_coerce(log_table.date_string, StringDateTime()).label('date')
            )


        A type that features bound-value handling will also have that behavior
        take effect when literal values or :func:`.bindparam` constructs are
        passed to :func:`.type_coerce` as targets.
        For example, if a type implements the
        :meth:`.TypeEngine.bind_expression`
        method or :meth:`.TypeEngine.bind_processor` method or equivalent,
        these functions will take effect at statement compilation/execution
        time when a literal value is passed, as in::

            # bound-value handling of MyStringType will be applied to the
            # literal value "some string"
            stmt = select(type_coerce("some string", MyStringType))

        When using :func:`.type_coerce` with composed expressions, note that
        **parenthesis are not applied**.   If :func:`.type_coerce` is being
        used in an operator context where the parenthesis normally present from
        CAST are necessary, use the :meth:`.TypeCoerce.self_group` method::

            >>> some_integer = column("someint", Integer)
            >>> some_string = column("somestr", String)
            >>> expr = type_coerce(some_integer + 5, String) + some_string
            >>> print(expr)
            someint + :someint_1 || somestr
            >>> expr = type_coerce(some_integer + 5, String).self_group() + some_string
            >>> print(expr)
            (someint + :someint_1) || somestr

        :param expression: A SQL expression, such as a
         :class:`_expression.ColumnElement`
         expression or a Python string which will be coerced into a bound
         literal value.

        :param type\_: A :class:`.TypeEngine` class or instance indicating
         the type to which the expression is coerced.

        .. seealso::

            :ref:`coretutorial_casts`

            :func:`.cast`

        """  # noqa
        self.type = type_api.to_instance(type_)
        self.clause = coercions.expect(
            roles.ExpressionElementRole,
            expression,
            type_=self.type,
            apply_propagate_attrs=self,
        )

    @property
    def _from_objects(self):
        return self.clause._from_objects

    @HasMemoized.memoized_attribute
    def typed_expression(self):
        if isinstance(self.clause, BindParameter):
            bp = self.clause._clone()
            bp.type = self.type
            return bp
        else:
            return self.clause

    @property
    def wrapped_column_expression(self):
        return self.clause

    def self_group(self, against=None):
        grouped = self.clause.self_group(against=against)
        if grouped is not self.clause:
            return TypeCoerce(grouped, self.type)
        else:
            return self


class Extract(ColumnElement):
    """Represent a SQL EXTRACT clause, ``extract(field FROM expr)``."""

    __visit_name__ = "extract"

    _traverse_internals = [
        ("expr", InternalTraversal.dp_clauseelement),
        ("field", InternalTraversal.dp_string),
    ]

    def __init__(self, field, expr, **kwargs):
        """Return a :class:`.Extract` construct.

        This is typically available as :func:`.extract`
        as well as ``func.extract`` from the
        :data:`.func` namespace.

        """
        self.type = type_api.INTEGERTYPE
        self.field = field
        self.expr = coercions.expect(roles.ExpressionElementRole, expr)

    @property
    def _from_objects(self):
        return self.expr._from_objects


class _label_reference(ColumnElement):
    """Wrap a column expression as it appears in a 'reference' context.

    This expression is any that includes an _order_by_label_element,
    which is a Label, or a DESC / ASC construct wrapping a Label.

    The production of _label_reference() should occur when an expression
    is added to this context; this includes the ORDER BY or GROUP BY of a
    SELECT statement, as well as a few other places, such as the ORDER BY
    within an OVER clause.

    """

    __visit_name__ = "label_reference"

    _traverse_internals = [("element", InternalTraversal.dp_clauseelement)]

    def __init__(self, element):
        self.element = element

    @property
    def _from_objects(self):
        return ()


class _textual_label_reference(ColumnElement):
    __visit_name__ = "textual_label_reference"

    _traverse_internals = [("element", InternalTraversal.dp_string)]

    def __init__(self, element):
        self.element = element

    @util.memoized_property
    def _text_clause(self):
        return TextClause._create_text(self.element)


class UnaryExpression(ColumnElement):
    """Define a 'unary' expression.

    A unary expression has a single column expression
    and an operator.  The operator can be placed on the left
    (where it is called the 'operator') or right (where it is called the
    'modifier') of the column expression.

    :class:`.UnaryExpression` is the basis for several unary operators
    including those used by :func:`.desc`, :func:`.asc`, :func:`.distinct`,
    :func:`.nulls_first` and :func:`.nulls_last`.

    """

    __visit_name__ = "unary"

    _traverse_internals = [
        ("element", InternalTraversal.dp_clauseelement),
        ("operator", InternalTraversal.dp_operator),
        ("modifier", InternalTraversal.dp_operator),
    ]

    def __init__(
        self,
        element,
        operator=None,
        modifier=None,
        type_=None,
        wraps_column_expression=False,
    ):
        self.operator = operator
        self.modifier = modifier
        self._propagate_attrs = element._propagate_attrs
        self.element = element.self_group(
            against=self.operator or self.modifier
        )
        self.type = type_api.to_instance(type_)
        self.wraps_column_expression = wraps_column_expression

    @classmethod
    def _create_nulls_first(cls, column):
        """Produce the ``NULLS FIRST`` modifier for an ``ORDER BY`` expression.

        :func:`.nulls_first` is intended to modify the expression produced
        by :func:`.asc` or :func:`.desc`, and indicates how NULL values
        should be handled when they are encountered during ordering::


            from sqlalchemy import desc, nulls_first

            stmt = select(users_table).order_by(
                nulls_first(desc(users_table.c.name)))

        The SQL expression from the above would resemble::

            SELECT id, name FROM user ORDER BY name DESC NULLS FIRST

        Like :func:`.asc` and :func:`.desc`, :func:`.nulls_first` is typically
        invoked from the column expression itself using
        :meth:`_expression.ColumnElement.nulls_first`,
        rather than as its standalone
        function version, as in::

            stmt = select(users_table).order_by(
                users_table.c.name.desc().nulls_first())

        .. versionchanged:: 1.4 :func:`.nulls_first` is renamed from
            :func:`.nullsfirst` in previous releases.
            The previous name remains available for backwards compatibility.

        .. seealso::

            :func:`.asc`

            :func:`.desc`

            :func:`.nulls_last`

            :meth:`_expression.Select.order_by`

        """
        return UnaryExpression(
            coercions.expect(roles.ByOfRole, column),
            modifier=operators.nulls_first_op,
            wraps_column_expression=False,
        )

    @classmethod
    def _create_nulls_last(cls, column):
        """Produce the ``NULLS LAST`` modifier for an ``ORDER BY`` expression.

        :func:`.nulls_last` is intended to modify the expression produced
        by :func:`.asc` or :func:`.desc`, and indicates how NULL values
        should be handled when they are encountered during ordering::


            from sqlalchemy import desc, nulls_last

            stmt = select(users_table).order_by(
                nulls_last(desc(users_table.c.name)))

        The SQL expression from the above would resemble::

            SELECT id, name FROM user ORDER BY name DESC NULLS LAST

        Like :func:`.asc` and :func:`.desc`, :func:`.nulls_last` is typically
        invoked from the column expression itself using
        :meth:`_expression.ColumnElement.nulls_last`,
        rather than as its standalone
        function version, as in::

            stmt = select(users_table).order_by(
                users_table.c.name.desc().nulls_last())

        .. versionchanged:: 1.4 :func:`.nulls_last` is renamed from
            :func:`.nullslast` in previous releases.
            The previous name remains available for backwards compatibility.

        .. seealso::

            :func:`.asc`

            :func:`.desc`

            :func:`.nulls_first`

            :meth:`_expression.Select.order_by`

        """
        return UnaryExpression(
            coercions.expect(roles.ByOfRole, column),
            modifier=operators.nulls_last_op,
            wraps_column_expression=False,
        )

    @classmethod
    def _create_desc(cls, column):
        """Produce a descending ``ORDER BY`` clause element.

        e.g.::

            from sqlalchemy import desc

            stmt = select(users_table).order_by(desc(users_table.c.name))

        will produce SQL as::

            SELECT id, name FROM user ORDER BY name DESC

        The :func:`.desc` function is a standalone version of the
        :meth:`_expression.ColumnElement.desc`
        method available on all SQL expressions,
        e.g.::


            stmt = select(users_table).order_by(users_table.c.name.desc())

        :param column: A :class:`_expression.ColumnElement` (e.g.
         scalar SQL expression)
         with which to apply the :func:`.desc` operation.

        .. seealso::

            :func:`.asc`

            :func:`.nulls_first`

            :func:`.nulls_last`

            :meth:`_expression.Select.order_by`

        """
        return UnaryExpression(
            coercions.expect(roles.ByOfRole, column),
            modifier=operators.desc_op,
            wraps_column_expression=False,
        )

    @classmethod
    def _create_asc(cls, column):
        """Produce an ascending ``ORDER BY`` clause element.

        e.g.::

            from sqlalchemy import asc
            stmt = select(users_table).order_by(asc(users_table.c.name))

        will produce SQL as::

            SELECT id, name FROM user ORDER BY name ASC

        The :func:`.asc` function is a standalone version of the
        :meth:`_expression.ColumnElement.asc`
        method available on all SQL expressions,
        e.g.::


            stmt = select(users_table).order_by(users_table.c.name.asc())

        :param column: A :class:`_expression.ColumnElement` (e.g.
         scalar SQL expression)
         with which to apply the :func:`.asc` operation.

        .. seealso::

            :func:`.desc`

            :func:`.nulls_first`

            :func:`.nulls_last`

            :meth:`_expression.Select.order_by`

        """
        return UnaryExpression(
            coercions.expect(roles.ByOfRole, column),
            modifier=operators.asc_op,
            wraps_column_expression=False,
        )

    @classmethod
    def _create_distinct(cls, expr):
        """Produce an column-expression-level unary ``DISTINCT`` clause.

        This applies the ``DISTINCT`` keyword to an individual column
        expression, and is typically contained within an aggregate function,
        as in::

            from sqlalchemy import distinct, func
            stmt = select(func.count(distinct(users_table.c.name)))

        The above would produce an expression resembling::

            SELECT COUNT(DISTINCT name) FROM user

        The :func:`.distinct` function is also available as a column-level
        method, e.g. :meth:`_expression.ColumnElement.distinct`, as in::

            stmt = select(func.count(users_table.c.name.distinct()))

        The :func:`.distinct` operator is different from the
        :meth:`_expression.Select.distinct` method of
        :class:`_expression.Select`,
        which produces a ``SELECT`` statement
        with ``DISTINCT`` applied to the result set as a whole,
        e.g. a ``SELECT DISTINCT`` expression.  See that method for further
        information.

        .. seealso::

            :meth:`_expression.ColumnElement.distinct`

            :meth:`_expression.Select.distinct`

            :data:`.func`

        """
        expr = coercions.expect(roles.ExpressionElementRole, expr)
        return UnaryExpression(
            expr,
            operator=operators.distinct_op,
            type_=expr.type,
            wraps_column_expression=False,
        )

    @property
    def _order_by_label_element(self):
        if self.modifier in (operators.desc_op, operators.asc_op):
            return self.element._order_by_label_element
        else:
            return None

    @property
    def _from_objects(self):
        return self.element._from_objects

    def _negate(self):
        if self.type._type_affinity is type_api.BOOLEANTYPE._type_affinity:
            return UnaryExpression(
                self.self_group(against=operators.inv),
                operator=operators.inv,
                type_=type_api.BOOLEANTYPE,
                wraps_column_expression=self.wraps_column_expression,
            )
        else:
            return ClauseElement._negate(self)

    def self_group(self, against=None):
        if self.operator and operators.is_precedent(self.operator, against):
            return Grouping(self)
        else:
            return self


class CollectionAggregate(UnaryExpression):
    """Forms the basis for right-hand collection operator modifiers
    ANY and ALL.

    The ANY and ALL keywords are available in different ways on different
    backends.  On PostgreSQL, they only work for an ARRAY type.  On
    MySQL, they only work for subqueries.

    """

    @classmethod
    def _create_any(cls, expr):
        """Produce an ANY expression.

        This may apply to an array type for some dialects (e.g. postgresql),
        or to a subquery for others (e.g. mysql).  e.g.::

            # postgresql '5 = ANY (somearray)'
            expr = 5 == any_(mytable.c.somearray)

            # mysql '5 = ANY (SELECT value FROM table)'
            expr = 5 == any_(select(table.c.value))

        The operator is more conveniently available from any
        :class:`_sql.ColumnElement` object that makes use of the
        :class:`_types.ARRAY` datatype::

            expr = mytable.c.somearray.any(5)

        .. seealso::

            :func:`_expression.all_`

            :meth:`_types.ARRAY.any`

        """

        expr = coercions.expect(roles.ExpressionElementRole, expr)

        expr = expr.self_group()
        return CollectionAggregate(
            expr,
            operator=operators.any_op,
            type_=type_api.NULLTYPE,
            wraps_column_expression=False,
        )

    @classmethod
    def _create_all(cls, expr):
        """Produce an ALL expression.

        This may apply to an array type for some dialects (e.g. postgresql),
        or to a subquery for others (e.g. mysql).  e.g.::

            # postgresql '5 = ALL (somearray)'
            expr = 5 == all_(mytable.c.somearray)

            # mysql '5 = ALL (SELECT value FROM table)'
            expr = 5 == all_(select(table.c.value))

        The operator is more conveniently available from any
        :class:`_sql.ColumnElement` object that makes use of the
        :class:`_types.ARRAY` datatype::

            expr = mytable.c.somearray.all(5)

        .. seealso::

            :func:`_expression.any_`

            :meth:`_types.ARRAY.Comparator.all`

        """

        expr = coercions.expect(roles.ExpressionElementRole, expr)
        expr = expr.self_group()
        return CollectionAggregate(
            expr,
            operator=operators.all_op,
            type_=type_api.NULLTYPE,
            wraps_column_expression=False,
        )

    # operate and reverse_operate are hardwired to
    # dispatch onto the type comparator directly, so that we can
    # ensure "reversed" behavior.
    def operate(self, op, *other, **kwargs):
        if not operators.is_comparison(op):
            raise exc.ArgumentError(
                "Only comparison operators may be used with ANY/ALL"
            )
        kwargs["reverse"] = True
        return self.comparator.operate(operators.mirror(op), *other, **kwargs)

    def reverse_operate(self, op, other, **kwargs):
        # comparison operators should never call reverse_operate
        assert not operators.is_comparison(op)
        raise exc.ArgumentError(
            "Only comparison operators may be used with ANY/ALL"
        )


class AsBoolean(WrapsColumnExpression, UnaryExpression):
    inherit_cache = True

    def __init__(self, element, operator, negate):
        self.element = element
        self.type = type_api.BOOLEANTYPE
        self.operator = operator
        self.negate = negate
        self.modifier = None
        self.wraps_column_expression = True
        self._is_implicitly_boolean = element._is_implicitly_boolean

    @property
    def wrapped_column_expression(self):
        return self.element

    def self_group(self, against=None):
        return self

    def _negate(self):
        if isinstance(self.element, (True_, False_)):
            return self.element._negate()
        else:
            return AsBoolean(self.element, self.negate, self.operator)


class BinaryExpression(ColumnElement):
    """Represent an expression that is ``LEFT <operator> RIGHT``.

    A :class:`.BinaryExpression` is generated automatically
    whenever two column expressions are used in a Python binary expression::

        >>> from sqlalchemy.sql import column
        >>> column('a') + column('b')
        <sqlalchemy.sql.expression.BinaryExpression object at 0x101029dd0>
        >>> print(column('a') + column('b'))
        a + b

    """

    __visit_name__ = "binary"

    _traverse_internals = [
        ("left", InternalTraversal.dp_clauseelement),
        ("right", InternalTraversal.dp_clauseelement),
        ("operator", InternalTraversal.dp_operator),
        ("negate", InternalTraversal.dp_operator),
        ("modifiers", InternalTraversal.dp_plain_dict),
        (
            "type",
            InternalTraversal.dp_type,
        ),  # affects JSON CAST operators
    ]

    _is_implicitly_boolean = True
    """Indicates that any database will know this is a boolean expression
    even if the database does not have an explicit boolean datatype.

    """

    def __init__(
        self, left, right, operator, type_=None, negate=None, modifiers=None
    ):
        # allow compatibility with libraries that
        # refer to BinaryExpression directly and pass strings
        if isinstance(operator, util.string_types):
            operator = operators.custom_op(operator)
        self._orig = (left.__hash__(), right.__hash__())
        self._propagate_attrs = left._propagate_attrs or right._propagate_attrs
        self.left = left.self_group(against=operator)
        self.right = right.self_group(against=operator)
        self.operator = operator
        self.type = type_api.to_instance(type_)
        self.negate = negate
        self._is_implicitly_boolean = operators.is_boolean(operator)

        if modifiers is None:
            self.modifiers = {}
        else:
            self.modifiers = modifiers

    def __bool__(self):
        if self.operator in (operator.eq, operator.ne):
            return self.operator(*self._orig)
        else:
            raise TypeError("Boolean value of this clause is not defined")

    __nonzero__ = __bool__

    @property
    def is_comparison(self):
        return operators.is_comparison(self.operator)

    @property
    def _from_objects(self):
        return self.left._from_objects + self.right._from_objects

    def self_group(self, against=None):

        if operators.is_precedent(self.operator, against):
            return Grouping(self)
        else:
            return self

    def _negate(self):
        if self.negate is not None:
            return BinaryExpression(
                self.left,
                self.right._negate_in_binary(self.negate, self.operator),
                self.negate,
                negate=self.operator,
                type_=self.type,
                modifiers=self.modifiers,
            )
        else:
            return super(BinaryExpression, self)._negate()


class Slice(ColumnElement):
    """Represent SQL for a Python array-slice object.

    This is not a specific SQL construct at this level, but
    may be interpreted by specific dialects, e.g. PostgreSQL.

    """

    __visit_name__ = "slice"

    _traverse_internals = [
        ("start", InternalTraversal.dp_clauseelement),
        ("stop", InternalTraversal.dp_clauseelement),
        ("step", InternalTraversal.dp_clauseelement),
    ]

    def __init__(self, start, stop, step, _name=None):
        self.start = coercions.expect(
            roles.ExpressionElementRole,
            start,
            name=_name,
            type_=type_api.INTEGERTYPE,
        )
        self.stop = coercions.expect(
            roles.ExpressionElementRole,
            stop,
            name=_name,
            type_=type_api.INTEGERTYPE,
        )
        self.step = coercions.expect(
            roles.ExpressionElementRole,
            step,
            name=_name,
            type_=type_api.INTEGERTYPE,
        )
        self.type = type_api.NULLTYPE

    def self_group(self, against=None):
        assert against is operator.getitem
        return self


class IndexExpression(BinaryExpression):
    """Represent the class of expressions that are like an "index"
    operation."""

    pass


class GroupedElement(ClauseElement):
    """Represent any parenthesized expression"""

    __visit_name__ = "grouping"

    def self_group(self, against=None):
        return self

    def _ungroup(self):
        return self.element._ungroup()


class Grouping(GroupedElement, ColumnElement):
    """Represent a grouping within a column expression"""

    _traverse_internals = [
        ("element", InternalTraversal.dp_clauseelement),
        ("type", InternalTraversal.dp_type),
    ]

    def __init__(self, element):
        self.element = element
        self.type = getattr(element, "type", type_api.NULLTYPE)

    def _with_binary_element_type(self, type_):
        return self.__class__(self.element._with_binary_element_type(type_))

    @util.memoized_property
    def _is_implicitly_boolean(self):
        return self.element._is_implicitly_boolean

    @property
    def _tq_label(self):
        return (
            getattr(self.element, "_tq_label", None) or self._anon_name_label
        )

    @property
    def _proxies(self):
        if isinstance(self.element, ColumnElement):
            return [self.element]
        else:
            return []

    @property
    def _from_objects(self):
        return self.element._from_objects

    def __getattr__(self, attr):
        return getattr(self.element, attr)

    def __getstate__(self):
        return {"element": self.element, "type": self.type}

    def __setstate__(self, state):
        self.element = state["element"]
        self.type = state["type"]


RANGE_UNBOUNDED = util.symbol("RANGE_UNBOUNDED")
RANGE_CURRENT = util.symbol("RANGE_CURRENT")


class Over(ColumnElement):
    """Represent an OVER clause.

    This is a special operator against a so-called
    "window" function, as well as any aggregate function,
    which produces results relative to the result set
    itself.  Most modern SQL backends now support window functions.

    """

    __visit_name__ = "over"

    _traverse_internals = [
        ("element", InternalTraversal.dp_clauseelement),
        ("order_by", InternalTraversal.dp_clauseelement),
        ("partition_by", InternalTraversal.dp_clauseelement),
        ("range_", InternalTraversal.dp_plain_obj),
        ("rows", InternalTraversal.dp_plain_obj),
    ]

    order_by = None
    partition_by = None

    element = None
    """The underlying expression object to which this :class:`.Over`
    object refers towards."""

    def __init__(
        self, element, partition_by=None, order_by=None, range_=None, rows=None
    ):
        r"""Produce an :class:`.Over` object against a function.

        Used against aggregate or so-called "window" functions,
        for database backends that support window functions.

        :func:`_expression.over` is usually called using
        the :meth:`.FunctionElement.over` method, e.g.::

            func.row_number().over(order_by=mytable.c.some_column)

        Would produce::

            ROW_NUMBER() OVER(ORDER BY some_column)

        Ranges are also possible using the :paramref:`.expression.over.range_`
        and :paramref:`.expression.over.rows` parameters.  These
        mutually-exclusive parameters each accept a 2-tuple, which contains
        a combination of integers and None::

            func.row_number().over(
                order_by=my_table.c.some_column, range_=(None, 0))

        The above would produce::

            ROW_NUMBER() OVER(ORDER BY some_column
            RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

        A value of ``None`` indicates "unbounded", a
        value of zero indicates "current row", and negative / positive
        integers indicate "preceding" and "following":

        * RANGE BETWEEN 5 PRECEDING AND 10 FOLLOWING::

            func.row_number().over(order_by='x', range_=(-5, 10))

        * ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW::

            func.row_number().over(order_by='x', rows=(None, 0))

        * RANGE BETWEEN 2 PRECEDING AND UNBOUNDED FOLLOWING::

            func.row_number().over(order_by='x', range_=(-2, None))

        * RANGE BETWEEN 1 FOLLOWING AND 3 FOLLOWING::

            func.row_number().over(order_by='x', range_=(1, 3))

        .. versionadded:: 1.1 support for RANGE / ROWS within a window


        :param element: a :class:`.FunctionElement`, :class:`.WithinGroup`,
         or other compatible construct.
        :param partition_by: a column element or string, or a list
         of such, that will be used as the PARTITION BY clause
         of the OVER construct.
        :param order_by: a column element or string, or a list
         of such, that will be used as the ORDER BY clause
         of the OVER construct.
        :param range\_: optional range clause for the window.  This is a
         tuple value which can contain integer values or ``None``,
         and will render a RANGE BETWEEN PRECEDING / FOLLOWING clause.

         .. versionadded:: 1.1

        :param rows: optional rows clause for the window.  This is a tuple
         value which can contain integer values or None, and will render
         a ROWS BETWEEN PRECEDING / FOLLOWING clause.

         .. versionadded:: 1.1

        This function is also available from the :data:`~.expression.func`
        construct itself via the :meth:`.FunctionElement.over` method.

        .. seealso::

            :ref:`tutorial_window_functions` - in the :ref:`unified_tutorial`

            :data:`.expression.func`

            :func:`_expression.within_group`

        """
        self.element = element
        if order_by is not None:
            self.order_by = ClauseList(
                *util.to_list(order_by), _literal_as_text_role=roles.ByOfRole
            )
        if partition_by is not None:
            self.partition_by = ClauseList(
                *util.to_list(partition_by),
                _literal_as_text_role=roles.ByOfRole
            )

        if range_:
            self.range_ = self._interpret_range(range_)
            if rows:
                raise exc.ArgumentError(
                    "'range_' and 'rows' are mutually exclusive"
                )
            else:
                self.rows = None
        elif rows:
            self.rows = self._interpret_range(rows)
            self.range_ = None
        else:
            self.rows = self.range_ = None

    def __reduce__(self):
        return self.__class__, (
            self.element,
            self.partition_by,
            self.order_by,
            self.range_,
            self.rows,
        )

    def _interpret_range(self, range_):
        if not isinstance(range_, tuple) or len(range_) != 2:
            raise exc.ArgumentError("2-tuple expected for range/rows")

        if range_[0] is None:
            lower = RANGE_UNBOUNDED
        else:
            try:
                lower = int(range_[0])
            except ValueError as err:
                util.raise_(
                    exc.ArgumentError(
                        "Integer or None expected for range value"
                    ),
                    replace_context=err,
                )
            else:
                if lower == 0:
                    lower = RANGE_CURRENT

        if range_[1] is None:
            upper = RANGE_UNBOUNDED
        else:
            try:
                upper = int(range_[1])
            except ValueError as err:
                util.raise_(
                    exc.ArgumentError(
                        "Integer or None expected for range value"
                    ),
                    replace_context=err,
                )
            else:
                if upper == 0:
                    upper = RANGE_CURRENT

        return lower, upper

    @util.memoized_property
    def type(self):
        return self.element.type

    @property
    def _from_objects(self):
        return list(
            itertools.chain(
                *[
                    c._from_objects
                    for c in (self.element, self.partition_by, self.order_by)
                    if c is not None
                ]
            )
        )


class WithinGroup(ColumnElement):
    """Represent a WITHIN GROUP (ORDER BY) clause.

    This is a special operator against so-called
    "ordered set aggregate" and "hypothetical
    set aggregate" functions, including ``percentile_cont()``,
    ``rank()``, ``dense_rank()``, etc.

    It's supported only by certain database backends, such as PostgreSQL,
    Oracle and MS SQL Server.

    The :class:`.WithinGroup` construct extracts its type from the
    method :meth:`.FunctionElement.within_group_type`.  If this returns
    ``None``, the function's ``.type`` is used.

    """

    __visit_name__ = "withingroup"

    _traverse_internals = [
        ("element", InternalTraversal.dp_clauseelement),
        ("order_by", InternalTraversal.dp_clauseelement),
    ]

    order_by = None

    def __init__(self, element, *order_by):
        r"""Produce a :class:`.WithinGroup` object against a function.

        Used against so-called "ordered set aggregate" and "hypothetical
        set aggregate" functions, including :class:`.percentile_cont`,
        :class:`.rank`, :class:`.dense_rank`, etc.

        :func:`_expression.within_group` is usually called using
        the :meth:`.FunctionElement.within_group` method, e.g.::

            from sqlalchemy import within_group
            stmt = select(
                department.c.id,
                func.percentile_cont(0.5).within_group(
                    department.c.salary.desc()
                )
            )

        The above statement would produce SQL similar to
        ``SELECT department.id, percentile_cont(0.5)
        WITHIN GROUP (ORDER BY department.salary DESC)``.

        :param element: a :class:`.FunctionElement` construct, typically
         generated by :data:`~.expression.func`.
        :param \*order_by: one or more column elements that will be used
         as the ORDER BY clause of the WITHIN GROUP construct.

        .. versionadded:: 1.1

        .. seealso::

            :ref:`tutorial_functions_within_group` - in the
            :ref:`unified_tutorial`

            :data:`.expression.func`

            :func:`_expression.over`

        """
        self.element = element
        if order_by is not None:
            self.order_by = ClauseList(
                *util.to_list(order_by), _literal_as_text_role=roles.ByOfRole
            )

    def over(self, partition_by=None, order_by=None, range_=None, rows=None):
        """Produce an OVER clause against this :class:`.WithinGroup`
        construct.

        This function has the same signature as that of
        :meth:`.FunctionElement.over`.

        """
        return Over(
            self,
            partition_by=partition_by,
            order_by=order_by,
            range_=range_,
            rows=rows,
        )

    @util.memoized_property
    def type(self):
        wgt = self.element.within_group_type(self)
        if wgt is not None:
            return wgt
        else:
            return self.element.type

    @property
    def _from_objects(self):
        return list(
            itertools.chain(
                *[
                    c._from_objects
                    for c in (self.element, self.order_by)
                    if c is not None
                ]
            )
        )


class FunctionFilter(ColumnElement):
    """Represent a function FILTER clause.

    This is a special operator against aggregate and window functions,
    which controls which rows are passed to it.
    It's supported only by certain database backends.

    Invocation of :class:`.FunctionFilter` is via
    :meth:`.FunctionElement.filter`::

        func.count(1).filter(True)

    .. versionadded:: 1.0.0

    .. seealso::

        :meth:`.FunctionElement.filter`

    """

    __visit_name__ = "funcfilter"

    _traverse_internals = [
        ("func", InternalTraversal.dp_clauseelement),
        ("criterion", InternalTraversal.dp_clauseelement),
    ]

    criterion = None

    def __init__(self, func, *criterion):
        """Produce a :class:`.FunctionFilter` object against a function.

        Used against aggregate and window functions,
        for database backends that support the "FILTER" clause.

        E.g.::

            from sqlalchemy import funcfilter
            funcfilter(func.count(1), MyClass.name == 'some name')

        Would produce "COUNT(1) FILTER (WHERE myclass.name = 'some name')".

        This function is also available from the :data:`~.expression.func`
        construct itself via the :meth:`.FunctionElement.filter` method.

        .. versionadded:: 1.0.0

        .. seealso::

            :ref:`tutorial_functions_within_group` - in the
            :ref:`unified_tutorial`

            :meth:`.FunctionElement.filter`

        """
        self.func = func
        self.filter(*criterion)

    def filter(self, *criterion):
        """Produce an additional FILTER against the function.

        This method adds additional criteria to the initial criteria
        set up by :meth:`.FunctionElement.filter`.

        Multiple criteria are joined together at SQL render time
        via ``AND``.


        """

        for criterion in list(criterion):
            criterion = coercions.expect(roles.WhereHavingRole, criterion)

            if self.criterion is not None:
                self.criterion = self.criterion & criterion
            else:
                self.criterion = criterion

        return self

    def over(self, partition_by=None, order_by=None, range_=None, rows=None):
        """Produce an OVER clause against this filtered function.

        Used against aggregate or so-called "window" functions,
        for database backends that support window functions.

        The expression::

            func.rank().filter(MyClass.y > 5).over(order_by='x')

        is shorthand for::

            from sqlalchemy import over, funcfilter
            over(funcfilter(func.rank(), MyClass.y > 5), order_by='x')

        See :func:`_expression.over` for a full description.

        """
        return Over(
            self,
            partition_by=partition_by,
            order_by=order_by,
            range_=range_,
            rows=rows,
        )

    def self_group(self, against=None):
        if operators.is_precedent(operators.filter_op, against):
            return Grouping(self)
        else:
            return self

    @util.memoized_property
    def type(self):
        return self.func.type

    @property
    def _from_objects(self):
        return list(
            itertools.chain(
                *[
                    c._from_objects
                    for c in (self.func, self.criterion)
                    if c is not None
                ]
            )
        )


class Label(roles.LabeledColumnExprRole, ColumnElement):
    """Represents a column label (AS).

    Represent a label, as typically applied to any column-level
    element using the ``AS`` sql keyword.

    """

    __visit_name__ = "label"

    _traverse_internals = [
        ("name", InternalTraversal.dp_anon_name),
        ("_type", InternalTraversal.dp_type),
        ("_element", InternalTraversal.dp_clauseelement),
    ]

    def __init__(self, name, element, type_=None):
        """Return a :class:`Label` object for the
        given :class:`_expression.ColumnElement`.

        A label changes the name of an element in the columns clause of a
        ``SELECT`` statement, typically via the ``AS`` SQL keyword.

        This functionality is more conveniently available via the
        :meth:`_expression.ColumnElement.label` method on
        :class:`_expression.ColumnElement`.

        :param name: label name

        :param obj: a :class:`_expression.ColumnElement`.

        """

        if isinstance(element, Label):
            self._resolve_label = element._label

        while isinstance(element, Label):
            element = element.element

        if name:
            self.name = name
            self._resolve_label = self.name
        else:
            self.name = _anonymous_label.safe_construct(
                id(self), getattr(element, "name", "anon")
            )

        self.key = self._tq_label = self._tq_key_label = self.name
        self._element = element
        self._type = type_
        self._proxies = [element]

    def __reduce__(self):
        return self.__class__, (self.name, self._element, self._type)

    @util.memoized_property
    def _is_implicitly_boolean(self):
        return self.element._is_implicitly_boolean

    @HasMemoized.memoized_attribute
    def _allow_label_resolve(self):
        return self.element._allow_label_resolve

    @property
    def _order_by_label_element(self):
        return self

    @util.memoized_property
    def type(self):
        return type_api.to_instance(
            self._type or getattr(self._element, "type", None)
        )

    @HasMemoized.memoized_attribute
    def element(self):
        return self._element.self_group(against=operators.as_)

    def self_group(self, against=None):
        return self._apply_to_inner(self._element.self_group, against=against)

    def _negate(self):
        return self._apply_to_inner(self._element._negate)

    def _apply_to_inner(self, fn, *arg, **kw):
        sub_element = fn(*arg, **kw)
        if sub_element is not self._element:
            return Label(self.name, sub_element, type_=self._type)
        else:
            return self

    @property
    def primary_key(self):
        return self.element.primary_key

    @property
    def foreign_keys(self):
        return self.element.foreign_keys

    def _copy_internals(self, clone=_clone, anonymize_labels=False, **kw):
        self._reset_memoizations()
        self._element = clone(self._element, **kw)
        if anonymize_labels:
            self.name = self._resolve_label = _anonymous_label.safe_construct(
                id(self), getattr(self.element, "name", "anon")
            )
            self.key = self._tq_label = self._tq_key_label = self.name

    @property
    def _from_objects(self):
        return self.element._from_objects

    def _make_proxy(self, selectable, name=None, **kw):
        name = self.name if not name else name

        key, e = self.element._make_proxy(
            selectable,
            name=name,
            disallow_is_literal=True,
            name_is_truncatable=isinstance(name, _truncated_label),
        )

        # there was a note here to remove this assertion, which was here
        # to determine if we later could support a use case where
        # the key and name of a label are separate.  But I don't know what
        # that case was.  For now, this is an unexpected case that occurs
        # when a label name conflicts with other columns and select()
        # is attempting to disambiguate an explicit label, which is not what
        # the user would want.   See issue #6090.
        if key != self.name:
            raise exc.InvalidRequestError(
                "Label name %s is being renamed to an anonymous label due "
                "to disambiguation "
                "which is not supported right now.  Please use unique names "
                "for explicit labels." % (self.name)
            )

        e._propagate_attrs = selectable._propagate_attrs
        e._proxies.append(self)
        if self._type is not None:
            e.type = self._type

        return self.key, e


class NamedColumn(ColumnElement):
    is_literal = False
    table = None

    def _compare_name_for_result(self, other):
        return (hasattr(other, "name") and self.name == other.name) or (
            hasattr(other, "_label") and self._label == other._label
        )

    @util.memoized_property
    def description(self):
        if util.py3k:
            return self.name
        else:
            return self.name.encode("ascii", "backslashreplace")

    @HasMemoized.memoized_attribute
    def _tq_key_label(self):
        """table qualified label based on column key.

        for table-bound columns this is <tablename>_<column key/proxy key>;

        all other expressions it resolves to key/proxy key.

        """
        proxy_key = self._proxy_key
        if proxy_key and proxy_key != self.name:
            return self._gen_tq_label(proxy_key)
        else:
            return self._tq_label

    @HasMemoized.memoized_attribute
    def _tq_label(self):
        """table qualified label based on column name.

        for table-bound columns this is <tablename>_<columnname>; all other
        expressions it resolves to .name.

        """
        return self._gen_tq_label(self.name)

    @HasMemoized.memoized_attribute
    def _render_label_in_columns_clause(self):
        return True

    @HasMemoized.memoized_attribute
    def _non_anon_label(self):
        return self.name

    def _gen_tq_label(self, name, dedupe_on_key=True):
        return name

    def _bind_param(self, operator, obj, type_=None, expanding=False):
        return BindParameter(
            self.key,
            obj,
            _compared_to_operator=operator,
            _compared_to_type=self.type,
            type_=type_,
            unique=True,
            expanding=expanding,
        )

    def _make_proxy(
        self,
        selectable,
        name=None,
        name_is_truncatable=False,
        disallow_is_literal=False,
        **kw
    ):
        c = ColumnClause(
            coercions.expect(roles.TruncatedLabelRole, name or self.name)
            if name_is_truncatable
            else (name or self.name),
            type_=self.type,
            _selectable=selectable,
            is_literal=False,
        )
        c._propagate_attrs = selectable._propagate_attrs
        if name is None:
            c.key = self.key
        c._proxies = [self]
        if selectable._is_clone_of is not None:
            c._is_clone_of = selectable._is_clone_of.columns.get(c.key)
        return c.key, c


class ColumnClause(
    roles.DDLReferredColumnRole,
    roles.LabeledColumnExprRole,
    roles.StrAsPlainColumnRole,
    Immutable,
    NamedColumn,
):
    """Represents a column expression from any textual string.

    The :class:`.ColumnClause`, a lightweight analogue to the
    :class:`_schema.Column` class, is typically invoked using the
    :func:`_expression.column` function, as in::

        from sqlalchemy import column

        id, name = column("id"), column("name")
        stmt = select(id, name).select_from("user")

    The above statement would produce SQL like::

        SELECT id, name FROM user

    :class:`.ColumnClause` is the immediate superclass of the schema-specific
    :class:`_schema.Column` object.  While the :class:`_schema.Column`
    class has all the
    same capabilities as :class:`.ColumnClause`, the :class:`.ColumnClause`
    class is usable by itself in those cases where behavioral requirements
    are limited to simple SQL expression generation.  The object has none of
    the associations with schema-level metadata or with execution-time
    behavior that :class:`_schema.Column` does,
    so in that sense is a "lightweight"
    version of :class:`_schema.Column`.

    Full details on :class:`.ColumnClause` usage is at
    :func:`_expression.column`.

    .. seealso::

        :func:`_expression.column`

        :class:`_schema.Column`

    """

    table = None
    is_literal = False

    __visit_name__ = "column"

    _traverse_internals = [
        ("name", InternalTraversal.dp_anon_name),
        ("type", InternalTraversal.dp_type),
        ("table", InternalTraversal.dp_clauseelement),
        ("is_literal", InternalTraversal.dp_boolean),
    ]

    onupdate = default = server_default = server_onupdate = None

    _is_multiparam_column = False

    def __init__(self, text, type_=None, is_literal=False, _selectable=None):
        """Produce a :class:`.ColumnClause` object.

        The :class:`.ColumnClause` is a lightweight analogue to the
        :class:`_schema.Column` class.  The :func:`_expression.column`
        function can
        be invoked with just a name alone, as in::

            from sqlalchemy import column

            id, name = column("id"), column("name")
            stmt = select(id, name).select_from("user")

        The above statement would produce SQL like::

            SELECT id, name FROM user

        Once constructed, :func:`_expression.column`
        may be used like any other SQL
        expression element such as within :func:`_expression.select`
        constructs::

            from sqlalchemy.sql import column

            id, name = column("id"), column("name")
            stmt = select(id, name).select_from("user")

        The text handled by :func:`_expression.column`
        is assumed to be handled
        like the name of a database column; if the string contains mixed case,
        special characters, or matches a known reserved word on the target
        backend, the column expression will render using the quoting
        behavior determined by the backend.  To produce a textual SQL
        expression that is rendered exactly without any quoting,
        use :func:`_expression.literal_column` instead,
        or pass ``True`` as the
        value of :paramref:`_expression.column.is_literal`.   Additionally,
        full SQL
        statements are best handled using the :func:`_expression.text`
        construct.

        :func:`_expression.column` can be used in a table-like
        fashion by combining it with the :func:`.table` function
        (which is the lightweight analogue to :class:`_schema.Table`
        ) to produce
        a working table construct with minimal boilerplate::

            from sqlalchemy import table, column, select

            user = table("user",
                    column("id"),
                    column("name"),
                    column("description"),
            )

            stmt = select(user.c.description).where(user.c.name == 'wendy')

        A :func:`_expression.column` / :func:`.table`
        construct like that illustrated
        above can be created in an
        ad-hoc fashion and is not associated with any
        :class:`_schema.MetaData`, DDL, or events, unlike its
        :class:`_schema.Table` counterpart.

        .. versionchanged:: 1.0.0 :func:`_expression.column` can now
           be imported from the plain ``sqlalchemy`` namespace like any
           other SQL element.

        :param text: the text of the element.

        :param type: :class:`_types.TypeEngine` object which can associate
          this :class:`.ColumnClause` with a type.

        :param is_literal: if True, the :class:`.ColumnClause` is assumed to
          be an exact expression that will be delivered to the output with no
          quoting rules applied regardless of case sensitive settings. the
          :func:`_expression.literal_column()` function essentially invokes
          :func:`_expression.column` while passing ``is_literal=True``.

        .. seealso::

            :class:`_schema.Column`

            :func:`_expression.literal_column`

            :func:`.table`

            :func:`_expression.text`

            :ref:`sqlexpression_literal_column`

        """
        self.key = self.name = text
        self.table = _selectable
        self.type = type_api.to_instance(type_)
        self.is_literal = is_literal

    def get_children(self, column_tables=False, **kw):
        # override base get_children() to not return the Table
        # or selectable that is parent to this column.  Traversals
        # expect the columns of tables and subqueries to be leaf nodes.
        return []

    @property
    def entity_namespace(self):
        if self.table is not None:
            return self.table.entity_namespace
        else:
            return super(ColumnClause, self).entity_namespace

    @HasMemoized.memoized_attribute
    def _from_objects(self):
        t = self.table
        if t is not None:
            return [t]
        else:
            return []

    @HasMemoized.memoized_attribute
    def _render_label_in_columns_clause(self):
        return self.table is not None

    @property
    def _ddl_label(self):
        return self._gen_tq_label(self.name, dedupe_on_key=False)

    def _compare_name_for_result(self, other):
        if (
            self.is_literal
            or self.table is None
            or self.table._is_textual
            or not hasattr(other, "proxy_set")
            or (
                isinstance(other, ColumnClause)
                and (
                    other.is_literal
                    or other.table is None
                    or other.table._is_textual
                )
            )
        ):
            return (hasattr(other, "name") and self.name == other.name) or (
                hasattr(other, "_tq_label")
                and self._tq_label == other._tq_label
            )
        else:
            return other.proxy_set.intersection(self.proxy_set)

    def _gen_tq_label(self, name, dedupe_on_key=True):
        """generate table-qualified label

        for a table-bound column this is <tablename>_<columnname>.

        used primarily for LABEL_STYLE_TABLENAME_PLUS_COL
        as well as the .columns collection on a Join object.

        """
        t = self.table
        if self.is_literal:
            return None
        elif t is not None and t.named_with_column:
            if getattr(t, "schema", None):
                label = t.schema.replace(".", "_") + "_" + t.name + "_" + name
            else:
                label = t.name + "_" + name

            # propagate name quoting rules for labels.
            if getattr(name, "quote", None) is not None:
                if isinstance(label, quoted_name):
                    label.quote = name.quote
                else:
                    label = quoted_name(label, name.quote)
            elif getattr(t.name, "quote", None) is not None:
                # can't get this situation to occur, so let's
                # assert false on it for now
                assert not isinstance(label, quoted_name)
                label = quoted_name(label, t.name.quote)

            if dedupe_on_key:
                # ensure the label name doesn't conflict with that of an
                # existing column.   note that this implies that any Column
                # must **not** set up its _label before its parent table has
                # all of its other Column objects set up.  There are several
                # tables in the test suite which will fail otherwise; example:
                # table "owner" has columns "name" and "owner_name".  Therefore
                # column owner.name cannot use the label "owner_name", it has
                # to be "owner_name_1".
                if label in t.c:
                    _label = label
                    counter = 1
                    while _label in t.c:
                        _label = label + "_" + str(counter)
                        counter += 1
                    label = _label

            return coercions.expect(roles.TruncatedLabelRole, label)

        else:
            return name

    def _make_proxy(
        self,
        selectable,
        name=None,
        name_is_truncatable=False,
        disallow_is_literal=False,
        **kw
    ):
        # the "is_literal" flag normally should never be propagated; a proxied
        # column is always a SQL identifier and never the actual expression
        # being evaluated. however, there is a case where the "is_literal" flag
        # might be used to allow the given identifier to have a fixed quoting
        # pattern already, so maintain the flag for the proxy unless a
        # :class:`.Label` object is creating the proxy.  See [ticket:4730].
        is_literal = (
            not disallow_is_literal
            and self.is_literal
            and (
                # note this does not accommodate for quoted_name differences
                # right now
                name is None
                or name == self.name
            )
        )
        c = self._constructor(
            coercions.expect(roles.TruncatedLabelRole, name or self.name)
            if name_is_truncatable
            else (name or self.name),
            type_=self.type,
            _selectable=selectable,
            is_literal=is_literal,
        )
        c._propagate_attrs = selectable._propagate_attrs
        if name is None:
            c.key = self.key
        c._proxies = [self]
        if selectable._is_clone_of is not None:
            c._is_clone_of = selectable._is_clone_of.columns.get(c.key)
        return c.key, c


class TableValuedColumn(NamedColumn):
    __visit_name__ = "table_valued_column"

    _traverse_internals = [
        ("name", InternalTraversal.dp_anon_name),
        ("type", InternalTraversal.dp_type),
        ("scalar_alias", InternalTraversal.dp_clauseelement),
    ]

    def __init__(self, scalar_alias, type_):
        self.scalar_alias = scalar_alias
        self.key = self.name = scalar_alias.name
        self.type = type_

    @property
    def _from_objects(self):
        return [self.scalar_alias]


class CollationClause(ColumnElement):
    __visit_name__ = "collation"

    _traverse_internals = [("collation", InternalTraversal.dp_string)]

    def __init__(self, collation):
        self.collation = collation


class _IdentifiedClause(Executable, ClauseElement):

    __visit_name__ = "identified"
    _execution_options = Executable._execution_options.union(
        {"autocommit": False}
    )

    def __init__(self, ident):
        self.ident = ident


class SavepointClause(_IdentifiedClause):
    __visit_name__ = "savepoint"


class RollbackToSavepointClause(_IdentifiedClause):
    __visit_name__ = "rollback_to_savepoint"


class ReleaseSavepointClause(_IdentifiedClause):
    __visit_name__ = "release_savepoint"


class quoted_name(util.MemoizedSlots, util.text_type):
    """Represent a SQL identifier combined with quoting preferences.

    :class:`.quoted_name` is a Python unicode/str subclass which
    represents a particular identifier name along with a
    ``quote`` flag.  This ``quote`` flag, when set to
    ``True`` or ``False``, overrides automatic quoting behavior
    for this identifier in order to either unconditionally quote
    or to not quote the name.  If left at its default of ``None``,
    quoting behavior is applied to the identifier on a per-backend basis
    based on an examination of the token itself.

    A :class:`.quoted_name` object with ``quote=True`` is also
    prevented from being modified in the case of a so-called
    "name normalize" option.  Certain database backends, such as
    Oracle, Firebird, and DB2 "normalize" case-insensitive names
    as uppercase.  The SQLAlchemy dialects for these backends
    convert from SQLAlchemy's lower-case-means-insensitive convention
    to the upper-case-means-insensitive conventions of those backends.
    The ``quote=True`` flag here will prevent this conversion from occurring
    to support an identifier that's quoted as all lower case against
    such a backend.

    The :class:`.quoted_name` object is normally created automatically
    when specifying the name for key schema constructs such as
    :class:`_schema.Table`, :class:`_schema.Column`, and others.
    The class can also be
    passed explicitly as the name to any function that receives a name which
    can be quoted.  Such as to use the :meth:`_engine.Engine.has_table`
    method with
    an unconditionally quoted name::

        from sqlalchemy import create_engine
        from sqlalchemy.sql import quoted_name

        engine = create_engine("oracle+cx_oracle://some_dsn")
        engine.has_table(quoted_name("some_table", True))

    The above logic will run the "has table" logic against the Oracle backend,
    passing the name exactly as ``"some_table"`` without converting to
    upper case.

    .. versionadded:: 0.9.0

    .. versionchanged:: 1.2 The :class:`.quoted_name` construct is now
       importable from ``sqlalchemy.sql``, in addition to the previous
       location of ``sqlalchemy.sql.elements``.

    """

    __slots__ = "quote", "lower", "upper"

    def __new__(cls, value, quote):
        if value is None:
            return None
        # experimental - don't bother with quoted_name
        # if quote flag is None.  doesn't seem to make any dent
        # in performance however
        # elif not sprcls and quote is None:
        #   return value
        elif isinstance(value, cls) and (
            quote is None or value.quote == quote
        ):
            return value
        self = super(quoted_name, cls).__new__(cls, value)

        self.quote = quote
        return self

    def __reduce__(self):
        return quoted_name, (util.text_type(self), self.quote)

    def _memoized_method_lower(self):
        if self.quote:
            return self
        else:
            return util.text_type(self).lower()

    def _memoized_method_upper(self):
        if self.quote:
            return self
        else:
            return util.text_type(self).upper()

    def __repr__(self):
        if util.py2k:
            backslashed = self.encode("ascii", "backslashreplace")
            if not util.py2k:
                backslashed = backslashed.decode("ascii")
            return "'%s'" % backslashed
        else:
            return str.__repr__(self)


def _find_columns(clause):
    """locate Column objects within the given expression."""

    cols = util.column_set()
    traverse(clause, {}, {"column": cols.add})
    return cols


def _type_from_args(args):
    for a in args:
        if not a.type._isnull:
            return a.type
    else:
        return type_api.NULLTYPE


def _corresponding_column_or_error(fromclause, column, require_embedded=False):
    c = fromclause.corresponding_column(
        column, require_embedded=require_embedded
    )
    if c is None:
        raise exc.InvalidRequestError(
            "Given column '%s', attached to table '%s', "
            "failed to locate a corresponding column from table '%s'"
            % (column, getattr(column, "table", None), fromclause.description)
        )
    return c


class AnnotatedColumnElement(Annotated):
    def __init__(self, element, values):
        Annotated.__init__(self, element, values)
        for attr in (
            "comparator",
            "_proxy_key",
            "_tq_key_label",
            "_tq_label",
            "_non_anon_label",
        ):
            self.__dict__.pop(attr, None)
        for attr in ("name", "key", "table"):
            if self.__dict__.get(attr, False) is None:
                self.__dict__.pop(attr)

    def _with_annotations(self, values):
        clone = super(AnnotatedColumnElement, self)._with_annotations(values)
        clone.__dict__.pop("comparator", None)
        return clone

    @util.memoized_property
    def name(self):
        """pull 'name' from parent, if not present"""
        return self._Annotated__element.name

    @util.memoized_property
    def table(self):
        """pull 'table' from parent, if not present"""
        return self._Annotated__element.table

    @util.memoized_property
    def key(self):
        """pull 'key' from parent, if not present"""
        return self._Annotated__element.key

    @util.memoized_property
    def info(self):
        return self._Annotated__element.info

    @util.memoized_property
    def _anon_name_label(self):
        return self._Annotated__element._anon_name_label


class _truncated_label(quoted_name):
    """A unicode subclass used to identify symbolic "
    "names that may require truncation."""

    __slots__ = ()

    def __new__(cls, value, quote=None):
        quote = getattr(value, "quote", quote)
        # return super(_truncated_label, cls).__new__(cls, value, quote, True)
        return super(_truncated_label, cls).__new__(cls, value, quote)

    def __reduce__(self):
        return self.__class__, (util.text_type(self), self.quote)

    def apply_map(self, map_):
        return self


class conv(_truncated_label):
    """Mark a string indicating that a name has already been converted
    by a naming convention.

    This is a string subclass that indicates a name that should not be
    subject to any further naming conventions.

    E.g. when we create a :class:`.Constraint` using a naming convention
    as follows::

        m = MetaData(naming_convention={
            "ck": "ck_%(table_name)s_%(constraint_name)s"
        })
        t = Table('t', m, Column('x', Integer),
                        CheckConstraint('x > 5', name='x5'))

    The name of the above constraint will be rendered as ``"ck_t_x5"``.
    That is, the existing name ``x5`` is used in the naming convention as the
    ``constraint_name`` token.

    In some situations, such as in migration scripts, we may be rendering
    the above :class:`.CheckConstraint` with a name that's already been
    converted.  In order to make sure the name isn't double-modified, the
    new name is applied using the :func:`_schema.conv` marker.  We can
    use this explicitly as follows::


        m = MetaData(naming_convention={
            "ck": "ck_%(table_name)s_%(constraint_name)s"
        })
        t = Table('t', m, Column('x', Integer),
                        CheckConstraint('x > 5', name=conv('ck_t_x5')))

    Where above, the :func:`_schema.conv` marker indicates that the constraint
    name here is final, and the name will render as ``"ck_t_x5"`` and not
    ``"ck_t_ck_t_x5"``

    .. versionadded:: 0.9.4

    .. seealso::

        :ref:`constraint_naming_conventions`

    """

    __slots__ = ()


_NONE_NAME = util.symbol("NONE_NAME")
"""indicate a 'deferred' name that was ultimately the value None."""

# for backwards compatibility in case
# someone is re-implementing the
# _truncated_identifier() sequence in a custom
# compiler
_generated_label = _truncated_label


class _anonymous_label(_truncated_label):
    """A unicode subclass used to identify anonymously
    generated names."""

    __slots__ = ()

    @classmethod
    def safe_construct(
        cls, seed, body, enclosing_label=None, sanitize_key=False
    ):

        if sanitize_key:
            body = re.sub(r"[%\(\) \$]+", "_", body).strip("_")

        label = "%%(%d %s)s" % (seed, body.replace("%", "%%"))
        if enclosing_label:
            label = "%s%s" % (enclosing_label, label)

        return _anonymous_label(label)

    def __add__(self, other):
        if "%" in other and not isinstance(other, _anonymous_label):
            other = util.text_type(other).replace("%", "%%")
        else:
            other = util.text_type(other)

        return _anonymous_label(
            quoted_name(
                util.text_type.__add__(self, other),
                self.quote,
            )
        )

    def __radd__(self, other):
        if "%" in other and not isinstance(other, _anonymous_label):
            other = util.text_type(other).replace("%", "%%")
        else:
            other = util.text_type(other)

        return _anonymous_label(
            quoted_name(
                util.text_type.__add__(other, self),
                self.quote,
            )
        )

    def apply_map(self, map_):
        if self.quote is not None:
            # preserve quoting only if necessary
            return quoted_name(self % map_, self.quote)
        else:
            # else skip the constructor call
            return self % map_
