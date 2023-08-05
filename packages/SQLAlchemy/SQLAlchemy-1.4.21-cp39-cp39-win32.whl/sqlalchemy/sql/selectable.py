# sql/selectable.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""The :class:`_expression.FromClause` class of SQL expression elements,
representing
SQL tables and derived rowsets.

"""

import collections
import itertools
from operator import attrgetter

from . import coercions
from . import operators
from . import roles
from . import traversals
from . import type_api
from . import visitors
from .annotation import Annotated
from .annotation import SupportsCloneAnnotations
from .base import _clone
from .base import _cloned_difference
from .base import _cloned_intersection
from .base import _entity_namespace_key
from .base import _expand_cloned
from .base import _from_objects
from .base import _generative
from .base import _select_iterables
from .base import CacheableOptions
from .base import ColumnCollection
from .base import ColumnSet
from .base import CompileState
from .base import DedupeColumnCollection
from .base import Executable
from .base import Generative
from .base import HasCompileState
from .base import HasMemoized
from .base import Immutable
from .base import prefix_anon_map
from .coercions import _document_text_coercion
from .elements import _anonymous_label
from .elements import and_
from .elements import BindParameter
from .elements import BooleanClauseList
from .elements import ClauseElement
from .elements import ClauseList
from .elements import ColumnClause
from .elements import GroupedElement
from .elements import Grouping
from .elements import literal_column
from .elements import TableValuedColumn
from .elements import UnaryExpression
from .visitors import InternalTraversal
from .. import exc
from .. import util
from ..inspection import inspect


class _OffsetLimitParam(BindParameter):
    inherit_cache = True

    @property
    def _limit_offset_value(self):
        return self.effective_value


@util.deprecated(
    "1.4",
    "The standalone :func:`.subquery` function is deprecated "
    "and will be removed in a future release.  Use select().subquery().",
)
def subquery(alias, *args, **kwargs):
    r"""Return an :class:`.Subquery` object derived
    from a :class:`_expression.Select`.

    :param alias: the alias name for the subquery

    :param \*args, \**kwargs:  all other arguments are passed through to the
     :func:`_expression.select` function.

    """
    return Select.create_legacy_select(*args, **kwargs).subquery(alias)


class ReturnsRows(roles.ReturnsRowsRole, ClauseElement):
    """The base-most class for Core constructs that have some concept of
    columns that can represent rows.

    While the SELECT statement and TABLE are the primary things we think
    of in this category,  DML like INSERT, UPDATE and DELETE can also specify
    RETURNING which means they can be used in CTEs and other forms, and
    PostgreSQL has functions that return rows also.

    .. versionadded:: 1.4

    """

    _is_returns_rows = True

    # sub-elements of returns_rows
    _is_from_clause = False
    _is_select_statement = False
    _is_lateral = False

    @property
    def selectable(self):
        return self

    @property
    def _all_selected_columns(self):
        """A sequence of column expression objects that represents the
        "selected" columns of this :class:`_expression.ReturnsRows`.

        This is typically equivalent to .exported_columns except it is
        delivered in the form of a straight sequence and not  keyed
        :class:`_expression.ColumnCollection`.

        """
        raise NotImplementedError()

    @property
    def exported_columns(self):
        """A :class:`_expression.ColumnCollection`
        that represents the "exported"
        columns of this :class:`_expression.ReturnsRows`.

        The "exported" columns represent the collection of
        :class:`_expression.ColumnElement`
        expressions that are rendered by this SQL
        construct.   There are primary varieties which are the
        "FROM clause columns" of a FROM clause, such as a table, join,
        or subquery, the "SELECTed columns", which are the columns in
        the "columns clause" of a SELECT statement, and the RETURNING
        columns in a DML statement..

        .. versionadded:: 1.4

        .. seealso::

            :attr:`_expression.FromClause.exported_columns`

            :attr:`_expression.SelectBase.exported_columns`
        """

        raise NotImplementedError()


class Selectable(ReturnsRows):
    """Mark a class as being selectable."""

    __visit_name__ = "selectable"

    is_selectable = True

    def _refresh_for_new_column(self, column):
        raise NotImplementedError()

    def lateral(self, name=None):
        """Return a LATERAL alias of this :class:`_expression.Selectable`.

        The return value is the :class:`_expression.Lateral` construct also
        provided by the top-level :func:`_expression.lateral` function.

        .. versionadded:: 1.1

        .. seealso::

            :ref:`lateral_selects` -  overview of usage.

        """
        return Lateral._construct(self, name)

    @util.deprecated(
        "1.4",
        message="The :meth:`.Selectable.replace_selectable` method is "
        "deprecated, and will be removed in a future release.  Similar "
        "functionality is available via the sqlalchemy.sql.visitors module.",
    )
    @util.preload_module("sqlalchemy.sql.util")
    def replace_selectable(self, old, alias):
        """Replace all occurrences of :class:`_expression.FromClause`
        'old' with the given :class:`_expression.Alias`
        object, returning a copy of this :class:`_expression.FromClause`.

        """
        return util.preloaded.sql_util.ClauseAdapter(alias).traverse(self)

    def corresponding_column(self, column, require_embedded=False):
        """Given a :class:`_expression.ColumnElement`, return the exported
        :class:`_expression.ColumnElement` object from the
        :attr:`_expression.Selectable.exported_columns`
        collection of this :class:`_expression.Selectable`
        which corresponds to that
        original :class:`_expression.ColumnElement` via a common ancestor
        column.

        :param column: the target :class:`_expression.ColumnElement`
                      to be matched.

        :param require_embedded: only return corresponding columns for
         the given :class:`_expression.ColumnElement`, if the given
         :class:`_expression.ColumnElement`
         is actually present within a sub-element
         of this :class:`_expression.Selectable`.
         Normally the column will match if
         it merely shares a common ancestor with one of the exported
         columns of this :class:`_expression.Selectable`.

        .. seealso::

            :attr:`_expression.Selectable.exported_columns` - the
            :class:`_expression.ColumnCollection`
            that is used for the operation.

            :meth:`_expression.ColumnCollection.corresponding_column`
            - implementation
            method.

        """

        return self.exported_columns.corresponding_column(
            column, require_embedded
        )


class HasPrefixes(object):
    _prefixes = ()

    _has_prefixes_traverse_internals = [
        ("_prefixes", InternalTraversal.dp_prefix_sequence)
    ]

    @_generative
    @_document_text_coercion(
        "expr",
        ":meth:`_expression.HasPrefixes.prefix_with`",
        ":paramref:`.HasPrefixes.prefix_with.*expr`",
    )
    def prefix_with(self, *expr, **kw):
        r"""Add one or more expressions following the statement keyword, i.e.
        SELECT, INSERT, UPDATE, or DELETE. Generative.

        This is used to support backend-specific prefix keywords such as those
        provided by MySQL.

        E.g.::

            stmt = table.insert().prefix_with("LOW_PRIORITY", dialect="mysql")

            # MySQL 5.7 optimizer hints
            stmt = select(table).prefix_with(
                "/*+ BKA(t1) */", dialect="mysql")

        Multiple prefixes can be specified by multiple calls
        to :meth:`_expression.HasPrefixes.prefix_with`.

        :param \*expr: textual or :class:`_expression.ClauseElement`
         construct which
         will be rendered following the INSERT, UPDATE, or DELETE
         keyword.
        :param \**kw: A single keyword 'dialect' is accepted.  This is an
         optional string dialect name which will
         limit rendering of this prefix to only that dialect.

        """
        dialect = kw.pop("dialect", None)
        if kw:
            raise exc.ArgumentError(
                "Unsupported argument(s): %s" % ",".join(kw)
            )
        self._setup_prefixes(expr, dialect)

    def _setup_prefixes(self, prefixes, dialect=None):
        self._prefixes = self._prefixes + tuple(
            [
                (coercions.expect(roles.StatementOptionRole, p), dialect)
                for p in prefixes
            ]
        )


class HasSuffixes(object):
    _suffixes = ()

    _has_suffixes_traverse_internals = [
        ("_suffixes", InternalTraversal.dp_prefix_sequence)
    ]

    @_generative
    @_document_text_coercion(
        "expr",
        ":meth:`_expression.HasSuffixes.suffix_with`",
        ":paramref:`.HasSuffixes.suffix_with.*expr`",
    )
    def suffix_with(self, *expr, **kw):
        r"""Add one or more expressions following the statement as a whole.

        This is used to support backend-specific suffix keywords on
        certain constructs.

        E.g.::

            stmt = select(col1, col2).cte().suffix_with(
                "cycle empno set y_cycle to 1 default 0", dialect="oracle")

        Multiple suffixes can be specified by multiple calls
        to :meth:`_expression.HasSuffixes.suffix_with`.

        :param \*expr: textual or :class:`_expression.ClauseElement`
         construct which
         will be rendered following the target clause.
        :param \**kw: A single keyword 'dialect' is accepted.  This is an
         optional string dialect name which will
         limit rendering of this suffix to only that dialect.

        """
        dialect = kw.pop("dialect", None)
        if kw:
            raise exc.ArgumentError(
                "Unsupported argument(s): %s" % ",".join(kw)
            )
        self._setup_suffixes(expr, dialect)

    def _setup_suffixes(self, suffixes, dialect=None):
        self._suffixes = self._suffixes + tuple(
            [
                (coercions.expect(roles.StatementOptionRole, p), dialect)
                for p in suffixes
            ]
        )


class HasHints(object):
    _hints = util.immutabledict()
    _statement_hints = ()

    _has_hints_traverse_internals = [
        ("_statement_hints", InternalTraversal.dp_statement_hint_list),
        ("_hints", InternalTraversal.dp_table_hint_list),
    ]

    def with_statement_hint(self, text, dialect_name="*"):
        """Add a statement hint to this :class:`_expression.Select` or
        other selectable object.

        This method is similar to :meth:`_expression.Select.with_hint`
        except that
        it does not require an individual table, and instead applies to the
        statement as a whole.

        Hints here are specific to the backend database and may include
        directives such as isolation levels, file directives, fetch directives,
        etc.

        .. versionadded:: 1.0.0

        .. seealso::

            :meth:`_expression.Select.with_hint`

            :meth:`_expression.Select.prefix_with` - generic SELECT prefixing
            which also can suit some database-specific HINT syntaxes such as
            MySQL optimizer hints

        """
        return self.with_hint(None, text, dialect_name)

    @_generative
    def with_hint(self, selectable, text, dialect_name="*"):
        r"""Add an indexing or other executional context hint for the given
        selectable to this :class:`_expression.Select` or other selectable
        object.

        The text of the hint is rendered in the appropriate
        location for the database backend in use, relative
        to the given :class:`_schema.Table` or :class:`_expression.Alias`
        passed as the
        ``selectable`` argument. The dialect implementation
        typically uses Python string substitution syntax
        with the token ``%(name)s`` to render the name of
        the table or alias. E.g. when using Oracle, the
        following::

            select(mytable).\
                with_hint(mytable, "index(%(name)s ix_mytable)")

        Would render SQL as::

            select /*+ index(mytable ix_mytable) */ ... from mytable

        The ``dialect_name`` option will limit the rendering of a particular
        hint to a particular backend. Such as, to add hints for both Oracle
        and Sybase simultaneously::

            select(mytable).\
                with_hint(mytable, "index(%(name)s ix_mytable)", 'oracle').\
                with_hint(mytable, "WITH INDEX ix_mytable", 'sybase')

        .. seealso::

            :meth:`_expression.Select.with_statement_hint`

        """
        if selectable is None:
            self._statement_hints += ((dialect_name, text),)
        else:
            self._hints = self._hints.union(
                {
                    (
                        coercions.expect(roles.FromClauseRole, selectable),
                        dialect_name,
                    ): text
                }
            )


class FromClause(roles.AnonymizedFromClauseRole, Selectable):
    """Represent an element that can be used within the ``FROM``
    clause of a ``SELECT`` statement.

    The most common forms of :class:`_expression.FromClause` are the
    :class:`_schema.Table` and the :func:`_expression.select` constructs.  Key
    features common to all :class:`_expression.FromClause` objects include:

    * a :attr:`.c` collection, which provides per-name access to a collection
      of :class:`_expression.ColumnElement` objects.
    * a :attr:`.primary_key` attribute, which is a collection of all those
      :class:`_expression.ColumnElement`
      objects that indicate the ``primary_key`` flag.
    * Methods to generate various derivations of a "from" clause, including
      :meth:`_expression.FromClause.alias`,
      :meth:`_expression.FromClause.join`,
      :meth:`_expression.FromClause.select`.


    """

    __visit_name__ = "fromclause"
    named_with_column = False
    _hide_froms = []

    schema = None
    """Define the 'schema' attribute for this :class:`_expression.FromClause`.

    This is typically ``None`` for most objects except that of
    :class:`_schema.Table`, where it is taken as the value of the
    :paramref:`_schema.Table.schema` argument.

    """

    is_selectable = True
    _is_from_clause = True
    _is_join = False

    _use_schema_map = False

    @util.deprecated_params(
        whereclause=(
            "2.0",
            "The :paramref:`_sql.FromClause.select().whereclause` parameter "
            "is deprecated and will be removed in version 2.0.  "
            "Please make use of "
            "the :meth:`.Select.where` "
            "method to add WHERE criteria to the SELECT statement.",
        ),
        kwargs=(
            "2.0",
            "The :meth:`_sql.FromClause.select` method will no longer accept "
            "keyword arguments in version 2.0.  Please use generative methods "
            "from the "
            ":class:`_sql.Select` construct in order to apply additional "
            "modifications.",
        ),
    )
    def select(self, whereclause=None, **kwargs):
        r"""Return a SELECT of this :class:`_expression.FromClause`.


        e.g.::

            stmt = some_table.select().where(some_table.c.id == 5)

        :param whereclause: a WHERE clause, equivalent to calling the
         :meth:`_sql.Select.where` method.

        :param \**kwargs: additional keyword arguments are passed to the
         legacy constructor for :class:`_sql.Select` described at
         :meth:`_sql.Select.create_legacy_select`.

        .. seealso::

            :func:`_expression.select` - general purpose
            method which allows for arbitrary column lists.

        """
        if whereclause is not None:
            kwargs["whereclause"] = whereclause
        return Select._create_select_from_fromclause(self, [self], **kwargs)

    def join(self, right, onclause=None, isouter=False, full=False):
        """Return a :class:`_expression.Join` from this
        :class:`_expression.FromClause`
        to another :class:`FromClause`.

        E.g.::

            from sqlalchemy import join

            j = user_table.join(address_table,
                            user_table.c.id == address_table.c.user_id)
            stmt = select(user_table).select_from(j)

        would emit SQL along the lines of::

            SELECT user.id, user.name FROM user
            JOIN address ON user.id = address.user_id

        :param right: the right side of the join; this is any
         :class:`_expression.FromClause` object such as a
         :class:`_schema.Table` object, and
         may also be a selectable-compatible object such as an ORM-mapped
         class.

        :param onclause: a SQL expression representing the ON clause of the
         join.  If left at ``None``, :meth:`_expression.FromClause.join`
         will attempt to
         join the two tables based on a foreign key relationship.

        :param isouter: if True, render a LEFT OUTER JOIN, instead of JOIN.

        :param full: if True, render a FULL OUTER JOIN, instead of LEFT OUTER
         JOIN.  Implies :paramref:`.FromClause.join.isouter`.

         .. versionadded:: 1.1

        .. seealso::

            :func:`_expression.join` - standalone function

            :class:`_expression.Join` - the type of object produced

        """

        return Join(self, right, onclause, isouter, full)

    def outerjoin(self, right, onclause=None, full=False):
        """Return a :class:`_expression.Join` from this
        :class:`_expression.FromClause`
        to another :class:`FromClause`, with the "isouter" flag set to
        True.

        E.g.::

            from sqlalchemy import outerjoin

            j = user_table.outerjoin(address_table,
                            user_table.c.id == address_table.c.user_id)

        The above is equivalent to::

            j = user_table.join(
                address_table,
                user_table.c.id == address_table.c.user_id,
                isouter=True)

        :param right: the right side of the join; this is any
         :class:`_expression.FromClause` object such as a
         :class:`_schema.Table` object, and
         may also be a selectable-compatible object such as an ORM-mapped
         class.

        :param onclause: a SQL expression representing the ON clause of the
         join.  If left at ``None``, :meth:`_expression.FromClause.join`
         will attempt to
         join the two tables based on a foreign key relationship.

        :param full: if True, render a FULL OUTER JOIN, instead of
         LEFT OUTER JOIN.

         .. versionadded:: 1.1

        .. seealso::

            :meth:`_expression.FromClause.join`

            :class:`_expression.Join`

        """

        return Join(self, right, onclause, True, full)

    def alias(self, name=None, flat=False):
        """Return an alias of this :class:`_expression.FromClause`.

        E.g.::

            a2 = some_table.alias('a2')

        The above code creates an :class:`_expression.Alias`
        object which can be used
        as a FROM clause in any SELECT statement.

        .. seealso::

            :ref:`core_tutorial_aliases`

            :func:`_expression.alias`

        """

        return Alias._construct(self, name)

    @util.preload_module("sqlalchemy.sql.sqltypes")
    def table_valued(self):
        """Return a :class:`_sql.TableValuedColumn` object for this
        :class:`_expression.FromClause`.

        A :class:`_sql.TableValuedColumn` is a :class:`_sql.ColumnElement` that
        represents a complete row in a table. Support for this construct is
        backend dependent, and is supported in various forms by backends
        such as PostgreSQL, Oracle and SQL Server.

        E.g.::

            >>> from sqlalchemy import select, column, func, table
            >>> a = table("a", column("id"), column("x"), column("y"))
            >>> stmt = select(func.row_to_json(a.table_valued()))
            >>> print(stmt)
            SELECT row_to_json(a) AS row_to_json_1
            FROM a

        .. versionadded:: 1.4.0b2

        .. seealso::

            :ref:`tutorial_functions` - in the :ref:`unified_tutorial`

        """
        return TableValuedColumn(self, type_api.TABLEVALUE)

    def tablesample(self, sampling, name=None, seed=None):
        """Return a TABLESAMPLE alias of this :class:`_expression.FromClause`.

        The return value is the :class:`_expression.TableSample`
        construct also
        provided by the top-level :func:`_expression.tablesample` function.

        .. versionadded:: 1.1

        .. seealso::

            :func:`_expression.tablesample` - usage guidelines and parameters

        """
        return TableSample._construct(self, sampling, name, seed)

    def is_derived_from(self, fromclause):
        """Return ``True`` if this :class:`_expression.FromClause` is
        'derived' from the given ``FromClause``.

        An example would be an Alias of a Table is derived from that Table.

        """
        # this is essentially an "identity" check in the base class.
        # Other constructs override this to traverse through
        # contained elements.
        return fromclause in self._cloned_set

    def _is_lexical_equivalent(self, other):
        """Return ``True`` if this :class:`_expression.FromClause` and
        the other represent the same lexical identity.

        This tests if either one is a copy of the other, or
        if they are the same via annotation identity.

        """
        return self._cloned_set.intersection(other._cloned_set)

    @property
    def description(self):
        """A brief description of this :class:`_expression.FromClause`.

        Used primarily for error message formatting.

        """
        return getattr(self, "name", self.__class__.__name__ + " object")

    def _generate_fromclause_column_proxies(self, fromclause):
        fromclause._columns._populate_separate_keys(
            col._make_proxy(fromclause) for col in self.c
        )

    @property
    def exported_columns(self):
        """A :class:`_expression.ColumnCollection`
        that represents the "exported"
        columns of this :class:`_expression.Selectable`.

        The "exported" columns for a :class:`_expression.FromClause`
        object are synonymous
        with the :attr:`_expression.FromClause.columns` collection.

        .. versionadded:: 1.4

        .. seealso::

            :attr:`_expression.Selectable.exported_columns`

            :attr:`_expression.SelectBase.exported_columns`


        """
        return self.columns

    @util.memoized_property
    def columns(self):
        """A named-based collection of :class:`_expression.ColumnElement`
        objects maintained by this :class:`_expression.FromClause`.

        The :attr:`.columns`, or :attr:`.c` collection, is the gateway
        to the construction of SQL expressions using table-bound or
        other selectable-bound columns::

            select(mytable).where(mytable.c.somecolumn == 5)

        :return: a :class:`.ColumnCollection` object.

        """

        if "_columns" not in self.__dict__:
            self._init_collections()
            self._populate_column_collection()
        return self._columns.as_immutable()

    @property
    def entity_namespace(self):
        """Return a namespace used for name-based access in SQL expressions.

        This is the namespace that is used to resolve "filter_by()" type
        expressions, such as::

            stmt.filter_by(address='some address')

        It defaults to the ``.c`` collection, however internally it can
        be overridden using the "entity_namespace" annotation to deliver
        alternative results.

        """
        return self.columns

    @util.memoized_property
    def primary_key(self):
        """Return the iterable collection of :class:`_schema.Column` objects
        which comprise the primary key of this :class:`_selectable.FromClause`.

        For a :class:`_schema.Table` object, this collection is represented
        by the :class:`_schema.PrimaryKeyConstraint` which itself is an
        iterable collection of :class:`_schema.Column` objects.

        """
        self._init_collections()
        self._populate_column_collection()
        return self.primary_key

    @util.memoized_property
    def foreign_keys(self):
        """Return the collection of :class:`_schema.ForeignKey` marker objects
        which this FromClause references.

        Each :class:`_schema.ForeignKey` is a member of a
        :class:`_schema.Table`-wide
        :class:`_schema.ForeignKeyConstraint`.

        .. seealso::

            :attr:`_schema.Table.foreign_key_constraints`

        """
        self._init_collections()
        self._populate_column_collection()
        return self.foreign_keys

    def _reset_column_collection(self):
        """Reset the attributes linked to the ``FromClause.c`` attribute.

        This collection is separate from all the other memoized things
        as it has shown to be sensitive to being cleared out in situations
        where enclosing code, typically in a replacement traversal scenario,
        has already established strong relationships
        with the exported columns.

        The collection is cleared for the case where a table is having a
        column added to it as well as within a Join during copy internals.

        """

        for key in ["_columns", "columns", "primary_key", "foreign_keys"]:
            self.__dict__.pop(key, None)

    c = property(
        attrgetter("columns"),
        doc="""
        A named-based collection of :class:`_expression.ColumnElement`
        objects maintained by this :class:`_expression.FromClause`.

        The :attr:`_sql.FromClause.c` attribute is an alias for the
        :attr:`_sql.FromClause.columns` atttribute.

        :return: a :class:`.ColumnCollection`

        """,
    )
    _select_iterable = property(attrgetter("columns"))

    def _init_collections(self):
        assert "_columns" not in self.__dict__
        assert "primary_key" not in self.__dict__
        assert "foreign_keys" not in self.__dict__

        self._columns = ColumnCollection()
        self.primary_key = ColumnSet()
        self.foreign_keys = set()

    @property
    def _cols_populated(self):
        return "_columns" in self.__dict__

    def _populate_column_collection(self):
        """Called on subclasses to establish the .c collection.

        Each implementation has a different way of establishing
        this collection.

        """

    def _refresh_for_new_column(self, column):
        """Given a column added to the .c collection of an underlying
        selectable, produce the local version of that column, assuming this
        selectable ultimately should proxy this column.

        this is used to "ping" a derived selectable to add a new column
        to its .c. collection when a Column has been added to one of the
        Table objects it ultimately derives from.

        If the given selectable hasn't populated its .c. collection yet,
        it should at least pass on the message to the contained selectables,
        but it will return None.

        This method is currently used by Declarative to allow Table
        columns to be added to a partially constructed inheritance
        mapping that may have already produced joins.  The method
        isn't public right now, as the full span of implications
        and/or caveats aren't yet clear.

        It's also possible that this functionality could be invoked by
        default via an event, which would require that
        selectables maintain a weak referencing collection of all
        derivations.

        """
        self._reset_column_collection()

    def _anonymous_fromclause(self, name=None, flat=False):
        return self.alias(name=name)


LABEL_STYLE_NONE = util.symbol(
    "LABEL_STYLE_NONE",
    """Label style indicating no automatic labeling should be applied to the
    columns clause of a SELECT statement.

    Below, the columns named ``columna`` are both rendered as is, meaning that
    the name ``columna`` can only refer to the first occurrence of this name
    within a result set, as well as if the statement were used as a subquery::

        >>> from sqlalchemy import table, column, select, true, LABEL_STYLE_NONE
        >>> table1 = table("table1", column("columna"), column("columnb"))
        >>> table2 = table("table2", column("columna"), column("columnc"))
        >>> print(select(table1, table2).join(table2, true()).set_label_style(LABEL_STYLE_NONE))
        SELECT table1.columna, table1.columnb, table2.columna, table2.columnc
        FROM table1 JOIN table2 ON true

    Used with the :meth:`_sql.Select.set_label_style` method.

    .. versionadded:: 1.4

""",  # noqa E501
)

LABEL_STYLE_TABLENAME_PLUS_COL = util.symbol(
    "LABEL_STYLE_TABLENAME_PLUS_COL",
    """Label style indicating all columns should be labeled as
    ``<tablename>_<columnname>`` when generating the columns clause of a SELECT
    statement, to disambiguate same-named columns referenced from different
    tables, aliases, or subqueries.

    Below, all column names are given a label so that the two same-named
    columns ``columna`` are disambiguated as ``table1_columna`` and
    ``table2_columna`::

        >>> from sqlalchemy import table, column, select, true, LABEL_STYLE_TABLENAME_PLUS_COL
        >>> table1 = table("table1", column("columna"), column("columnb"))
        >>> table2 = table("table2", column("columna"), column("columnc"))
        >>> print(select(table1, table2).join(table2, true()).set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL))
        SELECT table1.columna AS table1_columna, table1.columnb AS table1_columnb, table2.columna AS table2_columna, table2.columnc AS table2_columnc
        FROM table1 JOIN table2 ON true

    Used with the :meth:`_sql.GenerativeSelect.set_label_style` method.
    Equivalent to the legacy method ``Select.apply_labels()``;
    :data:`_sql.LABEL_STYLE_TABLENAME_PLUS_COL` is SQLAlchemy's legacy
    auto-labeling style. :data:`_sql.LABEL_STYLE_DISAMBIGUATE_ONLY` provides a
    less intrusive approach to disambiguation of same-named column expressions.


    .. versionadded:: 1.4

""",  # noqa E501
)


LABEL_STYLE_DISAMBIGUATE_ONLY = util.symbol(
    "LABEL_STYLE_DISAMBIGUATE_ONLY",
    """Label style indicating that columns with a name that conflicts with
    an existing name should be labeled with a semi-anonymizing label
    when generating the columns clause of a SELECT statement.

    Below, most column names are left unaffected, except for the second
    occurrence of the name ``columna``, which is labeled using the
    label ``columna_1`` to disambiguate it from that of ``tablea.columna``::

        >>> from sqlalchemy import table, column, select, true, LABEL_STYLE_DISAMBIGUATE_ONLY
        >>> table1 = table("table1", column("columna"), column("columnb"))
        >>> table2 = table("table2", column("columna"), column("columnc"))
        >>> print(select(table1, table2).join(table2, true()).set_label_style(LABEL_STYLE_DISAMBIGUATE_ONLY))
        SELECT table1.columna, table1.columnb, table2.columna AS columna_1, table2.columnc
        FROM table1 JOIN table2 ON true

    Used with the :meth:`_sql.GenerativeSelect.set_label_style` method,
    :data:`_sql.LABEL_STYLE_DISAMBIGUATE_ONLY` is the default labeling style
    for all SELECT statements outside of :term:`1.x style` ORM queries.

    .. versionadded:: 1.4

""",  # noqa: E501,
)


LABEL_STYLE_DEFAULT = LABEL_STYLE_DISAMBIGUATE_ONLY
"""The default label style, refers to
:data:`_sql.LABEL_STYLE_DISAMBIGUATE_ONLY`.

.. versionadded:: 1.4

"""


class Join(roles.DMLTableRole, FromClause):
    """Represent a ``JOIN`` construct between two
    :class:`_expression.FromClause`
    elements.

    The public constructor function for :class:`_expression.Join`
    is the module-level
    :func:`_expression.join()` function, as well as the
    :meth:`_expression.FromClause.join` method
    of any :class:`_expression.FromClause` (e.g. such as
    :class:`_schema.Table`).

    .. seealso::

        :func:`_expression.join`

        :meth:`_expression.FromClause.join`

    """

    __visit_name__ = "join"

    _traverse_internals = [
        ("left", InternalTraversal.dp_clauseelement),
        ("right", InternalTraversal.dp_clauseelement),
        ("onclause", InternalTraversal.dp_clauseelement),
        ("isouter", InternalTraversal.dp_boolean),
        ("full", InternalTraversal.dp_boolean),
    ]

    _is_join = True

    def __init__(self, left, right, onclause=None, isouter=False, full=False):
        """Construct a new :class:`_expression.Join`.

        The usual entrypoint here is the :func:`_expression.join`
        function or the :meth:`_expression.FromClause.join` method of any
        :class:`_expression.FromClause` object.

        """
        self.left = coercions.expect(
            roles.FromClauseRole, left, deannotate=True
        )
        self.right = coercions.expect(
            roles.FromClauseRole, right, deannotate=True
        ).self_group()

        if onclause is None:
            self.onclause = self._match_primaries(self.left, self.right)
        else:
            # note: taken from If91f61527236fd4d7ae3cad1f24c38be921c90ba
            # not merged yet
            self.onclause = coercions.expect(
                roles.OnClauseRole, onclause
            ).self_group(against=operators._asbool)

        self.isouter = isouter
        self.full = full

    @classmethod
    def _create_outerjoin(cls, left, right, onclause=None, full=False):
        """Return an ``OUTER JOIN`` clause element.

        The returned object is an instance of :class:`_expression.Join`.

        Similar functionality is also available via the
        :meth:`_expression.FromClause.outerjoin` method on any
        :class:`_expression.FromClause`.

        :param left: The left side of the join.

        :param right: The right side of the join.

        :param onclause:  Optional criterion for the ``ON`` clause, is
          derived from foreign key relationships established between
          left and right otherwise.

        To chain joins together, use the :meth:`_expression.FromClause.join`
        or
        :meth:`_expression.FromClause.outerjoin` methods on the resulting
        :class:`_expression.Join` object.

        """
        return cls(left, right, onclause, isouter=True, full=full)

    @classmethod
    def _create_join(
        cls, left, right, onclause=None, isouter=False, full=False
    ):
        """Produce a :class:`_expression.Join` object, given two
        :class:`_expression.FromClause`
        expressions.

        E.g.::

            j = join(user_table, address_table,
                     user_table.c.id == address_table.c.user_id)
            stmt = select(user_table).select_from(j)

        would emit SQL along the lines of::

            SELECT user.id, user.name FROM user
            JOIN address ON user.id = address.user_id

        Similar functionality is available given any
        :class:`_expression.FromClause` object (e.g. such as a
        :class:`_schema.Table`) using
        the :meth:`_expression.FromClause.join` method.

        :param left: The left side of the join.

        :param right: the right side of the join; this is any
         :class:`_expression.FromClause` object such as a
         :class:`_schema.Table` object, and
         may also be a selectable-compatible object such as an ORM-mapped
         class.

        :param onclause: a SQL expression representing the ON clause of the
         join.  If left at ``None``, :meth:`_expression.FromClause.join`
         will attempt to
         join the two tables based on a foreign key relationship.

        :param isouter: if True, render a LEFT OUTER JOIN, instead of JOIN.

        :param full: if True, render a FULL OUTER JOIN, instead of JOIN.

         .. versionadded:: 1.1

        .. seealso::

            :meth:`_expression.FromClause.join` - method form,
            based on a given left side.

            :class:`_expression.Join` - the type of object produced.

        """

        return cls(left, right, onclause, isouter, full)

    @property
    def description(self):
        return "Join object on %s(%d) and %s(%d)" % (
            self.left.description,
            id(self.left),
            self.right.description,
            id(self.right),
        )

    def is_derived_from(self, fromclause):
        return (
            # use hash() to ensure direct comparison to annotated works
            # as well
            hash(fromclause) == hash(self)
            or self.left.is_derived_from(fromclause)
            or self.right.is_derived_from(fromclause)
        )

    def self_group(self, against=None):
        return FromGrouping(self)

    @util.preload_module("sqlalchemy.sql.util")
    def _populate_column_collection(self):
        sqlutil = util.preloaded.sql_util
        columns = [c for c in self.left.columns] + [
            c for c in self.right.columns
        ]

        self.primary_key.extend(
            sqlutil.reduce_columns(
                (c for c in columns if c.primary_key), self.onclause
            )
        )
        self._columns._populate_separate_keys(
            (col._tq_key_label, col) for col in columns
        )
        self.foreign_keys.update(
            itertools.chain(*[col.foreign_keys for col in columns])
        )

    def _refresh_for_new_column(self, column):
        super(Join, self)._refresh_for_new_column(column)
        self.left._refresh_for_new_column(column)
        self.right._refresh_for_new_column(column)

    def _match_primaries(self, left, right):
        if isinstance(left, Join):
            left_right = left.right
        else:
            left_right = None
        return self._join_condition(left, right, a_subset=left_right)

    @classmethod
    def _join_condition(
        cls, a, b, a_subset=None, consider_as_foreign_keys=None
    ):
        """Create a join condition between two tables or selectables.

        e.g.::

            join_condition(tablea, tableb)

        would produce an expression along the lines of::

            tablea.c.id==tableb.c.tablea_id

        The join is determined based on the foreign key relationships
        between the two selectables.   If there are multiple ways
        to join, or no way to join, an error is raised.

        :param a_subset: An optional expression that is a sub-component
         of ``a``.  An attempt will be made to join to just this sub-component
         first before looking at the full ``a`` construct, and if found
         will be successful even if there are other ways to join to ``a``.
         This allows the "right side" of a join to be passed thereby
         providing a "natural join".

        """
        constraints = cls._joincond_scan_left_right(
            a, a_subset, b, consider_as_foreign_keys
        )

        if len(constraints) > 1:
            cls._joincond_trim_constraints(
                a, b, constraints, consider_as_foreign_keys
            )

        if len(constraints) == 0:
            if isinstance(b, FromGrouping):
                hint = (
                    " Perhaps you meant to convert the right side to a "
                    "subquery using alias()?"
                )
            else:
                hint = ""
            raise exc.NoForeignKeysError(
                "Can't find any foreign key relationships "
                "between '%s' and '%s'.%s"
                % (a.description, b.description, hint)
            )

        crit = [(x == y) for x, y in list(constraints.values())[0]]
        if len(crit) == 1:
            return crit[0]
        else:
            return and_(*crit)

    @classmethod
    def _can_join(cls, left, right, consider_as_foreign_keys=None):
        if isinstance(left, Join):
            left_right = left.right
        else:
            left_right = None

        constraints = cls._joincond_scan_left_right(
            a=left,
            b=right,
            a_subset=left_right,
            consider_as_foreign_keys=consider_as_foreign_keys,
        )

        return bool(constraints)

    @classmethod
    @util.preload_module("sqlalchemy.sql.util")
    def _joincond_scan_left_right(
        cls, a, a_subset, b, consider_as_foreign_keys
    ):
        sql_util = util.preloaded.sql_util

        a = coercions.expect(roles.FromClauseRole, a)
        b = coercions.expect(roles.FromClauseRole, b)

        constraints = collections.defaultdict(list)

        for left in (a_subset, a):
            if left is None:
                continue
            for fk in sorted(
                b.foreign_keys, key=lambda fk: fk.parent._creation_order
            ):
                if (
                    consider_as_foreign_keys is not None
                    and fk.parent not in consider_as_foreign_keys
                ):
                    continue
                try:
                    col = fk.get_referent(left)
                except exc.NoReferenceError as nrte:
                    table_names = {t.name for t in sql_util.find_tables(left)}
                    if nrte.table_name in table_names:
                        raise
                    else:
                        continue

                if col is not None:
                    constraints[fk.constraint].append((col, fk.parent))
            if left is not b:
                for fk in sorted(
                    left.foreign_keys, key=lambda fk: fk.parent._creation_order
                ):
                    if (
                        consider_as_foreign_keys is not None
                        and fk.parent not in consider_as_foreign_keys
                    ):
                        continue
                    try:
                        col = fk.get_referent(b)
                    except exc.NoReferenceError as nrte:
                        table_names = {t.name for t in sql_util.find_tables(b)}
                        if nrte.table_name in table_names:
                            raise
                        else:
                            continue

                    if col is not None:
                        constraints[fk.constraint].append((col, fk.parent))
            if constraints:
                break
        return constraints

    @classmethod
    def _joincond_trim_constraints(
        cls, a, b, constraints, consider_as_foreign_keys
    ):
        # more than one constraint matched.  narrow down the list
        # to include just those FKCs that match exactly to
        # "consider_as_foreign_keys".
        if consider_as_foreign_keys:
            for const in list(constraints):
                if set(f.parent for f in const.elements) != set(
                    consider_as_foreign_keys
                ):
                    del constraints[const]

        # if still multiple constraints, but
        # they all refer to the exact same end result, use it.
        if len(constraints) > 1:
            dedupe = set(tuple(crit) for crit in constraints.values())
            if len(dedupe) == 1:
                key = list(constraints)[0]
                constraints = {key: constraints[key]}

        if len(constraints) != 1:
            raise exc.AmbiguousForeignKeysError(
                "Can't determine join between '%s' and '%s'; "
                "tables have more than one foreign key "
                "constraint relationship between them. "
                "Please specify the 'onclause' of this "
                "join explicitly." % (a.description, b.description)
            )

    @util.deprecated_params(
        whereclause=(
            "2.0",
            "The :paramref:`_sql.Join.select().whereclause` parameter "
            "is deprecated and will be removed in version 2.0.  "
            "Please make use of "
            "the :meth:`.Select.where` "
            "method to add WHERE criteria to the SELECT statement.",
        ),
        kwargs=(
            "2.0",
            "The :meth:`_sql.Join.select` method will no longer accept "
            "keyword arguments in version 2.0.  Please use generative "
            "methods from the "
            ":class:`_sql.Select` construct in order to apply additional "
            "modifications.",
        ),
    )
    def select(self, whereclause=None, **kwargs):
        r"""Create a :class:`_expression.Select` from this
        :class:`_expression.Join`.

        E.g.::

            stmt = table_a.join(table_b, table_a.c.id == table_b.c.a_id)

            stmt = stmt.select()

        The above will produce a SQL string resembling::

            SELECT table_a.id, table_a.col, table_b.id, table_b.a_id
            FROM table_a JOIN table_b ON table_a.id = table_b.a_id

        :param whereclause: WHERE criteria, same as calling
          :meth:`_sql.Select.where` on the resulting statement

        :param \**kwargs: additional keyword arguments are passed to the
         legacy constructor for :class:`_sql.Select` described at
         :meth:`_sql.Select.create_legacy_select`.

        """
        collist = [self.left, self.right]

        if whereclause is not None:
            kwargs["whereclause"] = whereclause
        return Select._create_select_from_fromclause(
            self, collist, **kwargs
        ).select_from(self)

    @property
    @util.deprecated_20(
        ":attr:`.Executable.bind`",
        alternative="Bound metadata is being removed as of SQLAlchemy 2.0.",
        enable_warnings=False,
    )
    def bind(self):
        """Return the bound engine associated with either the left or right
        side of this :class:`_sql.Join`.

        """

        return self.left.bind or self.right.bind

    @util.preload_module("sqlalchemy.sql.util")
    def _anonymous_fromclause(self, name=None, flat=False):
        sqlutil = util.preloaded.sql_util
        if flat:
            if name is not None:
                raise exc.ArgumentError("Can't send name argument with flat")
            left_a, right_a = (
                self.left._anonymous_fromclause(flat=True),
                self.right._anonymous_fromclause(flat=True),
            )
            adapter = sqlutil.ClauseAdapter(left_a).chain(
                sqlutil.ClauseAdapter(right_a)
            )

            return left_a.join(
                right_a,
                adapter.traverse(self.onclause),
                isouter=self.isouter,
                full=self.full,
            )
        else:
            return (
                self.select()
                .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)
                .correlate(None)
                .alias(name)
            )

    @util.deprecated_20(
        ":meth:`_sql.Join.alias`",
        alternative="Create a select + subquery, or alias the "
        "individual tables inside the join, instead.",
    )
    def alias(self, name=None, flat=False):
        r"""Return an alias of this :class:`_expression.Join`.

        The default behavior here is to first produce a SELECT
        construct from this :class:`_expression.Join`, then to produce an
        :class:`_expression.Alias` from that.  So given a join of the form::

            j = table_a.join(table_b, table_a.c.id == table_b.c.a_id)

        The JOIN by itself would look like::

            table_a JOIN table_b ON table_a.id = table_b.a_id

        Whereas the alias of the above, ``j.alias()``, would in a
        SELECT context look like::

            (SELECT table_a.id AS table_a_id, table_b.id AS table_b_id,
                table_b.a_id AS table_b_a_id
                FROM table_a
                JOIN table_b ON table_a.id = table_b.a_id) AS anon_1

        The equivalent long-hand form, given a :class:`_expression.Join`
        object ``j``, is::

            from sqlalchemy import select, alias
            j = alias(
                select(j.left, j.right).\
                    select_from(j).\
                    set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL).\
                    correlate(False),
                name=name
            )

        The selectable produced by :meth:`_expression.Join.alias`
        features the same
        columns as that of the two individual selectables presented under
        a single name - the individual columns are "auto-labeled", meaning
        the ``.c.`` collection of the resulting :class:`_expression.Alias`
        represents
        the names of the individual columns using a
        ``<tablename>_<columname>`` scheme::

            j.c.table_a_id
            j.c.table_b_a_id

        :meth:`_expression.Join.alias` also features an alternate
        option for aliasing joins which produces no enclosing SELECT and
        does not normally apply labels to the column names.  The
        ``flat=True`` option will call :meth:`_expression.FromClause.alias`
        against the left and right sides individually.
        Using this option, no new ``SELECT`` is produced;
        we instead, from a construct as below::

            j = table_a.join(table_b, table_a.c.id == table_b.c.a_id)
            j = j.alias(flat=True)

        we get a result like this::

            table_a AS table_a_1 JOIN table_b AS table_b_1 ON
            table_a_1.id = table_b_1.a_id

        The ``flat=True`` argument is also propagated to the contained
        selectables, so that a composite join such as::

            j = table_a.join(
                    table_b.join(table_c,
                            table_b.c.id == table_c.c.b_id),
                    table_b.c.a_id == table_a.c.id
                ).alias(flat=True)

        Will produce an expression like::

            table_a AS table_a_1 JOIN (
                    table_b AS table_b_1 JOIN table_c AS table_c_1
                    ON table_b_1.id = table_c_1.b_id
            ) ON table_a_1.id = table_b_1.a_id

        The standalone :func:`_expression.alias` function as well as the
        base :meth:`_expression.FromClause.alias`
        method also support the ``flat=True``
        argument as a no-op, so that the argument can be passed to the
        ``alias()`` method of any selectable.

        :param name: name given to the alias.

        :param flat: if True, produce an alias of the left and right
         sides of this :class:`_expression.Join` and return the join of those
         two selectables.   This produces join expression that does not
         include an enclosing SELECT.

        .. seealso::

            :ref:`core_tutorial_aliases`

            :func:`_expression.alias`

        """
        return self._anonymous_fromclause(flat=flat, name=name)

    @property
    def _hide_froms(self):
        return itertools.chain(
            *[_from_objects(x.left, x.right) for x in self._cloned_set]
        )

    @property
    def _from_objects(self):
        return [self] + self.left._from_objects + self.right._from_objects


class NoInit(object):
    def __init__(self, *arg, **kw):
        raise NotImplementedError(
            "The %s class is not intended to be constructed "
            "directly.  Please use the %s() standalone "
            "function or the %s() method available from appropriate "
            "selectable objects."
            % (
                self.__class__.__name__,
                self.__class__.__name__.lower(),
                self.__class__.__name__.lower(),
            )
        )


# FromClause ->
#   AliasedReturnsRows
#        -> Alias   only for FromClause
#        -> Subquery  only for SelectBase
#        -> CTE only for HasCTE -> SelectBase, DML
#        -> Lateral -> FromClause, but we accept SelectBase
#           w/ non-deprecated coercion
#        -> TableSample -> only for FromClause
class AliasedReturnsRows(NoInit, FromClause):
    """Base class of aliases against tables, subqueries, and other
    selectables."""

    _is_from_container = True
    named_with_column = True

    _supports_derived_columns = False

    _traverse_internals = [
        ("element", InternalTraversal.dp_clauseelement),
        ("name", InternalTraversal.dp_anon_name),
    ]

    @classmethod
    def _construct(cls, *arg, **kw):
        obj = cls.__new__(cls)
        obj._init(*arg, **kw)
        return obj

    @classmethod
    def _factory(cls, returnsrows, name=None):
        """Base factory method.  Subclasses need to provide this."""
        raise NotImplementedError()

    def _init(self, selectable, name=None):
        self.element = coercions.expect(
            roles.ReturnsRowsRole, selectable, apply_propagate_attrs=self
        )
        self.element = selectable
        self._orig_name = name
        if name is None:
            if (
                isinstance(selectable, FromClause)
                and selectable.named_with_column
            ):
                name = getattr(selectable, "name", None)
                if isinstance(name, _anonymous_label):
                    name = None
            name = _anonymous_label.safe_construct(id(self), name or "anon")
        self.name = name

    def _refresh_for_new_column(self, column):
        super(AliasedReturnsRows, self)._refresh_for_new_column(column)
        self.element._refresh_for_new_column(column)

    @property
    def description(self):
        name = self.name
        if isinstance(name, _anonymous_label):
            name = "anon_1"

        if util.py3k:
            return name
        else:
            return name.encode("ascii", "backslashreplace")

    @property
    def original(self):
        """Legacy for dialects that are referring to Alias.original."""
        return self.element

    def is_derived_from(self, fromclause):
        if fromclause in self._cloned_set:
            return True
        return self.element.is_derived_from(fromclause)

    def _populate_column_collection(self):
        self.element._generate_fromclause_column_proxies(self)

    def _copy_internals(self, clone=_clone, **kw):
        existing_element = self.element

        super(AliasedReturnsRows, self)._copy_internals(clone=clone, **kw)

        # the element clone is usually against a Table that returns the
        # same object.  don't reset exported .c. collections and other
        # memoized details if it was not changed.  this saves a lot on
        # performance.
        if existing_element is not self.element:
            self._reset_column_collection()

    @property
    def _from_objects(self):
        return [self]

    @property
    def bind(self):
        return self.element.bind


class Alias(roles.DMLTableRole, AliasedReturnsRows):
    """Represents an table or selectable alias (AS).

    Represents an alias, as typically applied to any table or
    sub-select within a SQL statement using the ``AS`` keyword (or
    without the keyword on certain databases such as Oracle).

    This object is constructed from the :func:`_expression.alias` module
    level function as well as the :meth:`_expression.FromClause.alias`
    method available
    on all :class:`_expression.FromClause` subclasses.

    .. seealso::

        :meth:`_expression.FromClause.alias`

    """

    __visit_name__ = "alias"

    inherit_cache = True

    @classmethod
    def _factory(cls, selectable, name=None, flat=False):
        """Return an :class:`_expression.Alias` object.

        An :class:`_expression.Alias` represents any
        :class:`_expression.FromClause`
        with an alternate name assigned within SQL, typically using the ``AS``
        clause when generated, e.g. ``SELECT * FROM table AS aliasname``.

        Similar functionality is available via the
        :meth:`_expression.FromClause.alias`
        method available on all :class:`_expression.FromClause` subclasses.
        In terms of
        a SELECT object as generated from the :func:`_expression.select`
        function, the :meth:`_expression.SelectBase.alias` method returns an
        :class:`_expression.Alias` or similar object which represents a named,
        parenthesized subquery.

        When an :class:`_expression.Alias` is created from a
        :class:`_schema.Table` object,
        this has the effect of the table being rendered
        as ``tablename AS aliasname`` in a SELECT statement.

        For :func:`_expression.select` objects, the effect is that of
        creating a named subquery, i.e. ``(select ...) AS aliasname``.

        The ``name`` parameter is optional, and provides the name
        to use in the rendered SQL.  If blank, an "anonymous" name
        will be deterministically generated at compile time.
        Deterministic means the name is guaranteed to be unique against
        other constructs used in the same statement, and will also be the
        same name for each successive compilation of the same statement
        object.

        :param selectable: any :class:`_expression.FromClause` subclass,
            such as a table, select statement, etc.

        :param name: string name to be assigned as the alias.
            If ``None``, a name will be deterministically generated
            at compile time.

        :param flat: Will be passed through to if the given selectable
         is an instance of :class:`_expression.Join` - see
         :meth:`_expression.Join.alias`
         for details.

        """
        return coercions.expect(
            roles.FromClauseRole, selectable, allow_select=True
        ).alias(name=name, flat=flat)


class TableValuedAlias(Alias):
    """An alias against a "table valued" SQL function.

    This construct provides for a SQL function that returns columns
    to be used in the FROM clause of a SELECT statement.   The
    object is generated using the :meth:`_functions.FunctionElement.table_valued`
    method, e.g.::

        >>> from sqlalchemy import select, func
        >>> fn = func.json_array_elements_text('["one", "two", "three"]').table_valued("value")
        >>> print(select(fn.c.value))
        SELECT anon_1.value
        FROM json_array_elements_text(:json_array_elements_text_1) AS anon_1

    .. versionadded:: 1.4.0b2

    .. seealso::

        :ref:`tutorial_functions_table_valued` - in the :ref:`unified_tutorial`

    """  # noqa E501

    __visit_name__ = "table_valued_alias"

    _supports_derived_columns = True
    _render_derived = False
    _render_derived_w_types = False

    _traverse_internals = [
        ("element", InternalTraversal.dp_clauseelement),
        ("name", InternalTraversal.dp_anon_name),
        ("_tableval_type", InternalTraversal.dp_type),
        ("_render_derived", InternalTraversal.dp_boolean),
        ("_render_derived_w_types", InternalTraversal.dp_boolean),
    ]

    def _init(self, selectable, name=None, table_value_type=None):
        super(TableValuedAlias, self)._init(selectable, name=name)

        self._tableval_type = (
            type_api.TABLEVALUE
            if table_value_type is None
            else table_value_type
        )

    @HasMemoized.memoized_attribute
    def column(self):
        """Return a column expression representing this
        :class:`_sql.TableValuedAlias`.

        This accessor is used to implement the
        :meth:`_functions.FunctionElement.column_valued` method. See that
        method for further details.

        E.g.::

            >>> print(select(func.some_func().table_valued("value").column))
            SELECT anon_1 FROM some_func() AS anon_1

        .. seealso::

            :meth:`_functions.FunctionElement.column_valued`

        """

        return TableValuedColumn(self, self._tableval_type)

    def alias(self, name=None):
        """Return a new alias of this :class:`_sql.TableValuedAlias`.

        This creates a distinct FROM object that will be distinguished
        from the original one when used in a SQL statement.

        """

        tva = TableValuedAlias._construct(self, name=name)
        if self._render_derived:
            tva._render_derived = True
            tva._render_derived_w_types = self._render_derived_w_types
        return tva

    def lateral(self, name=None):
        """Return a new :class:`_sql.TableValuedAlias` with the lateral flag set,
        so that it renders as LATERAL.

        .. seealso::

            :func:`_expression.lateral`

        """
        tva = self.alias(name=name)
        tva._is_lateral = True
        return tva

    def render_derived(self, name=None, with_types=False):
        """Apply "render derived" to this :class:`_sql.TableValuedAlias`.

        This has the effect of the individual column names listed out
        after the alias name in the "AS" sequence, e.g.::

            >>> print(
            ...     select(
            ...         func.unnest(array(["one", "two", "three"])).
                        table_valued("x", with_ordinality="o").render_derived()
            ...     )
            ... )
            SELECT anon_1.x, anon_1.o
            FROM unnest(ARRAY[%(param_1)s, %(param_2)s, %(param_3)s]) WITH ORDINALITY AS anon_1(x, o)

        The ``with_types`` keyword will render column types inline within
        the alias expression (this syntax currently applies to the
        PostgreSQL database)::

            >>> print(
            ...     select(
            ...         func.json_to_recordset(
            ...             '[{"a":1,"b":"foo"},{"a":"2","c":"bar"}]'
            ...         )
            ...         .table_valued(column("a", Integer), column("b", String))
            ...         .render_derived(with_types=True)
            ...     )
            ... )
            SELECT anon_1.a, anon_1.b FROM json_to_recordset(:json_to_recordset_1)
            AS anon_1(a INTEGER, b VARCHAR)

        :param name: optional string name that will be applied to the alias
         generated.  If left as None, a unique anonymizing name will be used.

        :param with_types: if True, the derived columns will include the
         datatype specification with each column. This is a special syntax
         currently known to be required by PostgreSQL for some SQL functions.

        """  # noqa E501

        # note: don't use the @_generative system here, keep a reference
        # to the original object.  otherwise you can have re-use of the
        # python id() of the original which can cause name conflicts if
        # a new anon-name grabs the same identifier as the local anon-name
        # (just saw it happen on CI)
        new_alias = TableValuedAlias._construct(self, name=name)
        new_alias._render_derived = True
        new_alias._render_derived_w_types = with_types
        return new_alias


class Lateral(AliasedReturnsRows):
    """Represent a LATERAL subquery.

    This object is constructed from the :func:`_expression.lateral` module
    level function as well as the :meth:`_expression.FromClause.lateral`
    method available
    on all :class:`_expression.FromClause` subclasses.

    While LATERAL is part of the SQL standard, currently only more recent
    PostgreSQL versions provide support for this keyword.

    .. versionadded:: 1.1

    .. seealso::

        :ref:`lateral_selects` -  overview of usage.

    """

    __visit_name__ = "lateral"
    _is_lateral = True

    inherit_cache = True

    @classmethod
    def _factory(cls, selectable, name=None):
        """Return a :class:`_expression.Lateral` object.

        :class:`_expression.Lateral` is an :class:`_expression.Alias`
        subclass that represents
        a subquery with the LATERAL keyword applied to it.

        The special behavior of a LATERAL subquery is that it appears in the
        FROM clause of an enclosing SELECT, but may correlate to other
        FROM clauses of that SELECT.   It is a special case of subquery
        only supported by a small number of backends, currently more recent
        PostgreSQL versions.

        .. versionadded:: 1.1

        .. seealso::

            :ref:`lateral_selects` -  overview of usage.

        """
        return coercions.expect(
            roles.FromClauseRole, selectable, explicit_subquery=True
        ).lateral(name=name)


class TableSample(AliasedReturnsRows):
    """Represent a TABLESAMPLE clause.

    This object is constructed from the :func:`_expression.tablesample` module
    level function as well as the :meth:`_expression.FromClause.tablesample`
    method
    available on all :class:`_expression.FromClause` subclasses.

    .. versionadded:: 1.1

    .. seealso::

        :func:`_expression.tablesample`

    """

    __visit_name__ = "tablesample"

    _traverse_internals = AliasedReturnsRows._traverse_internals + [
        ("sampling", InternalTraversal.dp_clauseelement),
        ("seed", InternalTraversal.dp_clauseelement),
    ]

    @classmethod
    def _factory(cls, selectable, sampling, name=None, seed=None):
        """Return a :class:`_expression.TableSample` object.

        :class:`_expression.TableSample` is an :class:`_expression.Alias`
        subclass that represents
        a table with the TABLESAMPLE clause applied to it.
        :func:`_expression.tablesample`
        is also available from the :class:`_expression.FromClause`
        class via the
        :meth:`_expression.FromClause.tablesample` method.

        The TABLESAMPLE clause allows selecting a randomly selected approximate
        percentage of rows from a table. It supports multiple sampling methods,
        most commonly BERNOULLI and SYSTEM.

        e.g.::

            from sqlalchemy import func

            selectable = people.tablesample(
                        func.bernoulli(1),
                        name='alias',
                        seed=func.random())
            stmt = select(selectable.c.people_id)

        Assuming ``people`` with a column ``people_id``, the above
        statement would render as::

            SELECT alias.people_id FROM
            people AS alias TABLESAMPLE bernoulli(:bernoulli_1)
            REPEATABLE (random())

        .. versionadded:: 1.1

        :param sampling: a ``float`` percentage between 0 and 100 or
            :class:`_functions.Function`.

        :param name: optional alias name

        :param seed: any real-valued SQL expression.  When specified, the
         REPEATABLE sub-clause is also rendered.

        """
        return coercions.expect(roles.FromClauseRole, selectable).tablesample(
            sampling, name=name, seed=seed
        )

    @util.preload_module("sqlalchemy.sql.functions")
    def _init(self, selectable, sampling, name=None, seed=None):
        functions = util.preloaded.sql_functions
        if not isinstance(sampling, functions.Function):
            sampling = functions.func.system(sampling)

        self.sampling = sampling
        self.seed = seed
        super(TableSample, self)._init(selectable, name=name)

    def _get_method(self):
        return self.sampling


class CTE(
    roles.DMLTableRole,
    roles.IsCTERole,
    Generative,
    HasPrefixes,
    HasSuffixes,
    AliasedReturnsRows,
):
    """Represent a Common Table Expression.

    The :class:`_expression.CTE` object is obtained using the
    :meth:`_sql.SelectBase.cte` method from any SELECT statement. A less often
    available syntax also allows use of the :meth:`_sql.HasCTE.cte` method
    present on :term:`DML` constructs such as :class:`_sql.Insert`,
    :class:`_sql.Update` and
    :class:`_sql.Delete`.   See the :meth:`_sql.HasCTE.cte` method for
    usage details on CTEs.

    .. seealso::

        :ref:`tutorial_subqueries_ctes` - in the 2.0 tutorial

        :meth:`_sql.HasCTE.cte` - examples of calling styles

    """

    __visit_name__ = "cte"

    _traverse_internals = (
        AliasedReturnsRows._traverse_internals
        + [
            ("_cte_alias", InternalTraversal.dp_clauseelement),
            ("_restates", InternalTraversal.dp_clauseelement_list),
            ("recursive", InternalTraversal.dp_boolean),
        ]
        + HasPrefixes._has_prefixes_traverse_internals
        + HasSuffixes._has_suffixes_traverse_internals
    )

    @classmethod
    def _factory(cls, selectable, name=None, recursive=False):
        r"""Return a new :class:`_expression.CTE`,
        or Common Table Expression instance.

        Please see :meth:`_expression.HasCTE.cte` for detail on CTE usage.

        """
        return coercions.expect(roles.HasCTERole, selectable).cte(
            name=name, recursive=recursive
        )

    def _init(
        self,
        selectable,
        name=None,
        recursive=False,
        _cte_alias=None,
        _restates=(),
        _prefixes=None,
        _suffixes=None,
    ):
        self.recursive = recursive
        self._cte_alias = _cte_alias
        self._restates = _restates
        if _prefixes:
            self._prefixes = _prefixes
        if _suffixes:
            self._suffixes = _suffixes
        super(CTE, self)._init(selectable, name=name)

    def _populate_column_collection(self):
        if self._cte_alias is not None:
            self._cte_alias._generate_fromclause_column_proxies(self)
        else:
            self.element._generate_fromclause_column_proxies(self)

    def alias(self, name=None, flat=False):
        """Return an :class:`_expression.Alias` of this
        :class:`_expression.CTE`.

        This method is a CTE-specific specialization of the
        :meth:`_expression.FromClause.alias` method.

        .. seealso::

            :ref:`core_tutorial_aliases`

            :func:`_expression.alias`

        """
        return CTE._construct(
            self.element,
            name=name,
            recursive=self.recursive,
            _cte_alias=self,
            _prefixes=self._prefixes,
            _suffixes=self._suffixes,
        )

    def union(self, other):
        return CTE._construct(
            self.element.union(other),
            name=self.name,
            recursive=self.recursive,
            _restates=self._restates + (self,),
            _prefixes=self._prefixes,
            _suffixes=self._suffixes,
        )

    def union_all(self, other):
        return CTE._construct(
            self.element.union_all(other),
            name=self.name,
            recursive=self.recursive,
            _restates=self._restates + (self,),
            _prefixes=self._prefixes,
            _suffixes=self._suffixes,
        )


class HasCTE(roles.HasCTERole):
    """Mixin that declares a class to include CTE support.

    .. versionadded:: 1.1

    """

    _has_ctes_traverse_internals = [
        ("_independent_ctes", InternalTraversal.dp_clauseelement_list),
    ]

    _independent_ctes = ()

    @_generative
    def add_cte(self, cte):
        """Add a :class:`_sql.CTE` to this statement object that will be
        independently rendered even if not referenced in the statement
        otherwise.

        This feature is useful for the use case of embedding a DML statement
        such as an INSERT or UPDATE as a CTE inline with a primary statement
        that may draw from its results indirectly; while PostgreSQL is known
        to support this usage, it may not be supported by other backends.

        E.g.::

            from sqlalchemy import table, column, select
            t = table('t', column('c1'), column('c2'))

            ins = t.insert().values({"c1": "x", "c2": "y"}).cte()

            stmt = select(t).add_cte(ins)

        Would render::

            WITH anon_1 AS
            (INSERT INTO t (c1, c2) VALUES (:param_1, :param_2))
            SELECT t.c1, t.c2
            FROM t

        Above, the "anon_1" CTE is not referred towards in the SELECT
        statement, however still accomplishes the task of running an INSERT
        statement.

        Similarly in a DML-related context, using the PostgreSQL
        :class:`_postgresql.Insert` construct to generate an "upsert"::

            from sqlalchemy import table, column
            from sqlalchemy.dialects.postgresql import insert

            t = table("t", column("c1"), column("c2"))

            delete_statement_cte = (
                t.delete().where(t.c.c1 < 1).cte("deletions")
            )

            insert_stmt = insert(t).values({"c1": 1, "c2": 2})
            update_statement = insert_stmt.on_conflict_do_update(
                index_elements=[t.c.c1],
                set_={
                    "c1": insert_stmt.excluded.c1,
                    "c2": insert_stmt.excluded.c2,
                },
            ).add_cte(delete_statement_cte)

            print(update_statement)

        The above statement renders as::

            WITH deletions AS
            (DELETE FROM t WHERE t.c1 < %(c1_1)s)
            INSERT INTO t (c1, c2) VALUES (%(c1)s, %(c2)s)
            ON CONFLICT (c1) DO UPDATE SET c1 = excluded.c1, c2 = excluded.c2

        .. versionadded:: 1.4.21

        """
        cte = coercions.expect(roles.IsCTERole, cte)
        self._independent_ctes += (cte,)

    def cte(self, name=None, recursive=False):
        r"""Return a new :class:`_expression.CTE`,
        or Common Table Expression instance.

        Common table expressions are a SQL standard whereby SELECT
        statements can draw upon secondary statements specified along
        with the primary statement, using a clause called "WITH".
        Special semantics regarding UNION can also be employed to
        allow "recursive" queries, where a SELECT statement can draw
        upon the set of rows that have previously been selected.

        CTEs can also be applied to DML constructs UPDATE, INSERT
        and DELETE on some databases, both as a source of CTE rows
        when combined with RETURNING, as well as a consumer of
        CTE rows.

        .. versionchanged:: 1.1 Added support for UPDATE/INSERT/DELETE as
           CTE, CTEs added to UPDATE/INSERT/DELETE.

        SQLAlchemy detects :class:`_expression.CTE` objects, which are treated
        similarly to :class:`_expression.Alias` objects, as special elements
        to be delivered to the FROM clause of the statement as well
        as to a WITH clause at the top of the statement.

        For special prefixes such as PostgreSQL "MATERIALIZED" and
        "NOT MATERIALIZED", the :meth:`_expression.CTE.prefix_with`
        method may be
        used to establish these.

        .. versionchanged:: 1.3.13 Added support for prefixes.
           In particular - MATERIALIZED and NOT MATERIALIZED.

        :param name: name given to the common table expression.  Like
         :meth:`_expression.FromClause.alias`, the name can be left as
         ``None`` in which case an anonymous symbol will be used at query
         compile time.
        :param recursive: if ``True``, will render ``WITH RECURSIVE``.
         A recursive common table expression is intended to be used in
         conjunction with UNION ALL in order to derive rows
         from those already selected.

        The following examples include two from PostgreSQL's documentation at
        https://www.postgresql.org/docs/current/static/queries-with.html,
        as well as additional examples.

        Example 1, non recursive::

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            orders = Table('orders', metadata,
                Column('region', String),
                Column('amount', Integer),
                Column('product', String),
                Column('quantity', Integer)
            )

            regional_sales = select(
                                orders.c.region,
                                func.sum(orders.c.amount).label('total_sales')
                            ).group_by(orders.c.region).cte("regional_sales")


            top_regions = select(regional_sales.c.region).\
                    where(
                        regional_sales.c.total_sales >
                        select(
                            func.sum(regional_sales.c.total_sales) / 10
                        )
                    ).cte("top_regions")

            statement = select(
                        orders.c.region,
                        orders.c.product,
                        func.sum(orders.c.quantity).label("product_units"),
                        func.sum(orders.c.amount).label("product_sales")
                ).where(orders.c.region.in_(
                    select(top_regions.c.region)
                )).group_by(orders.c.region, orders.c.product)

            result = conn.execute(statement).fetchall()

        Example 2, WITH RECURSIVE::

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            parts = Table('parts', metadata,
                Column('part', String),
                Column('sub_part', String),
                Column('quantity', Integer),
            )

            included_parts = select(\
                parts.c.sub_part, parts.c.part, parts.c.quantity\
                ).\
                where(parts.c.part=='our part').\
                cte(recursive=True)


            incl_alias = included_parts.alias()
            parts_alias = parts.alias()
            included_parts = included_parts.union_all(
                select(
                    parts_alias.c.sub_part,
                    parts_alias.c.part,
                    parts_alias.c.quantity
                ).\
                where(parts_alias.c.part==incl_alias.c.sub_part)
            )

            statement = select(
                        included_parts.c.sub_part,
                        func.sum(included_parts.c.quantity).
                          label('total_quantity')
                    ).\
                    group_by(included_parts.c.sub_part)

            result = conn.execute(statement).fetchall()

        Example 3, an upsert using UPDATE and INSERT with CTEs::

            from datetime import date
            from sqlalchemy import (MetaData, Table, Column, Integer,
                                    Date, select, literal, and_, exists)

            metadata = MetaData()

            visitors = Table('visitors', metadata,
                Column('product_id', Integer, primary_key=True),
                Column('date', Date, primary_key=True),
                Column('count', Integer),
            )

            # add 5 visitors for the product_id == 1
            product_id = 1
            day = date.today()
            count = 5

            update_cte = (
                visitors.update()
                .where(and_(visitors.c.product_id == product_id,
                            visitors.c.date == day))
                .values(count=visitors.c.count + count)
                .returning(literal(1))
                .cte('update_cte')
            )

            upsert = visitors.insert().from_select(
                [visitors.c.product_id, visitors.c.date, visitors.c.count],
                select(literal(product_id), literal(day), literal(count))
                    .where(~exists(update_cte.select()))
            )

            connection.execute(upsert)

        .. seealso::

            :meth:`_orm.Query.cte` - ORM version of
            :meth:`_expression.HasCTE.cte`.

        """
        return CTE._construct(self, name=name, recursive=recursive)


class Subquery(AliasedReturnsRows):
    """Represent a subquery of a SELECT.

    A :class:`.Subquery` is created by invoking the
    :meth:`_expression.SelectBase.subquery` method, or for convenience the
    :meth:`_expression.SelectBase.alias` method, on any
    :class:`_expression.SelectBase` subclass
    which includes :class:`_expression.Select`,
    :class:`_expression.CompoundSelect`, and
    :class:`_expression.TextualSelect`.  As rendered in a FROM clause,
    it represents the
    body of the SELECT statement inside of parenthesis, followed by the usual
    "AS <somename>" that defines all "alias" objects.

    The :class:`.Subquery` object is very similar to the
    :class:`_expression.Alias`
    object and can be used in an equivalent way.    The difference between
    :class:`_expression.Alias` and :class:`.Subquery` is that
    :class:`_expression.Alias` always
    contains a :class:`_expression.FromClause` object whereas
    :class:`.Subquery`
    always contains a :class:`_expression.SelectBase` object.

    .. versionadded:: 1.4 The :class:`.Subquery` class was added which now
       serves the purpose of providing an aliased version of a SELECT
       statement.

    """

    __visit_name__ = "subquery"

    _is_subquery = True

    inherit_cache = True

    @classmethod
    def _factory(cls, selectable, name=None):
        """Return a :class:`.Subquery` object."""
        return coercions.expect(
            roles.SelectStatementRole, selectable
        ).subquery(name=name)

    @util.deprecated(
        "1.4",
        "The :meth:`.Subquery.as_scalar` method, which was previously "
        "``Alias.as_scalar()`` prior to version 1.4, is deprecated and "
        "will be removed in a future release; Please use the "
        ":meth:`_expression.Select.scalar_subquery` method of the "
        ":func:`_expression.select` "
        "construct before constructing a subquery object, or with the ORM "
        "use the :meth:`_query.Query.scalar_subquery` method.",
    )
    def as_scalar(self):
        return self.element.set_label_style(LABEL_STYLE_NONE).scalar_subquery()

    def _execute_on_connection(
        self,
        connection,
        multiparams,
        params,
        execution_options,
    ):
        util.warn_deprecated(
            "Executing a subquery object is deprecated and will raise "
            "ObjectNotExecutableError in an upcoming release.  Please "
            "execute the underlying select() statement directly.",
            "1.4",
        )
        return self.element._execute_on_connection(
            connection, multiparams, params, execution_options, _force=True
        )


class FromGrouping(GroupedElement, FromClause):
    """Represent a grouping of a FROM clause"""

    _traverse_internals = [("element", InternalTraversal.dp_clauseelement)]

    def __init__(self, element):
        self.element = coercions.expect(roles.FromClauseRole, element)

    def _init_collections(self):
        pass

    @property
    def columns(self):
        return self.element.columns

    @property
    def primary_key(self):
        return self.element.primary_key

    @property
    def foreign_keys(self):
        return self.element.foreign_keys

    def is_derived_from(self, element):
        return self.element.is_derived_from(element)

    def alias(self, **kw):
        return FromGrouping(self.element.alias(**kw))

    def _anonymous_fromclause(self, **kw):
        return FromGrouping(self.element._anonymous_fromclause(**kw))

    @property
    def _hide_froms(self):
        return self.element._hide_froms

    @property
    def _from_objects(self):
        return self.element._from_objects

    def __getstate__(self):
        return {"element": self.element}

    def __setstate__(self, state):
        self.element = state["element"]


class TableClause(roles.DMLTableRole, Immutable, FromClause):
    """Represents a minimal "table" construct.

    This is a lightweight table object that has only a name, a
    collection of columns, which are typically produced
    by the :func:`_expression.column` function, and a schema::

        from sqlalchemy import table, column

        user = table("user",
                column("id"),
                column("name"),
                column("description"),
        )

    The :class:`_expression.TableClause` construct serves as the base for
    the more commonly used :class:`_schema.Table` object, providing
    the usual set of :class:`_expression.FromClause` services including
    the ``.c.`` collection and statement generation methods.

    It does **not** provide all the additional schema-level services
    of :class:`_schema.Table`, including constraints, references to other
    tables, or support for :class:`_schema.MetaData`-level services.
    It's useful
    on its own as an ad-hoc construct used to generate quick SQL
    statements when a more fully fledged :class:`_schema.Table`
    is not on hand.

    """

    __visit_name__ = "table"

    _traverse_internals = [
        (
            "columns",
            InternalTraversal.dp_fromclause_canonical_column_collection,
        ),
        ("name", InternalTraversal.dp_string),
    ]

    named_with_column = True

    implicit_returning = False
    """:class:`_expression.TableClause`
    doesn't support having a primary key or column
    -level defaults, so implicit returning doesn't apply."""

    _autoincrement_column = None
    """No PK or default support so no autoincrement column."""

    def __init__(self, name, *columns, **kw):
        """Produce a new :class:`_expression.TableClause`.

        The object returned is an instance of
        :class:`_expression.TableClause`, which
        represents the "syntactical" portion of the schema-level
        :class:`_schema.Table` object.
        It may be used to construct lightweight table constructs.

        .. versionchanged:: 1.0.0 :func:`_expression.table` can now
           be imported from the plain ``sqlalchemy`` namespace like any
           other SQL element.


        :param name: Name of the table.

        :param columns: A collection of :func:`_expression.column` constructs.

        :param schema: The schema name for this table.

            .. versionadded:: 1.3.18 :func:`_expression.table` can now
               accept a ``schema`` argument.
        """

        super(TableClause, self).__init__()
        self.name = self.fullname = name
        self._columns = DedupeColumnCollection()
        self.primary_key = ColumnSet()
        self.foreign_keys = set()
        for c in columns:
            self.append_column(c)

        schema = kw.pop("schema", None)
        if schema is not None:
            self.schema = schema
        if kw:
            raise exc.ArgumentError("Unsupported argument(s): %s" % list(kw))

    def __str__(self):
        if self.schema is not None:
            return self.schema + "." + self.name
        else:
            return self.name

    def _refresh_for_new_column(self, column):
        pass

    def _init_collections(self):
        pass

    @util.memoized_property
    def description(self):
        if util.py3k:
            return self.name
        else:
            return self.name.encode("ascii", "backslashreplace")

    def append_column(self, c, **kw):
        existing = c.table
        if existing is not None and existing is not self:
            raise exc.ArgumentError(
                "column object '%s' already assigned to table '%s'"
                % (c.key, existing)
            )

        self._columns.add(c)
        c.table = self

    @util.preload_module("sqlalchemy.sql.dml")
    def insert(self, values=None, inline=False, **kwargs):
        """Generate an :func:`_expression.insert` construct against this
        :class:`_expression.TableClause`.

        E.g.::

            table.insert().values(name='foo')

        See :func:`_expression.insert` for argument and usage information.

        """
        return util.preloaded.sql_dml.Insert(
            self, values=values, inline=inline, **kwargs
        )

    @util.preload_module("sqlalchemy.sql.dml")
    def update(self, whereclause=None, values=None, inline=False, **kwargs):
        """Generate an :func:`_expression.update` construct against this
        :class:`_expression.TableClause`.

        E.g.::

            table.update().where(table.c.id==7).values(name='foo')

        See :func:`_expression.update` for argument and usage information.

        """
        return util.preloaded.sql_dml.Update(
            self,
            whereclause=whereclause,
            values=values,
            inline=inline,
            **kwargs
        )

    @util.preload_module("sqlalchemy.sql.dml")
    def delete(self, whereclause=None, **kwargs):
        """Generate a :func:`_expression.delete` construct against this
        :class:`_expression.TableClause`.

        E.g.::

            table.delete().where(table.c.id==7)

        See :func:`_expression.delete` for argument and usage information.

        """
        return util.preloaded.sql_dml.Delete(self, whereclause, **kwargs)

    @property
    def _from_objects(self):
        return [self]


class ForUpdateArg(ClauseElement):
    _traverse_internals = [
        ("of", InternalTraversal.dp_clauseelement_list),
        ("nowait", InternalTraversal.dp_boolean),
        ("read", InternalTraversal.dp_boolean),
        ("skip_locked", InternalTraversal.dp_boolean),
    ]

    @classmethod
    def _from_argument(cls, with_for_update):
        if isinstance(with_for_update, ForUpdateArg):
            return with_for_update
        elif with_for_update in (None, False):
            return None
        elif with_for_update is True:
            return ForUpdateArg()
        else:
            return ForUpdateArg(**with_for_update)

    def __eq__(self, other):
        return (
            isinstance(other, ForUpdateArg)
            and other.nowait == self.nowait
            and other.read == self.read
            and other.skip_locked == self.skip_locked
            and other.key_share == self.key_share
            and other.of is self.of
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __init__(
        self,
        nowait=False,
        read=False,
        of=None,
        skip_locked=False,
        key_share=False,
    ):
        """Represents arguments specified to
        :meth:`_expression.Select.for_update`.

        """

        self.nowait = nowait
        self.read = read
        self.skip_locked = skip_locked
        self.key_share = key_share
        if of is not None:
            self.of = [
                coercions.expect(roles.ColumnsClauseRole, elem)
                for elem in util.to_list(of)
            ]
        else:
            self.of = None


class Values(Generative, FromClause):
    """Represent a ``VALUES`` construct that can be used as a FROM element
    in a statement.

    The :class:`_expression.Values` object is created from the
    :func:`_expression.values` function.

    .. versionadded:: 1.4

    """

    named_with_column = True
    __visit_name__ = "values"

    _data = ()

    _traverse_internals = [
        ("_column_args", InternalTraversal.dp_clauseelement_list),
        ("_data", InternalTraversal.dp_dml_multi_values),
        ("name", InternalTraversal.dp_string),
        ("literal_binds", InternalTraversal.dp_boolean),
    ]

    def __init__(self, *columns, **kw):
        r"""Construct a :class:`_expression.Values` construct.

        The column expressions and the actual data for
        :class:`_expression.Values` are given in two separate steps.  The
        constructor receives the column expressions typically as
        :func:`_expression.column` constructs,
        and the data is then passed via the
        :meth:`_expression.Values.data` method as a list,
        which can be called multiple
        times to add more data, e.g.::

            from sqlalchemy import column
            from sqlalchemy import values

            value_expr = values(
                column('id', Integer),
                column('name', String),
                name="my_values"
            ).data(
                [(1, 'name1'), (2, 'name2'), (3, 'name3')]
            )

        :param \*columns: column expressions, typically composed using
         :func:`_expression.column` objects.

        :param name: the name for this VALUES construct.  If omitted, the
         VALUES construct will be unnamed in a SQL expression.   Different
         backends may have different requirements here.

        :param literal_binds: Defaults to False.  Whether or not to render
         the data values inline in the SQL output, rather than using bound
         parameters.

        """

        super(Values, self).__init__()
        self._column_args = columns
        self.name = kw.pop("name", None)
        self.literal_binds = kw.pop("literal_binds", False)
        self.named_with_column = self.name is not None

    @property
    def _column_types(self):
        return [col.type for col in self._column_args]

    @_generative
    def alias(self, name, **kw):
        """Return a new :class:`_expression.Values`
        construct that is a copy of this
        one with the given name.

        This method is a VALUES-specific specialization of the
        :meth:`_expression.FromClause.alias` method.

        .. seealso::

            :ref:`core_tutorial_aliases`

            :func:`_expression.alias`

        """
        self.name = name
        self.named_with_column = self.name is not None

    @_generative
    def lateral(self, name=None):
        """Return a new :class:`_expression.Values` with the lateral flag set,
        so that
        it renders as LATERAL.

        .. seealso::

            :func:`_expression.lateral`

        """
        self._is_lateral = True
        if name is not None:
            self.name = name

    @_generative
    def data(self, values):
        """Return a new :class:`_expression.Values` construct,
        adding the given data
        to the data list.

        E.g.::

            my_values = my_values.data([(1, 'value 1'), (2, 'value2')])

        :param values: a sequence (i.e. list) of tuples that map to the
         column expressions given in the :class:`_expression.Values`
         constructor.

        """

        self._data += (values,)

    def _populate_column_collection(self):
        for c in self._column_args:
            self._columns.add(c)
            c.table = self

    @property
    def _from_objects(self):
        return [self]


class SelectBase(
    roles.SelectStatementRole,
    roles.DMLSelectRole,
    roles.CompoundElementRole,
    roles.InElementRole,
    HasCTE,
    Executable,
    SupportsCloneAnnotations,
    Selectable,
):
    """Base class for SELECT statements.


    This includes :class:`_expression.Select`,
    :class:`_expression.CompoundSelect` and
    :class:`_expression.TextualSelect`.


    """

    _is_select_statement = True
    is_select = True

    def _generate_fromclause_column_proxies(self, fromclause):
        raise NotImplementedError()

    def _refresh_for_new_column(self, column):
        self._reset_memoizations()

    @property
    def selected_columns(self):
        """A :class:`_expression.ColumnCollection`
        representing the columns that
        this SELECT statement or similar construct returns in its result set.

        This collection differs from the :attr:`_expression.FromClause.columns`
        collection of a :class:`_expression.FromClause` in that the columns
        within this collection cannot be directly nested inside another SELECT
        statement; a subquery must be applied first which provides for the
        necessary parenthesization required by SQL.

        .. note::

            The :attr:`_sql.SelectBase.selected_columns` collection does not
            include expressions established in the columns clause using the
            :func:`_sql.text` construct; these are silently omitted from the
            collection. To use plain textual column expressions inside of a
            :class:`_sql.Select` construct, use the :func:`_sql.literal_column`
            construct.

        .. seealso::

            :attr:`_sql.Select.selected_columns`

        .. versionadded:: 1.4

        """
        raise NotImplementedError()

    @property
    def _all_selected_columns(self):
        """A sequence of expressions that correspond to what is rendered
        in the columns clause, including :class:`_sql.TextClause`
        constructs.

        .. versionadded:: 1.4.12

        .. seealso::

            :attr:`_sql.SelectBase.exported_columns`

        """
        raise NotImplementedError()

    @property
    def exported_columns(self):
        """A :class:`_expression.ColumnCollection`
        that represents the "exported"
        columns of this :class:`_expression.Selectable`, not including
        :class:`_sql.TextClause` constructs.

        The "exported" columns for a :class:`_expression.SelectBase`
        object are synonymous
        with the :attr:`_expression.SelectBase.selected_columns` collection.

        .. versionadded:: 1.4

        .. seealso::

            :attr:`_expression.Select.exported_columns`

            :attr:`_expression.Selectable.exported_columns`

            :attr:`_expression.FromClause.exported_columns`


        """
        return self.selected_columns

    @property
    @util.deprecated(
        "1.4",
        "The :attr:`_expression.SelectBase.c` and "
        ":attr:`_expression.SelectBase.columns` attributes "
        "are deprecated and will be removed in a future release; these "
        "attributes implicitly create a subquery that should be explicit.  "
        "Please call :meth:`_expression.SelectBase.subquery` "
        "first in order to create "
        "a subquery, which then contains this attribute.  To access the "
        "columns that this SELECT object SELECTs "
        "from, use the :attr:`_expression.SelectBase.selected_columns` "
        "attribute.",
    )
    def c(self):
        return self._implicit_subquery.columns

    @property
    def columns(self):
        return self.c

    @util.deprecated(
        "1.4",
        "The :meth:`_expression.SelectBase.select` method is deprecated "
        "and will be removed in a future release; this method implicitly "
        "creates a subquery that should be explicit.  "
        "Please call :meth:`_expression.SelectBase.subquery` "
        "first in order to create "
        "a subquery, which then can be selected.",
    )
    def select(self, *arg, **kw):
        return self._implicit_subquery.select(*arg, **kw)

    @HasMemoized.memoized_attribute
    def _implicit_subquery(self):
        return self.subquery()

    @util.deprecated(
        "1.4",
        "The :meth:`_expression.SelectBase.as_scalar` "
        "method is deprecated and will be "
        "removed in a future release.  Please refer to "
        ":meth:`_expression.SelectBase.scalar_subquery`.",
    )
    def as_scalar(self):
        return self.scalar_subquery()

    def exists(self):
        """Return an :class:`_sql.Exists` representation of this selectable,
        which can be used as a column expression.

        The returned object is an instance of :class:`_sql.Exists`.

        .. seealso::

            :func:`_sql.exists`

            :ref:`tutorial_exists` - in the :term:`2.0 style` tutorial.

        .. versionadded:: 1.4

        """
        return Exists(self)

    def scalar_subquery(self):
        """Return a 'scalar' representation of this selectable, which can be
        used as a column expression.

        The returned object is an instance of :class:`_sql.ScalarSelect`.

        Typically, a select statement which has only one column in its columns
        clause is eligible to be used as a scalar expression.  The scalar
        subquery can then be used in the WHERE clause or columns clause of
        an enclosing SELECT.

        Note that the scalar subquery differentiates from the FROM-level
        subquery that can be produced using the
        :meth:`_expression.SelectBase.subquery`
        method.

        .. versionchanged: 1.4 - the ``.as_scalar()`` method was renamed to
           :meth:`_expression.SelectBase.scalar_subquery`.

        .. seealso::

            :ref:`tutorial_scalar_subquery` - in the 2.0 tutorial

            :ref:`scalar_selects` - in the 1.x tutorial

        """
        if self._label_style is not LABEL_STYLE_NONE:
            self = self.set_label_style(LABEL_STYLE_NONE)

        return ScalarSelect(self)

    def label(self, name):
        """Return a 'scalar' representation of this selectable, embedded as a
        subquery with a label.

        .. seealso::

            :meth:`_expression.SelectBase.as_scalar`.

        """
        return self.scalar_subquery().label(name)

    def lateral(self, name=None):
        """Return a LATERAL alias of this :class:`_expression.Selectable`.

        The return value is the :class:`_expression.Lateral` construct also
        provided by the top-level :func:`_expression.lateral` function.

        .. versionadded:: 1.1

        .. seealso::

            :ref:`lateral_selects` -  overview of usage.

        """
        return Lateral._factory(self, name)

    @property
    def _from_objects(self):
        return [self]

    def subquery(self, name=None):
        """Return a subquery of this :class:`_expression.SelectBase`.

        A subquery is from a SQL perspective a parenthesized, named
        construct that can be placed in the FROM clause of another
        SELECT statement.

        Given a SELECT statement such as::

            stmt = select(table.c.id, table.c.name)

        The above statement might look like::

            SELECT table.id, table.name FROM table

        The subquery form by itself renders the same way, however when
        embedded into the FROM clause of another SELECT statement, it becomes
        a named sub-element::

            subq = stmt.subquery()
            new_stmt = select(subq)

        The above renders as::

            SELECT anon_1.id, anon_1.name
            FROM (SELECT table.id, table.name FROM table) AS anon_1

        Historically, :meth:`_expression.SelectBase.subquery`
        is equivalent to calling
        the :meth:`_expression.FromClause.alias`
        method on a FROM object; however,
        as a :class:`_expression.SelectBase`
        object is not directly  FROM object,
        the :meth:`_expression.SelectBase.subquery`
        method provides clearer semantics.

        .. versionadded:: 1.4

        """

        return Subquery._construct(self._ensure_disambiguated_names(), name)

    def _ensure_disambiguated_names(self):
        """Ensure that the names generated by this selectbase will be
        disambiguated in some way, if possible.

        """

        raise NotImplementedError()

    def alias(self, name=None, flat=False):
        """Return a named subquery against this
        :class:`_expression.SelectBase`.

        For a :class:`_expression.SelectBase` (as opposed to a
        :class:`_expression.FromClause`),
        this returns a :class:`.Subquery` object which behaves mostly the
        same as the :class:`_expression.Alias` object that is used with a
        :class:`_expression.FromClause`.

        .. versionchanged:: 1.4 The :meth:`_expression.SelectBase.alias`
           method is now
           a synonym for the :meth:`_expression.SelectBase.subquery` method.

        """
        return self.subquery(name=name)


class SelectStatementGrouping(GroupedElement, SelectBase):
    """Represent a grouping of a :class:`_expression.SelectBase`.

    This differs from :class:`.Subquery` in that we are still
    an "inner" SELECT statement, this is strictly for grouping inside of
    compound selects.

    """

    __visit_name__ = "select_statement_grouping"
    _traverse_internals = [("element", InternalTraversal.dp_clauseelement)]

    _is_select_container = True

    def __init__(self, element):
        self.element = coercions.expect(roles.SelectStatementRole, element)

    def _ensure_disambiguated_names(self):
        new_element = self.element._ensure_disambiguated_names()
        if new_element is not self.element:
            return SelectStatementGrouping(new_element)
        else:
            return self

    def get_label_style(self):
        return self._label_style

    def set_label_style(self, label_style):
        return SelectStatementGrouping(
            self.element.set_label_style(label_style)
        )

    @property
    def _label_style(self):
        return self.element._label_style

    @property
    def select_statement(self):
        return self.element

    def self_group(self, against=None):
        return self

    def _generate_columns_plus_names(self, anon_for_dupe_key):
        return self.element._generate_columns_plus_names(anon_for_dupe_key)

    def _generate_fromclause_column_proxies(self, subquery):
        self.element._generate_fromclause_column_proxies(subquery)

    def _generate_proxy_for_new_column(self, column, subquery):
        return self.element._generate_proxy_for_new_column(subquery)

    @property
    def _all_selected_columns(self):
        return self.element._all_selected_columns

    @property
    def selected_columns(self):
        """A :class:`_expression.ColumnCollection`
        representing the columns that
        the embedded SELECT statement returns in its result set, not including
        :class:`_sql.TextClause` constructs.

        .. versionadded:: 1.4

        .. seealso::

            :attr:`_sql.Select.selected_columns`

        """
        return self.element.selected_columns

    @property
    def _from_objects(self):
        return self.element._from_objects


class DeprecatedSelectBaseGenerations(object):
    """A collection of methods available on :class:`_sql.Select` and
    :class:`_sql.CompoundSelect`, these are all **deprecated** methods as they
    modify the object in-place.

    """

    @util.deprecated(
        "1.4",
        "The :meth:`_expression.GenerativeSelect.append_order_by` "
        "method is deprecated "
        "and will be removed in a future release.  Use the generative method "
        ":meth:`_expression.GenerativeSelect.order_by`.",
    )
    def append_order_by(self, *clauses):
        """Append the given ORDER BY criterion applied to this selectable.

        The criterion will be appended to any pre-existing ORDER BY criterion.

        This is an **in-place** mutation method; the
        :meth:`_expression.GenerativeSelect.order_by` method is preferred,
        as it
        provides standard :term:`method chaining`.

        .. seealso::

            :meth:`_expression.GenerativeSelect.order_by`

        """
        self.order_by.non_generative(self, *clauses)

    @util.deprecated(
        "1.4",
        "The :meth:`_expression.GenerativeSelect.append_group_by` "
        "method is deprecated "
        "and will be removed in a future release.  Use the generative method "
        ":meth:`_expression.GenerativeSelect.group_by`.",
    )
    def append_group_by(self, *clauses):
        """Append the given GROUP BY criterion applied to this selectable.

        The criterion will be appended to any pre-existing GROUP BY criterion.

        This is an **in-place** mutation method; the
        :meth:`_expression.GenerativeSelect.group_by` method is preferred,
        as it
        provides standard :term:`method chaining`.


        """
        self.group_by.non_generative(self, *clauses)


class GenerativeSelect(DeprecatedSelectBaseGenerations, SelectBase):
    """Base class for SELECT statements where additional elements can be
    added.

    This serves as the base for :class:`_expression.Select` and
    :class:`_expression.CompoundSelect`
    where elements such as ORDER BY, GROUP BY can be added and column
    rendering can be controlled.  Compare to
    :class:`_expression.TextualSelect`, which,
    while it subclasses :class:`_expression.SelectBase`
    and is also a SELECT construct,
    represents a fixed textual string which cannot be altered at this level,
    only wrapped as a subquery.

    """

    _order_by_clauses = ()
    _group_by_clauses = ()
    _limit_clause = None
    _offset_clause = None
    _fetch_clause = None
    _fetch_clause_options = None
    _for_update_arg = None

    @util.deprecated_params(
        bind=(
            "2.0",
            "The :paramref:`_sql.select.bind` argument is deprecated and "
            "will be removed in SQLAlchemy 2.0.",
        ),
    )
    def __init__(
        self,
        _label_style=LABEL_STYLE_DEFAULT,
        use_labels=False,
        limit=None,
        offset=None,
        order_by=None,
        group_by=None,
        bind=None,
    ):
        if use_labels:
            if util.SQLALCHEMY_WARN_20:
                util.warn_deprecated_20(
                    "The use_labels=True keyword argument to GenerativeSelect "
                    "is deprecated and will be removed in version 2.0. Please "
                    "use "
                    "select.set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL) "
                    "if you need to replicate this legacy behavior.",
                    stacklevel=4,
                )
            _label_style = LABEL_STYLE_TABLENAME_PLUS_COL

        self._label_style = _label_style

        if limit is not None:
            self.limit.non_generative(self, limit)
        if offset is not None:
            self.offset.non_generative(self, offset)

        if order_by is not None:
            self.order_by.non_generative(self, *util.to_list(order_by))
        if group_by is not None:
            self.group_by.non_generative(self, *util.to_list(group_by))

        self._bind = bind

    @_generative
    def with_for_update(
        self,
        nowait=False,
        read=False,
        of=None,
        skip_locked=False,
        key_share=False,
    ):
        """Specify a ``FOR UPDATE`` clause for this
        :class:`_expression.GenerativeSelect`.

        E.g.::

            stmt = select(table).with_for_update(nowait=True)

        On a database like PostgreSQL or Oracle, the above would render a
        statement like::

            SELECT table.a, table.b FROM table FOR UPDATE NOWAIT

        on other backends, the ``nowait`` option is ignored and instead
        would produce::

            SELECT table.a, table.b FROM table FOR UPDATE

        When called with no arguments, the statement will render with
        the suffix ``FOR UPDATE``.   Additional arguments can then be
        provided which allow for common database-specific
        variants.

        :param nowait: boolean; will render ``FOR UPDATE NOWAIT`` on Oracle
         and PostgreSQL dialects.

        :param read: boolean; will render ``LOCK IN SHARE MODE`` on MySQL,
         ``FOR SHARE`` on PostgreSQL.  On PostgreSQL, when combined with
         ``nowait``, will render ``FOR SHARE NOWAIT``.

        :param of: SQL expression or list of SQL expression elements
         (typically :class:`_schema.Column`
         objects or a compatible expression) which
         will render into a ``FOR UPDATE OF`` clause; supported by PostgreSQL
         and Oracle.  May render as a table or as a column depending on
         backend.

        :param skip_locked: boolean, will render ``FOR UPDATE SKIP LOCKED``
         on Oracle and PostgreSQL dialects or ``FOR SHARE SKIP LOCKED`` if
         ``read=True`` is also specified.

        :param key_share: boolean, will render ``FOR NO KEY UPDATE``,
         or if combined with ``read=True`` will render ``FOR KEY SHARE``,
         on the PostgreSQL dialect.

        """
        self._for_update_arg = ForUpdateArg(
            nowait=nowait,
            read=read,
            of=of,
            skip_locked=skip_locked,
            key_share=key_share,
        )

    def get_label_style(self):
        """
        Retrieve the current label style.

        .. versionadded:: 1.4

        """
        return self._label_style

    def set_label_style(self, style):
        """Return a new selectable with the specified label style.

        There are three "label styles" available,
        :data:`_sql.LABEL_STYLE_DISAMBIGUATE_ONLY`,
        :data:`_sql.LABEL_STYLE_TABLENAME_PLUS_COL`, and
        :data:`_sql.LABEL_STYLE_NONE`.   The default style is
        :data:`_sql.LABEL_STYLE_TABLENAME_PLUS_COL`.

        In modern SQLAlchemy, there is not generally a need to change the
        labeling style, as per-expression labels are more effectively used by
        making use of the :meth:`_sql.ColumnElement.label` method. In past
        versions, :data:`_sql.LABEL_STYLE_TABLENAME_PLUS_COL` was used to
        disambiguate same-named columns from different tables, aliases, or
        subqueries; the newer :data:`_sql.LABEL_STYLE_DISAMBIGUATE_ONLY` now
        applies labels only to names that conflict with an existing name so
        that the impact of this labeling is minimal.

        The rationale for disambiguation is mostly so that all column
        expressions are available from a given :attr:`_sql.FromClause.c`
        collection when a subquery is created.

        .. versionadded:: 1.4 - the
            :meth:`_sql.GenerativeSelect.set_label_style` method replaces the
            previous combination of ``.apply_labels()``, ``.with_labels()`` and
            ``use_labels=True`` methods and/or parameters.

        .. seealso::

            :data:`_sql.LABEL_STYLE_DISAMBIGUATE_ONLY`

            :data:`_sql.LABEL_STYLE_TABLENAME_PLUS_COL`

            :data:`_sql.LABEL_STYLE_NONE`

            :data:`_sql.LABEL_STYLE_DEFAULT`

        """
        if self._label_style is not style:
            self = self._generate()
            self._label_style = style
        return self

    @util.deprecated_20(
        ":meth:`_sql.GenerativeSelect.apply_labels`",
        alternative="Use set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL) "
        "instead.",
    )
    def apply_labels(self):
        return self.set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)

    @property
    def _group_by_clause(self):
        """ClauseList access to group_by_clauses for legacy dialects"""
        return ClauseList._construct_raw(
            operators.comma_op, self._group_by_clauses
        )

    @property
    def _order_by_clause(self):
        """ClauseList access to order_by_clauses for legacy dialects"""
        return ClauseList._construct_raw(
            operators.comma_op, self._order_by_clauses
        )

    def _offset_or_limit_clause(self, element, name=None, type_=None):
        """Convert the given value to an "offset or limit" clause.

        This handles incoming integers and converts to an expression; if
        an expression is already given, it is passed through.

        """
        return coercions.expect(
            roles.LimitOffsetRole, element, name=name, type_=type_
        )

    def _offset_or_limit_clause_asint(self, clause, attrname):
        """Convert the "offset or limit" clause of a select construct to an
        integer.

        This is only possible if the value is stored as a simple bound
        parameter. Otherwise, a compilation error is raised.

        """
        if clause is None:
            return None
        try:
            value = clause._limit_offset_value
        except AttributeError as err:
            util.raise_(
                exc.CompileError(
                    "This SELECT structure does not use a simple "
                    "integer value for %s" % attrname
                ),
                replace_context=err,
            )
        else:
            return util.asint(value)

    @property
    def _limit(self):
        """Get an integer value for the limit.  This should only be used
        by code that cannot support a limit as a BindParameter or
        other custom clause as it will throw an exception if the limit
        isn't currently set to an integer.

        """
        return self._offset_or_limit_clause_asint(self._limit_clause, "limit")

    def _simple_int_clause(self, clause):
        """True if the clause is a simple integer, False
        if it is not present or is a SQL expression.
        """
        return isinstance(clause, _OffsetLimitParam)

    @property
    def _offset(self):
        """Get an integer value for the offset.  This should only be used
        by code that cannot support an offset as a BindParameter or
        other custom clause as it will throw an exception if the
        offset isn't currently set to an integer.

        """
        return self._offset_or_limit_clause_asint(
            self._offset_clause, "offset"
        )

    @property
    def _has_row_limiting_clause(self):
        return (
            self._limit_clause is not None
            or self._offset_clause is not None
            or self._fetch_clause is not None
        )

    @_generative
    def limit(self, limit):
        """Return a new selectable with the given LIMIT criterion
        applied.

        This is a numerical value which usually renders as a ``LIMIT``
        expression in the resulting select.  Backends that don't
        support ``LIMIT`` will attempt to provide similar
        functionality.

        .. note::

           The :meth:`_sql.GenerativeSelect.limit` method will replace
           any clause applied with :meth:`_sql.GenerativeSelect.fetch`.

        .. versionchanged:: 1.0.0 - :meth:`_expression.Select.limit` can now
           accept arbitrary SQL expressions as well as integer values.

        :param limit: an integer LIMIT parameter, or a SQL expression
         that provides an integer result. Pass ``None`` to reset it.

        .. seealso::

           :meth:`_sql.GenerativeSelect.fetch`

           :meth:`_sql.GenerativeSelect.offset`

        """

        self._fetch_clause = self._fetch_clause_options = None
        self._limit_clause = self._offset_or_limit_clause(limit)

    @_generative
    def fetch(self, count, with_ties=False, percent=False):
        """Return a new selectable with the given FETCH FIRST criterion
        applied.

        This is a numeric value which usually renders as
        ``FETCH {FIRST | NEXT} [ count ] {ROW | ROWS} {ONLY | WITH TIES}``
        expression in the resulting select. This functionality is
        is currently implemented for Oracle, PostgreSQL, MSSQL.

        Use :meth:`_sql.GenerativeSelect.offset` to specify the offset.

        .. note::

           The :meth:`_sql.GenerativeSelect.fetch` method will replace
           any clause applied with :meth:`_sql.GenerativeSelect.limit`.

        .. versionadded:: 1.4

        :param count: an integer COUNT parameter, or a SQL expression
         that provides an integer result. When ``percent=True`` this will
         represent the percentage of rows to return, not the absolute value.
         Pass ``None`` to reset it.

        :param with_ties: When ``True``, the WITH TIES option is used
         to return any additional rows that tie for the last place in the
         result set according to the ``ORDER BY`` clause. The
         ``ORDER BY`` may be mandatory in this case. Defaults to ``False``

        :param percent: When ``True``, ``count`` represents the percentage
         of the total number of selected rows to return. Defaults to ``False``

        .. seealso::

           :meth:`_sql.GenerativeSelect.limit`

           :meth:`_sql.GenerativeSelect.offset`

        """

        self._limit_clause = None
        if count is None:
            self._fetch_clause = self._fetch_clause_options = None
        else:
            self._fetch_clause = self._offset_or_limit_clause(count)
            self._fetch_clause_options = {
                "with_ties": with_ties,
                "percent": percent,
            }

    @_generative
    def offset(self, offset):
        """Return a new selectable with the given OFFSET criterion
        applied.


        This is a numeric value which usually renders as an ``OFFSET``
        expression in the resulting select.  Backends that don't
        support ``OFFSET`` will attempt to provide similar
        functionality.


        .. versionchanged:: 1.0.0 - :meth:`_expression.Select.offset` can now
           accept arbitrary SQL expressions as well as integer values.

        :param offset: an integer OFFSET parameter, or a SQL expression
         that provides an integer result. Pass ``None`` to reset it.

        .. seealso::

           :meth:`_sql.GenerativeSelect.limit`

           :meth:`_sql.GenerativeSelect.fetch`

        """

        self._offset_clause = self._offset_or_limit_clause(offset)

    @_generative
    @util.preload_module("sqlalchemy.sql.util")
    def slice(self, start, stop):
        """Apply LIMIT / OFFSET to this statement based on a slice.

        The start and stop indices behave like the argument to Python's
        built-in :func:`range` function. This method provides an
        alternative to using ``LIMIT``/``OFFSET`` to get a slice of the
        query.

        For example, ::

            stmt = select(User).order_by(User).id.slice(1, 3)

        renders as

        .. sourcecode:: sql

           SELECT users.id AS users_id,
                  users.name AS users_name
           FROM users ORDER BY users.id
           LIMIT ? OFFSET ?
           (2, 1)

        .. note::

           The :meth:`_sql.GenerativeSelect.slice` method will replace
           any clause applied with :meth:`_sql.GenerativeSelect.fetch`.

        .. versionadded:: 1.4  Added the :meth:`_sql.GenerativeSelect.slice`
           method generalized from the ORM.

        .. seealso::

           :meth:`_sql.GenerativeSelect.limit`

           :meth:`_sql.GenerativeSelect.offset`

           :meth:`_sql.GenerativeSelect.fetch`

        """
        sql_util = util.preloaded.sql_util
        self._fetch_clause = self._fetch_clause_options = None
        self._limit_clause, self._offset_clause = sql_util._make_slice(
            self._limit_clause, self._offset_clause, start, stop
        )

    @_generative
    def order_by(self, *clauses):
        r"""Return a new selectable with the given list of ORDER BY
        criterion applied.

        e.g.::

            stmt = select(table).order_by(table.c.id, table.c.name)

        :param \*clauses: a series of :class:`_expression.ColumnElement`
         constructs
         which will be used to generate an ORDER BY clause.

        .. seealso::

            :ref:`tutorial_order_by` - in the :ref:`unified_tutorial`

            :ref:`tutorial_order_by_label` - in the :ref:`unified_tutorial`

        """

        if len(clauses) == 1 and clauses[0] is None:
            self._order_by_clauses = ()
        else:
            self._order_by_clauses += tuple(
                coercions.expect(roles.OrderByRole, clause)
                for clause in clauses
            )

    @_generative
    def group_by(self, *clauses):
        r"""Return a new selectable with the given list of GROUP BY
        criterion applied.

        e.g.::

            stmt = select(table.c.name, func.max(table.c.stat)).\
            group_by(table.c.name)

        :param \*clauses: a series of :class:`_expression.ColumnElement`
         constructs
         which will be used to generate an GROUP BY clause.

        .. seealso::

            :ref:`tutorial_group_by_w_aggregates` - in the
            :ref:`unified_tutorial`

            :ref:`tutorial_order_by_label` - in the :ref:`unified_tutorial`

        """

        if len(clauses) == 1 and clauses[0] is None:
            self._group_by_clauses = ()
        else:
            self._group_by_clauses += tuple(
                coercions.expect(roles.GroupByRole, clause)
                for clause in clauses
            )


@CompileState.plugin_for("default", "compound_select")
class CompoundSelectState(CompileState):
    @util.memoized_property
    def _label_resolve_dict(self):
        # TODO: this is hacky and slow
        hacky_subquery = self.statement.subquery()
        hacky_subquery.named_with_column = False
        d = dict((c.key, c) for c in hacky_subquery.c)
        return d, d, d


class CompoundSelect(HasCompileState, GenerativeSelect):
    """Forms the basis of ``UNION``, ``UNION ALL``, and other
    SELECT-based set operations.


    .. seealso::

        :func:`_expression.union`

        :func:`_expression.union_all`

        :func:`_expression.intersect`

        :func:`_expression.intersect_all`

        :func:`_expression.except`

        :func:`_expression.except_all`

    """

    __visit_name__ = "compound_select"

    _traverse_internals = [
        ("selects", InternalTraversal.dp_clauseelement_list),
        ("_limit_clause", InternalTraversal.dp_clauseelement),
        ("_offset_clause", InternalTraversal.dp_clauseelement),
        ("_fetch_clause", InternalTraversal.dp_clauseelement),
        ("_fetch_clause_options", InternalTraversal.dp_plain_dict),
        ("_order_by_clauses", InternalTraversal.dp_clauseelement_list),
        ("_group_by_clauses", InternalTraversal.dp_clauseelement_list),
        ("_for_update_arg", InternalTraversal.dp_clauseelement),
        ("keyword", InternalTraversal.dp_string),
    ] + SupportsCloneAnnotations._clone_annotations_traverse_internals

    UNION = util.symbol("UNION")
    UNION_ALL = util.symbol("UNION ALL")
    EXCEPT = util.symbol("EXCEPT")
    EXCEPT_ALL = util.symbol("EXCEPT ALL")
    INTERSECT = util.symbol("INTERSECT")
    INTERSECT_ALL = util.symbol("INTERSECT ALL")

    _is_from_container = True

    def __init__(self, keyword, *selects, **kwargs):
        self._auto_correlate = kwargs.pop("correlate", False)
        self.keyword = keyword
        self.selects = [
            coercions.expect(roles.CompoundElementRole, s).self_group(
                against=self
            )
            for s in selects
        ]

        if kwargs and util.SQLALCHEMY_WARN_20:
            util.warn_deprecated_20(
                "Set functions such as union(), union_all(), extract(), etc. "
                "in SQLAlchemy 2.0 will accept a "
                "series of SELECT statements only. "
                "Please use generative methods such as order_by() for "
                "additional modifications to this CompoundSelect.",
                stacklevel=4,
            )

        GenerativeSelect.__init__(self, **kwargs)

    @classmethod
    def _create_union(cls, *selects, **kwargs):
        r"""Return a ``UNION`` of multiple selectables.

        The returned object is an instance of
        :class:`_expression.CompoundSelect`.

        A similar :func:`union()` method is available on all
        :class:`_expression.FromClause` subclasses.

        :param \*selects:
          a list of :class:`_expression.Select` instances.

        :param \**kwargs:
          available keyword arguments are the same as those of
          :func:`select`.

        """
        return CompoundSelect(CompoundSelect.UNION, *selects, **kwargs)

    @classmethod
    def _create_union_all(cls, *selects, **kwargs):
        r"""Return a ``UNION ALL`` of multiple selectables.

        The returned object is an instance of
        :class:`_expression.CompoundSelect`.

        A similar :func:`union_all()` method is available on all
        :class:`_expression.FromClause` subclasses.

        :param \*selects:
          a list of :class:`_expression.Select` instances.

        :param \**kwargs:
          available keyword arguments are the same as those of
          :func:`select`.

        """
        return CompoundSelect(CompoundSelect.UNION_ALL, *selects, **kwargs)

    @classmethod
    def _create_except(cls, *selects, **kwargs):
        r"""Return an ``EXCEPT`` of multiple selectables.

        The returned object is an instance of
        :class:`_expression.CompoundSelect`.

        :param \*selects:
          a list of :class:`_expression.Select` instances.

        :param \**kwargs:
          available keyword arguments are the same as those of
          :func:`select`.

        """
        return CompoundSelect(CompoundSelect.EXCEPT, *selects, **kwargs)

    @classmethod
    def _create_except_all(cls, *selects, **kwargs):
        r"""Return an ``EXCEPT ALL`` of multiple selectables.

        The returned object is an instance of
        :class:`_expression.CompoundSelect`.

        :param \*selects:
          a list of :class:`_expression.Select` instances.

        :param \**kwargs:
          available keyword arguments are the same as those of
          :func:`select`.

        """
        return CompoundSelect(CompoundSelect.EXCEPT_ALL, *selects, **kwargs)

    @classmethod
    def _create_intersect(cls, *selects, **kwargs):
        r"""Return an ``INTERSECT`` of multiple selectables.

        The returned object is an instance of
        :class:`_expression.CompoundSelect`.

        :param \*selects:
          a list of :class:`_expression.Select` instances.

        :param \**kwargs:
          available keyword arguments are the same as those of
          :func:`select`.

        """
        return CompoundSelect(CompoundSelect.INTERSECT, *selects, **kwargs)

    @classmethod
    def _create_intersect_all(cls, *selects, **kwargs):
        r"""Return an ``INTERSECT ALL`` of multiple selectables.

        The returned object is an instance of
        :class:`_expression.CompoundSelect`.

        :param \*selects:
          a list of :class:`_expression.Select` instances.

        :param \**kwargs:
          available keyword arguments are the same as those of
          :func:`select`.

        """
        return CompoundSelect(CompoundSelect.INTERSECT_ALL, *selects, **kwargs)

    def _scalar_type(self):
        return self.selects[0]._scalar_type()

    def self_group(self, against=None):
        return SelectStatementGrouping(self)

    def is_derived_from(self, fromclause):
        for s in self.selects:
            if s.is_derived_from(fromclause):
                return True
        return False

    def _set_label_style(self, style):
        if self._label_style is not style:
            self = self._generate()
            select_0 = self.selects[0]._set_label_style(style)
            self.selects = [select_0] + self.selects[1:]

        return self

    def _ensure_disambiguated_names(self):
        new_select = self.selects[0]._ensure_disambiguated_names()
        if new_select is not self.selects[0]:
            self = self._generate()
            self.selects = [new_select] + self.selects[1:]

        return self

    def _generate_fromclause_column_proxies(self, subquery):

        # this is a slightly hacky thing - the union exports a
        # column that resembles just that of the *first* selectable.
        # to get at a "composite" column, particularly foreign keys,
        # you have to dig through the proxies collection which we
        # generate below.  We may want to improve upon this, such as
        # perhaps _make_proxy can accept a list of other columns
        # that are "shared" - schema.column can then copy all the
        # ForeignKeys in. this would allow the union() to have all
        # those fks too.
        select_0 = self.selects[0]

        if self._label_style is not LABEL_STYLE_DEFAULT:
            select_0 = select_0.set_label_style(self._label_style)
        select_0._generate_fromclause_column_proxies(subquery)

        # hand-construct the "_proxies" collection to include all
        # derived columns place a 'weight' annotation corresponding
        # to how low in the list of select()s the column occurs, so
        # that the corresponding_column() operation can resolve
        # conflicts

        for subq_col, select_cols in zip(
            subquery.c._all_columns,
            zip(*[s.selected_columns for s in self.selects]),
        ):
            subq_col._proxies = [
                c._annotate({"weight": i + 1})
                for (i, c) in enumerate(select_cols)
            ]

    def _refresh_for_new_column(self, column):
        super(CompoundSelect, self)._refresh_for_new_column(column)
        for select in self.selects:
            select._refresh_for_new_column(column)

    @property
    def _all_selected_columns(self):
        return self.selects[0]._all_selected_columns

    @property
    def selected_columns(self):
        """A :class:`_expression.ColumnCollection`
        representing the columns that
        this SELECT statement or similar construct returns in its result set,
        not including :class:`_sql.TextClause` constructs.

        For a :class:`_expression.CompoundSelect`, the
        :attr:`_expression.CompoundSelect.selected_columns`
        attribute returns the selected
        columns of the first SELECT statement contained within the series of
        statements within the set operation.

        .. seealso::

            :attr:`_sql.Select.selected_columns`

        .. versionadded:: 1.4

        """
        return self.selects[0].selected_columns

    @property
    @util.deprecated_20(
        ":attr:`.Executable.bind`",
        alternative="Bound metadata is being removed as of SQLAlchemy 2.0.",
        enable_warnings=False,
    )
    def bind(self):
        """Returns the :class:`_engine.Engine` or :class:`_engine.Connection`
        to which this :class:`.Executable` is bound, or None if none found.

        """
        if self._bind:
            return self._bind
        for s in self.selects:
            e = s.bind
            if e:
                return e
        else:
            return None

    @bind.setter
    def bind(self, bind):
        self._bind = bind


class DeprecatedSelectGenerations(object):
    """A collection of methods available on :class:`_sql.Select`, these
    are all **deprecated** methods as they modify the :class:`_sql.Select`
    object in -place.

    """

    @util.deprecated(
        "1.4",
        "The :meth:`_expression.Select.append_correlation` "
        "method is deprecated "
        "and will be removed in a future release.  Use the generative "
        "method :meth:`_expression.Select.correlate`.",
    )
    def append_correlation(self, fromclause):
        """Append the given correlation expression to this select()
        construct.

        This is an **in-place** mutation method; the
        :meth:`_expression.Select.correlate` method is preferred,
        as it provides
        standard :term:`method chaining`.

        """

        self.correlate.non_generative(self, fromclause)

    @util.deprecated(
        "1.4",
        "The :meth:`_expression.Select.append_column` method is deprecated "
        "and will be removed in a future release.  Use the generative "
        "method :meth:`_expression.Select.add_columns`.",
    )
    def append_column(self, column):
        """Append the given column expression to the columns clause of this
        select() construct.

        E.g.::

            my_select.append_column(some_table.c.new_column)

        This is an **in-place** mutation method; the
        :meth:`_expression.Select.add_columns` method is preferred,
        as it provides standard
        :term:`method chaining`.

        """
        self.add_columns.non_generative(self, column)

    @util.deprecated(
        "1.4",
        "The :meth:`_expression.Select.append_prefix` method is deprecated "
        "and will be removed in a future release.  Use the generative "
        "method :meth:`_expression.Select.prefix_with`.",
    )
    def append_prefix(self, clause):
        """Append the given columns clause prefix expression to this select()
        construct.

        This is an **in-place** mutation method; the
        :meth:`_expression.Select.prefix_with` method is preferred,
        as it provides
        standard :term:`method chaining`.

        """
        self.prefix_with.non_generative(self, clause)

    @util.deprecated(
        "1.4",
        "The :meth:`_expression.Select.append_whereclause` "
        "method is deprecated "
        "and will be removed in a future release.  Use the generative "
        "method :meth:`_expression.Select.where`.",
    )
    def append_whereclause(self, whereclause):
        """Append the given expression to this select() construct's WHERE
        criterion.

        The expression will be joined to existing WHERE criterion via AND.

        This is an **in-place** mutation method; the
        :meth:`_expression.Select.where` method is preferred,
        as it provides standard
        :term:`method chaining`.

        """
        self.where.non_generative(self, whereclause)

    @util.deprecated(
        "1.4",
        "The :meth:`_expression.Select.append_having` method is deprecated "
        "and will be removed in a future release.  Use the generative "
        "method :meth:`_expression.Select.having`.",
    )
    def append_having(self, having):
        """Append the given expression to this select() construct's HAVING
        criterion.

        The expression will be joined to existing HAVING criterion via AND.

        This is an **in-place** mutation method; the
        :meth:`_expression.Select.having` method is preferred,
        as it provides standard
        :term:`method chaining`.

        """

        self.having.non_generative(self, having)

    @util.deprecated(
        "1.4",
        "The :meth:`_expression.Select.append_from` method is deprecated "
        "and will be removed in a future release.  Use the generative "
        "method :meth:`_expression.Select.select_from`.",
    )
    def append_from(self, fromclause):
        """Append the given :class:`_expression.FromClause` expression
        to this select() construct's FROM clause.

        This is an **in-place** mutation method; the
        :meth:`_expression.Select.select_from` method is preferred,
        as it provides
        standard :term:`method chaining`.

        """
        self.select_from.non_generative(self, fromclause)


@CompileState.plugin_for("default", "select")
class SelectState(util.MemoizedSlots, CompileState):
    __slots__ = (
        "from_clauses",
        "froms",
        "columns_plus_names",
        "_label_resolve_dict",
    )

    class default_select_compile_options(CacheableOptions):
        _cache_key_traversal = []

    def __init__(self, statement, compiler, **kw):
        self.statement = statement
        self.from_clauses = statement._from_obj

        for memoized_entities in statement._memoized_select_entities:
            self._setup_joins(
                memoized_entities._setup_joins, memoized_entities._raw_columns
            )

        if statement._setup_joins:
            self._setup_joins(statement._setup_joins, statement._raw_columns)

        self.froms = self._get_froms(statement)

        self.columns_plus_names = statement._generate_columns_plus_names(True)

    @classmethod
    def _plugin_not_implemented(cls):
        raise NotImplementedError(
            "The default SELECT construct without plugins does not "
            "implement this method."
        )

    @classmethod
    def get_column_descriptions(cls, statement):
        cls._plugin_not_implemented()

    @classmethod
    def from_statement(cls, statement, from_statement):
        cls._plugin_not_implemented()

    @classmethod
    def _column_naming_convention(cls, label_style):

        table_qualified = label_style is LABEL_STYLE_TABLENAME_PLUS_COL
        dedupe = label_style is not LABEL_STYLE_NONE

        pa = prefix_anon_map()
        names = set()

        def go(c, col_name=None):
            if c._is_text_clause:
                return None

            elif not dedupe:
                name = c._proxy_key
                if name is None:
                    name = "_no_label"
                return name

            name = c._tq_key_label if table_qualified else c._proxy_key

            if name is None:
                name = "_no_label"
                if name in names:
                    return c._anon_label(name) % pa
                else:
                    names.add(name)
                    return name

            elif name in names:
                return (
                    c._anon_tq_key_label % pa
                    if table_qualified
                    else c._anon_key_label % pa
                )
            else:
                names.add(name)
                return name

        return go

    def _get_froms(self, statement):
        return self._normalize_froms(
            itertools.chain(
                itertools.chain.from_iterable(
                    [
                        element._from_objects
                        for element in statement._raw_columns
                    ]
                ),
                itertools.chain.from_iterable(
                    [
                        element._from_objects
                        for element in statement._where_criteria
                    ]
                ),
                self.from_clauses,
            ),
            check_statement=statement,
        )

    def _normalize_froms(self, iterable_of_froms, check_statement=None):
        """given an iterable of things to select FROM, reduce them to what
        would actually render in the FROM clause of a SELECT.

        This does the job of checking for JOINs, tables, etc. that are in fact
        overlapping due to cloning, adaption, present in overlapping joins,
        etc.

        """
        seen = set()
        froms = []

        for item in iterable_of_froms:
            if item._is_subquery and item.element is check_statement:
                raise exc.InvalidRequestError(
                    "select() construct refers to itself as a FROM"
                )

            if not seen.intersection(item._cloned_set):
                froms.append(item)
                seen.update(item._cloned_set)

        if froms:
            toremove = set(
                itertools.chain.from_iterable(
                    [_expand_cloned(f._hide_froms) for f in froms]
                )
            )
            if toremove:
                # filter out to FROM clauses not in the list,
                # using a list to maintain ordering
                froms = [f for f in froms if f not in toremove]

        return froms

    def _get_display_froms(
        self, explicit_correlate_froms=None, implicit_correlate_froms=None
    ):
        """Return the full list of 'from' clauses to be displayed.

        Takes into account a set of existing froms which may be
        rendered in the FROM clause of enclosing selects; this Select
        may want to leave those absent if it is automatically
        correlating.

        """

        froms = self.froms

        if self.statement._correlate:
            to_correlate = self.statement._correlate
            if to_correlate:
                froms = [
                    f
                    for f in froms
                    if f
                    not in _cloned_intersection(
                        _cloned_intersection(
                            froms, explicit_correlate_froms or ()
                        ),
                        to_correlate,
                    )
                ]

        if self.statement._correlate_except is not None:

            froms = [
                f
                for f in froms
                if f
                not in _cloned_difference(
                    _cloned_intersection(
                        froms, explicit_correlate_froms or ()
                    ),
                    self.statement._correlate_except,
                )
            ]

        if (
            self.statement._auto_correlate
            and implicit_correlate_froms
            and len(froms) > 1
        ):

            froms = [
                f
                for f in froms
                if f
                not in _cloned_intersection(froms, implicit_correlate_froms)
            ]

            if not len(froms):
                raise exc.InvalidRequestError(
                    "Select statement '%r"
                    "' returned no FROM clauses "
                    "due to auto-correlation; "
                    "specify correlate(<tables>) "
                    "to control correlation "
                    "manually." % self.statement
                )

        return froms

    def _memoized_attr__label_resolve_dict(self):
        with_cols = dict(
            (c._resolve_label or c._tq_label or c.key, c)
            for c in self.statement._all_selected_columns
            if c._allow_label_resolve
        )
        only_froms = dict(
            (c.key, c)
            for c in _select_iterables(self.froms)
            if c._allow_label_resolve
        )
        only_cols = with_cols.copy()
        for key, value in only_froms.items():
            with_cols.setdefault(key, value)

        return with_cols, only_froms, only_cols

    @classmethod
    def determine_last_joined_entity(cls, stmt):
        if stmt._setup_joins:
            return stmt._setup_joins[-1][0]
        else:
            return None

    @classmethod
    def all_selected_columns(cls, statement):
        return [c for c in _select_iterables(statement._raw_columns)]

    def _setup_joins(self, args, raw_columns):
        for (right, onclause, left, flags) in args:
            isouter = flags["isouter"]
            full = flags["full"]

            if left is None:
                (
                    left,
                    replace_from_obj_index,
                ) = self._join_determine_implicit_left_side(
                    raw_columns, left, right, onclause
                )
            else:
                (replace_from_obj_index) = self._join_place_explicit_left_side(
                    left
                )

            if replace_from_obj_index is not None:
                # splice into an existing element in the
                # self._from_obj list
                left_clause = self.from_clauses[replace_from_obj_index]

                self.from_clauses = (
                    self.from_clauses[:replace_from_obj_index]
                    + (
                        Join(
                            left_clause,
                            right,
                            onclause,
                            isouter=isouter,
                            full=full,
                        ),
                    )
                    + self.from_clauses[replace_from_obj_index + 1 :]
                )
            else:

                self.from_clauses = self.from_clauses + (
                    Join(left, right, onclause, isouter=isouter, full=full),
                )

    @util.preload_module("sqlalchemy.sql.util")
    def _join_determine_implicit_left_side(
        self, raw_columns, left, right, onclause
    ):
        """When join conditions don't express the left side explicitly,
        determine if an existing FROM or entity in this query
        can serve as the left hand side.

        """

        sql_util = util.preloaded.sql_util

        replace_from_obj_index = None

        from_clauses = self.from_clauses

        if from_clauses:

            indexes = sql_util.find_left_clause_to_join_from(
                from_clauses, right, onclause
            )

            if len(indexes) == 1:
                replace_from_obj_index = indexes[0]
                left = from_clauses[replace_from_obj_index]
        else:
            potential = {}
            statement = self.statement

            for from_clause in itertools.chain(
                itertools.chain.from_iterable(
                    [element._from_objects for element in raw_columns]
                ),
                itertools.chain.from_iterable(
                    [
                        element._from_objects
                        for element in statement._where_criteria
                    ]
                ),
            ):

                potential[from_clause] = ()

            all_clauses = list(potential.keys())
            indexes = sql_util.find_left_clause_to_join_from(
                all_clauses, right, onclause
            )

            if len(indexes) == 1:
                left = all_clauses[indexes[0]]

        if len(indexes) > 1:
            raise exc.InvalidRequestError(
                "Can't determine which FROM clause to join "
                "from, there are multiple FROMS which can "
                "join to this entity. Please use the .select_from() "
                "method to establish an explicit left side, as well as "
                "providing an explicit ON clause if not present already to "
                "help resolve the ambiguity."
            )
        elif not indexes:
            raise exc.InvalidRequestError(
                "Don't know how to join to %r. "
                "Please use the .select_from() "
                "method to establish an explicit left side, as well as "
                "providing an explicit ON clause if not present already to "
                "help resolve the ambiguity." % (right,)
            )
        return left, replace_from_obj_index

    @util.preload_module("sqlalchemy.sql.util")
    def _join_place_explicit_left_side(self, left):
        replace_from_obj_index = None

        sql_util = util.preloaded.sql_util

        from_clauses = list(self.statement._iterate_from_elements())

        if from_clauses:
            indexes = sql_util.find_left_clause_that_matches_given(
                self.from_clauses, left
            )
        else:
            indexes = []

        if len(indexes) > 1:
            raise exc.InvalidRequestError(
                "Can't identify which entity in which to assign the "
                "left side of this join.   Please use a more specific "
                "ON clause."
            )

        # have an index, means the left side is already present in
        # an existing FROM in the self._from_obj tuple
        if indexes:
            replace_from_obj_index = indexes[0]

        # no index, means we need to add a new element to the
        # self._from_obj tuple

        return replace_from_obj_index


class _SelectFromElements(object):
    def _iterate_from_elements(self):
        # note this does not include elements
        # in _setup_joins or _legacy_setup_joins

        seen = set()
        for element in self._raw_columns:
            for fr in element._from_objects:
                if fr in seen:
                    continue
                seen.add(fr)
                yield fr
        for element in self._where_criteria:
            for fr in element._from_objects:
                if fr in seen:
                    continue
                seen.add(fr)
                yield fr
        for element in self._from_obj:
            if element in seen:
                continue
            seen.add(element)
            yield element


class _MemoizedSelectEntities(
    traversals.HasCacheKey, traversals.HasCopyInternals, visitors.Traversible
):
    __visit_name__ = "memoized_select_entities"

    _traverse_internals = [
        ("_raw_columns", InternalTraversal.dp_clauseelement_list),
        ("_setup_joins", InternalTraversal.dp_setup_join_tuple),
        ("_legacy_setup_joins", InternalTraversal.dp_setup_join_tuple),
        ("_with_options", InternalTraversal.dp_executable_options),
    ]

    _annotations = util.EMPTY_DICT

    def _clone(self, **kw):
        c = self.__class__.__new__(self.__class__)
        c.__dict__ = {k: v for k, v in self.__dict__.items()}
        c._is_clone_of = self
        return c

    @classmethod
    def _generate_for_statement(cls, select_stmt):
        if (
            select_stmt._setup_joins
            or select_stmt._legacy_setup_joins
            or select_stmt._with_options
        ):
            self = _MemoizedSelectEntities()
            self._raw_columns = select_stmt._raw_columns
            self._setup_joins = select_stmt._setup_joins
            self._legacy_setup_joins = select_stmt._legacy_setup_joins
            self._with_options = select_stmt._with_options

            select_stmt._memoized_select_entities += (self,)
            select_stmt._raw_columns = (
                select_stmt._setup_joins
            ) = (
                select_stmt._legacy_setup_joins
            ) = select_stmt._with_options = ()


class Select(
    HasPrefixes,
    HasSuffixes,
    HasHints,
    HasCompileState,
    DeprecatedSelectGenerations,
    _SelectFromElements,
    GenerativeSelect,
):
    """Represents a ``SELECT`` statement.

    The :class:`_sql.Select` object is normally constructed using the
    :func:`_sql.select` function.  See that function for details.

    .. seealso::

        :func:`_sql.select`

        :ref:`coretutorial_selecting` - in the 1.x tutorial

        :ref:`tutorial_selecting_data` - in the 2.0 tutorial

    """

    __visit_name__ = "select"

    _setup_joins = ()
    _legacy_setup_joins = ()
    _memoized_select_entities = ()

    _distinct = False
    _distinct_on = ()
    _correlate = ()
    _correlate_except = None
    _where_criteria = ()
    _having_criteria = ()
    _from_obj = ()
    _auto_correlate = True

    _compile_options = SelectState.default_select_compile_options

    _traverse_internals = (
        [
            ("_raw_columns", InternalTraversal.dp_clauseelement_list),
            (
                "_memoized_select_entities",
                InternalTraversal.dp_memoized_select_entities,
            ),
            ("_from_obj", InternalTraversal.dp_clauseelement_list),
            ("_where_criteria", InternalTraversal.dp_clauseelement_tuple),
            ("_having_criteria", InternalTraversal.dp_clauseelement_tuple),
            ("_order_by_clauses", InternalTraversal.dp_clauseelement_tuple),
            ("_group_by_clauses", InternalTraversal.dp_clauseelement_tuple),
            ("_setup_joins", InternalTraversal.dp_setup_join_tuple),
            ("_legacy_setup_joins", InternalTraversal.dp_setup_join_tuple),
            ("_correlate", InternalTraversal.dp_clauseelement_tuple),
            ("_correlate_except", InternalTraversal.dp_clauseelement_tuple),
            ("_limit_clause", InternalTraversal.dp_clauseelement),
            ("_offset_clause", InternalTraversal.dp_clauseelement),
            ("_fetch_clause", InternalTraversal.dp_clauseelement),
            ("_fetch_clause_options", InternalTraversal.dp_plain_dict),
            ("_for_update_arg", InternalTraversal.dp_clauseelement),
            ("_distinct", InternalTraversal.dp_boolean),
            ("_distinct_on", InternalTraversal.dp_clauseelement_tuple),
            ("_label_style", InternalTraversal.dp_plain_obj),
        ]
        + HasCTE._has_ctes_traverse_internals
        + HasPrefixes._has_prefixes_traverse_internals
        + HasSuffixes._has_suffixes_traverse_internals
        + HasHints._has_hints_traverse_internals
        + SupportsCloneAnnotations._clone_annotations_traverse_internals
        + Executable._executable_traverse_internals
    )

    _cache_key_traversal = _traverse_internals + [
        ("_compile_options", InternalTraversal.dp_has_cache_key)
    ]

    @classmethod
    def _create_select_from_fromclause(cls, target, entities, *arg, **kw):
        if arg or kw:
            return Select.create_legacy_select(entities, *arg, **kw)
        else:
            return Select._create_select(*entities)

    @classmethod
    @util.deprecated(
        "2.0",
        "The legacy calling style of :func:`_sql.select` is deprecated and "
        "will be removed in SQLAlchemy 2.0.  Please use the new calling "
        "style described at :func:`_sql.select`.",
    )
    def create_legacy_select(
        cls,
        columns=None,
        whereclause=None,
        from_obj=None,
        distinct=False,
        having=None,
        correlate=True,
        prefixes=None,
        suffixes=None,
        **kwargs
    ):
        """Construct a new :class:`_expression.Select` using the 1.x style API.

        This method is called implicitly when the :func:`_expression.select`
        construct is used and the first argument is a Python list or other
        plain sequence object, which is taken to refer to the columns
        collection.

        .. versionchanged:: 1.4 Added the :meth:`.Select.create_legacy_select`
           constructor which documents the calling style in use when the
           :func:`.select` construct is invoked using 1.x-style arguments.

        Similar functionality is also available via the
        :meth:`_expression.FromClause.select` method on any
        :class:`_expression.FromClause`.

        All arguments which accept :class:`_expression.ClauseElement` arguments
        also accept string arguments, which will be converted as appropriate
        into either :func:`_expression.text()` or
        :func:`_expression.literal_column()` constructs.

        .. seealso::

            :ref:`coretutorial_selecting` - Core Tutorial description of
            :func:`_expression.select`.

        :param columns:
          A list of :class:`_expression.ColumnElement` or
          :class:`_expression.FromClause`
          objects which will form the columns clause of the resulting
          statement.   For those objects that are instances of
          :class:`_expression.FromClause` (typically :class:`_schema.Table`
          or :class:`_expression.Alias`
          objects), the :attr:`_expression.FromClause.c`
          collection is extracted
          to form a collection of :class:`_expression.ColumnElement` objects.

          This parameter will also accept :class:`_expression.TextClause`
          constructs as
          given, as well as ORM-mapped classes.

          .. note::

            The :paramref:`_expression.select.columns`
            parameter is not available
            in the method form of :func:`_expression.select`, e.g.
            :meth:`_expression.FromClause.select`.

          .. seealso::

            :meth:`_expression.Select.column`

            :meth:`_expression.Select.with_only_columns`

        :param whereclause:
          A :class:`_expression.ClauseElement`
          expression which will be used to form the
          ``WHERE`` clause.   It is typically preferable to add WHERE
          criterion to an existing :class:`_expression.Select`
          using method chaining
          with :meth:`_expression.Select.where`.

          .. seealso::

            :meth:`_expression.Select.where`

        :param from_obj:
          A list of :class:`_expression.ClauseElement`
          objects which will be added to the
          ``FROM`` clause of the resulting statement.  This is equivalent
          to calling :meth:`_expression.Select.select_from`
          using method chaining on
          an existing :class:`_expression.Select` object.

          .. seealso::

            :meth:`_expression.Select.select_from`
            - full description of explicit
            FROM clause specification.

        :param bind=None:
          an :class:`_engine.Engine` or :class:`_engine.Connection` instance
          to which the
          resulting :class:`_expression.Select` object will be bound.  The
          :class:`_expression.Select`
          object will otherwise automatically bind to
          whatever :class:`~.base.Connectable` instances can be located within
          its contained :class:`_expression.ClauseElement` members.

        :param correlate=True:
          indicates that this :class:`_expression.Select`
          object should have its
          contained :class:`_expression.FromClause`
          elements "correlated" to an enclosing
          :class:`_expression.Select` object.
          It is typically preferable to specify
          correlations on an existing :class:`_expression.Select`
          construct using
          :meth:`_expression.Select.correlate`.

          .. seealso::

            :meth:`_expression.Select.correlate`
            - full description of correlation.

        :param distinct=False:
          when ``True``, applies a ``DISTINCT`` qualifier to the columns
          clause of the resulting statement.

          The boolean argument may also be a column expression or list
          of column expressions - this is a special calling form which
          is understood by the PostgreSQL dialect to render the
          ``DISTINCT ON (<columns>)`` syntax.

          ``distinct`` is also available on an existing
          :class:`_expression.Select`
          object via the :meth:`_expression.Select.distinct` method.

          .. seealso::

            :meth:`_expression.Select.distinct`

        :param group_by:
          a list of :class:`_expression.ClauseElement`
          objects which will comprise the
          ``GROUP BY`` clause of the resulting select.  This parameter
          is typically specified more naturally using the
          :meth:`_expression.Select.group_by` method on an existing
          :class:`_expression.Select`.

          .. seealso::

            :meth:`_expression.Select.group_by`

        :param having:
          a :class:`_expression.ClauseElement`
          that will comprise the ``HAVING`` clause
          of the resulting select when ``GROUP BY`` is used.  This parameter
          is typically specified more naturally using the
          :meth:`_expression.Select.having` method on an existing
          :class:`_expression.Select`.

          .. seealso::

            :meth:`_expression.Select.having`

        :param limit=None:
          a numerical value which usually renders as a ``LIMIT``
          expression in the resulting select.  Backends that don't
          support ``LIMIT`` will attempt to provide similar
          functionality.    This parameter is typically specified more
          naturally using the :meth:`_expression.Select.limit`
          method on an existing
          :class:`_expression.Select`.

          .. seealso::

            :meth:`_expression.Select.limit`

        :param offset=None:
          a numeric value which usually renders as an ``OFFSET``
          expression in the resulting select.  Backends that don't
          support ``OFFSET`` will attempt to provide similar
          functionality.  This parameter is typically specified more naturally
          using the :meth:`_expression.Select.offset` method on an existing
          :class:`_expression.Select`.

          .. seealso::

            :meth:`_expression.Select.offset`

        :param order_by:
          a scalar or list of :class:`_expression.ClauseElement`
          objects which will
          comprise the ``ORDER BY`` clause of the resulting select.
          This parameter is typically specified more naturally using the
          :meth:`_expression.Select.order_by` method on an existing
          :class:`_expression.Select`.

          .. seealso::

            :meth:`_expression.Select.order_by`

        :param use_labels=False:
          when ``True``, the statement will be generated using labels
          for each column in the columns clause, which qualify each
          column with its parent table's (or aliases) name so that name
          conflicts between columns in different tables don't occur.
          The format of the label is ``<tablename>_<column>``.  The "c"
          collection of a :class:`_expression.Subquery` created
          against this :class:`_expression.Select`
          object, as well as the :attr:`_expression.Select.selected_columns`
          collection of the :class:`_expression.Select` itself, will use these
          names for targeting column members.

          This parameter can also be specified on an existing
          :class:`_expression.Select` object using the
          :meth:`_expression.Select.set_label_style`
          method.

          .. seealso::

            :meth:`_expression.Select.set_label_style`

        """
        self = cls.__new__(cls)

        self._auto_correlate = correlate

        if distinct is not False:
            if distinct is True:
                self.distinct.non_generative(self)
            else:
                self.distinct.non_generative(self, *util.to_list(distinct))

        if from_obj is not None:
            self.select_from.non_generative(self, *util.to_list(from_obj))

        try:
            cols_present = bool(columns)
        except TypeError as err:
            util.raise_(
                exc.ArgumentError(
                    "select() construct created in legacy mode, i.e. with "
                    "keyword arguments, must provide the columns argument as "
                    "a Python list or other iterable.",
                    code="c9ae",
                ),
                from_=err,
            )

        if cols_present:
            self._raw_columns = [
                coercions.expect(
                    roles.ColumnsClauseRole, c, apply_propagate_attrs=self
                )
                for c in columns
            ]
        else:
            self._raw_columns = []

        if whereclause is not None:
            self.where.non_generative(self, whereclause)

        if having is not None:
            self.having.non_generative(self, having)

        if prefixes:
            self._setup_prefixes(prefixes)

        if suffixes:
            self._setup_suffixes(suffixes)

        GenerativeSelect.__init__(self, **kwargs)
        return self

    @classmethod
    def _create_future_select(cls, *entities):
        r"""Construct a new :class:`_expression.Select` using the 2.
        x style API.

        .. versionadded:: 1.4 - The :func:`_sql.select` function now accepts
           column arguments positionally.   The top-level :func:`_sql.select`
           function will automatically use the 1.x or 2.x style API based on
           the incoming arguments; using :func:`_future.select` from the
           ``sqlalchemy.future`` module will enforce that only the 2.x style
           constructor is used.

        Similar functionality is also available via the
        :meth:`_expression.FromClause.select` method on any
        :class:`_expression.FromClause`.

        .. seealso::

            :ref:`coretutorial_selecting` - Core Tutorial description of
            :func:`_expression.select`.

        :param \*entities:
          Entities to SELECT from.  For Core usage, this is typically a series
          of :class:`_expression.ColumnElement` and / or
          :class:`_expression.FromClause`
          objects which will form the columns clause of the resulting
          statement.   For those objects that are instances of
          :class:`_expression.FromClause` (typically :class:`_schema.Table`
          or :class:`_expression.Alias`
          objects), the :attr:`_expression.FromClause.c`
          collection is extracted
          to form a collection of :class:`_expression.ColumnElement` objects.

          This parameter will also accept :class:`_expression.TextClause`
          constructs as
          given, as well as ORM-mapped classes.

        """

        self = cls.__new__(cls)
        self._raw_columns = [
            coercions.expect(
                roles.ColumnsClauseRole, ent, apply_propagate_attrs=self
            )
            for ent in entities
        ]

        GenerativeSelect.__init__(self)

        return self

    _create_select = _create_future_select

    @classmethod
    def _create(cls, *args, **kw):
        r"""Create a :class:`.Select` using either the 1.x or 2.0 constructor
        style.

        For the legacy calling style, see :meth:`.Select.create_legacy_select`.
        If the first argument passed is a Python sequence or if keyword
        arguments are present, this style is used.

        .. versionadded:: 2.0 - the :func:`_future.select` construct is
           the same construct as the one returned by
           :func:`_expression.select`, except that the function only
           accepts the "columns clause" entities up front; the rest of the
           state of the SELECT should be built up using generative methods.

        Similar functionality is also available via the
        :meth:`_expression.FromClause.select` method on any
        :class:`_expression.FromClause`.

        .. seealso::

            :ref:`coretutorial_selecting` - Core Tutorial description of
            :func:`_expression.select`.

        :param \*entities:
          Entities to SELECT from.  For Core usage, this is typically a series
          of :class:`_expression.ColumnElement` and / or
          :class:`_expression.FromClause`
          objects which will form the columns clause of the resulting
          statement.   For those objects that are instances of
          :class:`_expression.FromClause` (typically :class:`_schema.Table`
          or :class:`_expression.Alias`
          objects), the :attr:`_expression.FromClause.c`
          collection is extracted
          to form a collection of :class:`_expression.ColumnElement` objects.

          This parameter will also accept :class:`_expression.TextClause`
          constructs as given, as well as ORM-mapped classes.

        """
        if (
            args
            and (
                isinstance(args[0], list)
                or (
                    hasattr(args[0], "__iter__")
                    and not isinstance(
                        args[0], util.string_types + (ClauseElement,)
                    )
                    and inspect(args[0], raiseerr=False) is None
                    and not hasattr(args[0], "__clause_element__")
                )
            )
        ) or kw:
            return cls.create_legacy_select(*args, **kw)
        else:
            return cls._create_future_select(*args)

    def __init__(self):
        raise NotImplementedError()

    def _scalar_type(self):
        elem = self._raw_columns[0]
        cols = list(elem._select_iterable)
        return cols[0].type

    def filter(self, *criteria):
        """A synonym for the :meth:`_future.Select.where` method."""

        return self.where(*criteria)

    def _filter_by_zero(self):
        if self._setup_joins:
            meth = SelectState.get_plugin_class(
                self
            ).determine_last_joined_entity
            _last_joined_entity = meth(self)
            if _last_joined_entity is not None:
                return _last_joined_entity

        if self._from_obj:
            return self._from_obj[0]

        return self._raw_columns[0]

    def filter_by(self, **kwargs):
        r"""apply the given filtering criterion as a WHERE clause
        to this select.

        """
        from_entity = self._filter_by_zero()

        clauses = [
            _entity_namespace_key(from_entity, key) == value
            for key, value in kwargs.items()
        ]
        return self.filter(*clauses)

    @property
    def column_descriptions(self):
        """Return a 'column descriptions' structure which may be
        :term:`plugin-specific`.

        """
        meth = SelectState.get_plugin_class(self).get_column_descriptions
        return meth(self)

    def from_statement(self, statement):
        """Apply the columns which this :class:`.Select` would select
        onto another statement.

        This operation is :term:`plugin-specific` and will raise a not
        supported exception if this :class:`_sql.Select` does not select from
        plugin-enabled entities.


        The statement is typically either a :func:`_expression.text` or
        :func:`_expression.select` construct, and should return the set of
        columns appropriate to the entities represented by this
        :class:`.Select`.

        .. seealso::

            :ref:`orm_queryguide_selecting_text` - usage examples in the
            ORM Querying Guide

        """
        meth = SelectState.get_plugin_class(self).from_statement
        return meth(self, statement)

    @_generative
    def join(self, target, onclause=None, isouter=False, full=False):
        r"""Create a SQL JOIN against this :class:`_expression.Select`
        object's criterion
        and apply generatively, returning the newly resulting
        :class:`_expression.Select`.

        E.g.::

            stmt = select(user_table).join(address_table, user_table.c.id == address_table.c.user_id)

        The above statement generates SQL similar to::

            SELECT user.id, user.name FROM user JOIN address ON user.id = address.user_id

        .. versionchanged:: 1.4 :meth:`_expression.Select.join` now creates
           a :class:`_sql.Join` object between a :class:`_sql.FromClause`
           source that is within the FROM clause of the existing SELECT,
           and a given target :class:`_sql.FromClause`, and then adds
           this :class:`_sql.Join` to the FROM clause of the newly generated
           SELECT statement.    This is completely reworked from the behavior
           in 1.3, which would instead create a subquery of the entire
           :class:`_expression.Select` and then join that subquery to the
           target.

           This is a **backwards incompatible change** as the previous behavior
           was mostly useless, producing an unnamed subquery rejected by
           most databases in any case.   The new behavior is modeled after
           that of the very successful :meth:`_orm.Query.join` method in the
           ORM, in order to support the functionality of :class:`_orm.Query`
           being available by using a :class:`_sql.Select` object with an
           :class:`_orm.Session`.

           See the notes for this change at :ref:`change_select_join`.


        :param target: target table to join towards

        :param onclause: ON clause of the join.  If omitted, an ON clause
         is generated automatically based on the :class:`_schema.ForeignKey`
         linkages between the two tables, if one can be unambiguously
         determined, otherwise an error is raised.

        :param isouter: if True, generate LEFT OUTER join.  Same as
         :meth:`_expression.Select.outerjoin`.

        :param full: if True, generate FULL OUTER join.

        .. seealso::

            :ref:`tutorial_select_join` - in the :doc:`/tutorial/index`

            :ref:`orm_queryguide_joins` - in the :ref:`queryguide_toplevel`

            :meth:`_expression.Select.join_from`

            :meth:`_expression.Select.outerjoin`

        """  # noqa: E501
        target = coercions.expect(
            roles.JoinTargetRole, target, apply_propagate_attrs=self
        )
        if onclause is not None:
            onclause = coercions.expect(roles.OnClauseRole, onclause)
        self._setup_joins += (
            (target, onclause, None, {"isouter": isouter, "full": full}),
        )

    def outerjoin_from(self, from_, target, onclause=None, full=False):
        r"""Create a SQL LEFT OUTER JOIN against this :class:`_expression.Select`
        object's criterion
        and apply generatively, returning the newly resulting
        :class:`_expression.Select`.

        Usage is the same as that of :meth:`_selectable.Select.join_from`.

        """
        return self.join_from(
            from_, target, onclause=onclause, isouter=True, full=full
        )

    @_generative
    def join_from(
        self, from_, target, onclause=None, isouter=False, full=False
    ):
        r"""Create a SQL JOIN against this :class:`_expression.Select`
        object's criterion
        and apply generatively, returning the newly resulting
        :class:`_expression.Select`.

        E.g.::

            stmt = select(user_table, address_table).join_from(
                user_table, address_table, user_table.c.id == address_table.c.user_id
            )

        The above statement generates SQL similar to::

            SELECT user.id, user.name, address.id, address.email, address.user_id
            FROM user JOIN address ON user.id = address.user_id

        .. versionadded:: 1.4

        :param from\_: the left side of the join, will be rendered in the
         FROM clause and is roughly equivalent to using the
         :meth:`.Select.select_from` method.

        :param target: target table to join towards

        :param onclause: ON clause of the join.

        :param isouter: if True, generate LEFT OUTER join.  Same as
         :meth:`_expression.Select.outerjoin`.

        :param full: if True, generate FULL OUTER join.

        .. seealso::

            :ref:`tutorial_select_join` - in the :doc:`/tutorial/index`

            :ref:`orm_queryguide_joins` - in the :ref:`queryguide_toplevel`

            :meth:`_expression.Select.join`

        """  # noqa: E501

        # note the order of parsing from vs. target is important here, as we
        # are also deriving the source of the plugin (i.e. the subject mapper
        # in an ORM query) which should favor the "from_" over the "target"

        from_ = coercions.expect(
            roles.FromClauseRole, from_, apply_propagate_attrs=self
        )
        target = coercions.expect(
            roles.JoinTargetRole, target, apply_propagate_attrs=self
        )
        if onclause is not None:
            onclause = coercions.expect(roles.OnClauseRole, onclause)

        self._setup_joins += (
            (target, onclause, from_, {"isouter": isouter, "full": full}),
        )

    def outerjoin(self, target, onclause=None, full=False):
        """Create a left outer join.

        Parameters are the same as that of :meth:`_expression.Select.join`.

        .. versionchanged:: 1.4 :meth:`_expression.Select.outerjoin` now
           creates a :class:`_sql.Join` object between a
           :class:`_sql.FromClause` source that is within the FROM clause of
           the existing SELECT, and a given target :class:`_sql.FromClause`,
           and then adds this :class:`_sql.Join` to the FROM clause of the
           newly generated SELECT statement.    This is completely reworked
           from the behavior in 1.3, which would instead create a subquery of
           the entire
           :class:`_expression.Select` and then join that subquery to the
           target.

           This is a **backwards incompatible change** as the previous behavior
           was mostly useless, producing an unnamed subquery rejected by
           most databases in any case.   The new behavior is modeled after
           that of the very successful :meth:`_orm.Query.join` method in the
           ORM, in order to support the functionality of :class:`_orm.Query`
           being available by using a :class:`_sql.Select` object with an
           :class:`_orm.Session`.

           See the notes for this change at :ref:`change_select_join`.

        .. seealso::

            :ref:`tutorial_select_join` - in the :doc:`/tutorial/index`

            :ref:`orm_queryguide_joins` - in the :ref:`queryguide_toplevel`

            :meth:`_expression.Select.join`

        """
        return self.join(target, onclause=onclause, isouter=True, full=full)

    @property
    def froms(self):
        """Return the displayed list of :class:`_expression.FromClause`
        elements.

        """
        return self._compile_state_factory(self, None)._get_display_froms()

    @property
    def inner_columns(self):
        """An iterator of all :class:`_expression.ColumnElement`
        expressions which would
        be rendered into the columns clause of the resulting SELECT statement.

        This method is legacy as of 1.4 and is superseded by the
        :attr:`_expression.Select.exported_columns` collection.

        """

        return iter(self._all_selected_columns)

    def is_derived_from(self, fromclause):
        if self in fromclause._cloned_set:
            return True

        for f in self._iterate_from_elements():
            if f.is_derived_from(fromclause):
                return True
        return False

    def _copy_internals(self, clone=_clone, **kw):
        # Select() object has been cloned and probably adapted by the
        # given clone function.  Apply the cloning function to internal
        # objects

        # 1. keep a dictionary of the froms we've cloned, and what
        # they've become.  This allows us to ensure the same cloned from
        # is used when other items such as columns are "cloned"

        all_the_froms = set(
            itertools.chain(
                _from_objects(*self._raw_columns),
                _from_objects(*self._where_criteria),
            )
        )

        # do a clone for the froms we've gathered.  what is important here
        # is if any of the things we are selecting from, like tables,
        # were converted into Join objects.   if so, these need to be
        # added to _from_obj explicitly, because otherwise they won't be
        # part of the new state, as they don't associate themselves with
        # their columns.
        new_froms = {f: clone(f, **kw) for f in all_the_froms}

        # 2. copy FROM collections, adding in joins that we've created.
        existing_from_obj = [clone(f, **kw) for f in self._from_obj]
        add_froms = (
            set(f for f in new_froms.values() if isinstance(f, Join))
            .difference(all_the_froms)
            .difference(existing_from_obj)
        )

        self._from_obj = tuple(existing_from_obj) + tuple(add_froms)

        # 3. clone everything else, making sure we use columns
        # corresponding to the froms we just made.
        def replace(obj, **kw):
            if isinstance(obj, ColumnClause) and obj.table in new_froms:
                newelem = new_froms[obj.table].corresponding_column(obj)
                return newelem

        kw["replace"] = replace

        # copy everything else.   for table-ish things like correlate,
        # correlate_except, setup_joins, these clone normally.  For
        # column-expression oriented things like raw_columns, where_criteria,
        # order by, we get this from the new froms.
        super(Select, self)._copy_internals(
            clone=clone, omit_attrs=("_from_obj",), **kw
        )

        self._reset_memoizations()

    def get_children(self, **kwargs):
        return itertools.chain(
            super(Select, self).get_children(
                omit_attrs=["_from_obj", "_correlate", "_correlate_except"]
            ),
            self._iterate_from_elements(),
        )

    @_generative
    def add_columns(self, *columns):
        """Return a new :func:`_expression.select` construct with
        the given column expressions added to its columns clause.

        E.g.::

            my_select = my_select.add_columns(table.c.new_column)

        See the documentation for
        :meth:`_expression.Select.with_only_columns`
        for guidelines on adding /replacing the columns of a
        :class:`_expression.Select` object.

        """
        self._reset_memoizations()

        self._raw_columns = self._raw_columns + [
            coercions.expect(
                roles.ColumnsClauseRole, column, apply_propagate_attrs=self
            )
            for column in columns
        ]

    def _set_entities(self, entities):
        self._raw_columns = [
            coercions.expect(
                roles.ColumnsClauseRole, ent, apply_propagate_attrs=self
            )
            for ent in util.to_list(entities)
        ]

    @util.deprecated(
        "1.4",
        "The :meth:`_expression.Select.column` method is deprecated and will "
        "be removed in a future release.  Please use "
        ":meth:`_expression.Select.add_columns`",
    )
    def column(self, column):
        """Return a new :func:`_expression.select` construct with
        the given column expression added to its columns clause.

        E.g.::

            my_select = my_select.column(table.c.new_column)

        See the documentation for
        :meth:`_expression.Select.with_only_columns`
        for guidelines on adding /replacing the columns of a
        :class:`_expression.Select` object.

        """
        return self.add_columns(column)

    @util.preload_module("sqlalchemy.sql.util")
    def reduce_columns(self, only_synonyms=True):
        """Return a new :func:`_expression.select` construct with redundantly
        named, equivalently-valued columns removed from the columns clause.

        "Redundant" here means two columns where one refers to the
        other either based on foreign key, or via a simple equality
        comparison in the WHERE clause of the statement.   The primary purpose
        of this method is to automatically construct a select statement
        with all uniquely-named columns, without the need to use
        table-qualified labels as
        :meth:`_expression.Select.set_label_style`
        does.

        When columns are omitted based on foreign key, the referred-to
        column is the one that's kept.  When columns are omitted based on
        WHERE equivalence, the first column in the columns clause is the
        one that's kept.

        :param only_synonyms: when True, limit the removal of columns
         to those which have the same name as the equivalent.   Otherwise,
         all columns that are equivalent to another are removed.

        """
        return self.with_only_columns(
            *util.preloaded.sql_util.reduce_columns(
                self._all_selected_columns,
                only_synonyms=only_synonyms,
                *(self._where_criteria + self._from_obj)
            )
        )

    @_generative
    def with_only_columns(self, *columns):
        r"""Return a new :func:`_expression.select` construct with its columns
        clause replaced with the given columns.

        This method is exactly equivalent to as if the original
        :func:`_expression.select` had been called with the given columns
        clause.   I.e. a statement::

            s = select(table1.c.a, table1.c.b)
            s = s.with_only_columns(table1.c.b)

        should be exactly equivalent to::

            s = select(table1.c.b)

        Note that this will also dynamically alter the FROM clause of the
        statement if it is not explicitly stated.  To maintain the FROM
        clause, ensure the :meth:`_sql.Select.select_from` method is
        used appropriately::

            s = select(table1.c.a, table2.c.b)
            s = s.select_from(table2.c.b).with_only_columns(table1.c.a)

        :param \*columns: column expressions to be used.

         .. versionchanged:: 1.4 the :meth:`_sql.Select.with_only_columns`
            method accepts the list of column expressions positionally;
            passing the expressions as a list is deprecated.

        """

        # memoizations should be cleared here as of
        # I95c560ffcbfa30b26644999412fb6a385125f663 , asserting this
        # is the case for now.
        self._assert_no_memoizations()

        _MemoizedSelectEntities._generate_for_statement(self)

        self._raw_columns = [
            coercions.expect(roles.ColumnsClauseRole, c)
            for c in coercions._expression_collection_was_a_list(
                "columns", "Select.with_only_columns", columns
            )
        ]

    @property
    def whereclause(self):
        """Return the completed WHERE clause for this
        :class:`_expression.Select` statement.

        This assembles the current collection of WHERE criteria
        into a single :class:`_expression.BooleanClauseList` construct.


        .. versionadded:: 1.4

        """

        return BooleanClauseList._construct_for_whereclause(
            self._where_criteria
        )

    _whereclause = whereclause

    @_generative
    def where(self, *whereclause):
        """Return a new :func:`_expression.select` construct with
        the given expression added to
        its WHERE clause, joined to the existing clause via AND, if any.

        """

        assert isinstance(self._where_criteria, tuple)

        for criterion in whereclause:
            where_criteria = coercions.expect(roles.WhereHavingRole, criterion)
            self._where_criteria += (where_criteria,)

    @_generative
    def having(self, having):
        """Return a new :func:`_expression.select` construct with
        the given expression added to
        its HAVING clause, joined to the existing clause via AND, if any.

        """
        self._having_criteria += (
            coercions.expect(roles.WhereHavingRole, having),
        )

    @_generative
    def distinct(self, *expr):
        r"""Return a new :func:`_expression.select` construct which
        will apply DISTINCT to its columns clause.

        :param \*expr: optional column expressions.  When present,
         the PostgreSQL dialect will render a ``DISTINCT ON (<expressions>>)``
         construct.

         .. deprecated:: 1.4 Using \*expr in other dialects is deprecated
            and will raise :class:`_exc.CompileError` in a future version.

        """
        if expr:
            self._distinct = True
            self._distinct_on = self._distinct_on + tuple(
                coercions.expect(roles.ByOfRole, e) for e in expr
            )
        else:
            self._distinct = True

    @_generative
    def select_from(self, *froms):
        r"""Return a new :func:`_expression.select` construct with the
        given FROM expression(s)
        merged into its list of FROM objects.

        E.g.::

            table1 = table('t1', column('a'))
            table2 = table('t2', column('b'))
            s = select(table1.c.a).\
                select_from(
                    table1.join(table2, table1.c.a==table2.c.b)
                )

        The "from" list is a unique set on the identity of each element,
        so adding an already present :class:`_schema.Table`
        or other selectable
        will have no effect.   Passing a :class:`_expression.Join` that refers
        to an already present :class:`_schema.Table`
        or other selectable will have
        the effect of concealing the presence of that selectable as
        an individual element in the rendered FROM list, instead
        rendering it into a JOIN clause.

        While the typical purpose of :meth:`_expression.Select.select_from`
        is to
        replace the default, derived FROM clause with a join, it can
        also be called with individual table elements, multiple times
        if desired, in the case that the FROM clause cannot be fully
        derived from the columns clause::

            select(func.count('*')).select_from(table1)

        """

        self._from_obj += tuple(
            coercions.expect(
                roles.FromClauseRole, fromclause, apply_propagate_attrs=self
            )
            for fromclause in froms
        )

    @_generative
    def correlate(self, *fromclauses):
        r"""Return a new :class:`_expression.Select`
        which will correlate the given FROM
        clauses to that of an enclosing :class:`_expression.Select`.

        Calling this method turns off the :class:`_expression.Select` object's
        default behavior of "auto-correlation".  Normally, FROM elements
        which appear in a :class:`_expression.Select`
        that encloses this one via
        its :term:`WHERE clause`, ORDER BY, HAVING or
        :term:`columns clause` will be omitted from this
        :class:`_expression.Select`
        object's :term:`FROM clause`.
        Setting an explicit correlation collection using the
        :meth:`_expression.Select.correlate`
        method provides a fixed list of FROM objects
        that can potentially take place in this process.

        When :meth:`_expression.Select.correlate`
        is used to apply specific FROM clauses
        for correlation, the FROM elements become candidates for
        correlation regardless of how deeply nested this
        :class:`_expression.Select`
        object is, relative to an enclosing :class:`_expression.Select`
        which refers to
        the same FROM object.  This is in contrast to the behavior of
        "auto-correlation" which only correlates to an immediate enclosing
        :class:`_expression.Select`.
        Multi-level correlation ensures that the link
        between enclosed and enclosing :class:`_expression.Select`
        is always via
        at least one WHERE/ORDER BY/HAVING/columns clause in order for
        correlation to take place.

        If ``None`` is passed, the :class:`_expression.Select`
        object will correlate
        none of its FROM entries, and all will render unconditionally
        in the local FROM clause.

        :param \*fromclauses: a list of one or more
         :class:`_expression.FromClause`
         constructs, or other compatible constructs (i.e. ORM-mapped
         classes) to become part of the correlate collection.

        .. seealso::

            :meth:`_expression.Select.correlate_except`

            :ref:`correlated_subqueries`

        """

        self._auto_correlate = False
        if fromclauses and fromclauses[0] in {None, False}:
            self._correlate = ()
        else:
            self._correlate = self._correlate + tuple(
                coercions.expect(roles.FromClauseRole, f) for f in fromclauses
            )

    @_generative
    def correlate_except(self, *fromclauses):
        r"""Return a new :class:`_expression.Select`
        which will omit the given FROM
        clauses from the auto-correlation process.

        Calling :meth:`_expression.Select.correlate_except` turns off the
        :class:`_expression.Select` object's default behavior of
        "auto-correlation" for the given FROM elements.  An element
        specified here will unconditionally appear in the FROM list, while
        all other FROM elements remain subject to normal auto-correlation
        behaviors.

        If ``None`` is passed, the :class:`_expression.Select`
        object will correlate
        all of its FROM entries.

        :param \*fromclauses: a list of one or more
         :class:`_expression.FromClause`
         constructs, or other compatible constructs (i.e. ORM-mapped
         classes) to become part of the correlate-exception collection.

        .. seealso::

            :meth:`_expression.Select.correlate`

            :ref:`correlated_subqueries`

        """

        self._auto_correlate = False
        if fromclauses and fromclauses[0] in {None, False}:
            self._correlate_except = ()
        else:
            self._correlate_except = (self._correlate_except or ()) + tuple(
                coercions.expect(roles.FromClauseRole, f) for f in fromclauses
            )

    @HasMemoized.memoized_attribute
    def selected_columns(self):
        """A :class:`_expression.ColumnCollection`
        representing the columns that
        this SELECT statement or similar construct returns in its result set,
        not including :class:`_sql.TextClause` constructs.

        This collection differs from the :attr:`_expression.FromClause.columns`
        collection of a :class:`_expression.FromClause` in that the columns
        within this collection cannot be directly nested inside another SELECT
        statement; a subquery must be applied first which provides for the
        necessary parenthesization required by SQL.

        For a :func:`_expression.select` construct, the collection here is
        exactly what would be rendered inside the "SELECT" statement, and the
        :class:`_expression.ColumnElement` objects are directly present as they
        were given, e.g.::

            col1 = column('q', Integer)
            col2 = column('p', Integer)
            stmt = select(col1, col2)

        Above, ``stmt.selected_columns`` would be a collection that contains
        the ``col1`` and ``col2`` objects directly. For a statement that is
        against a :class:`_schema.Table` or other
        :class:`_expression.FromClause`, the collection will use the
        :class:`_expression.ColumnElement` objects that are in the
        :attr:`_expression.FromClause.c` collection of the from element.

        .. note::

            The :attr:`_sql.Select.selected_columns` collection does not
            include expressions established in the columns clause using the
            :func:`_sql.text` construct; these are silently omitted from the
            collection. To use plain textual column expressions inside of a
            :class:`_sql.Select` construct, use the :func:`_sql.literal_column`
            construct.


        .. versionadded:: 1.4

        """

        # compare to SelectState._generate_columns_plus_names, which
        # generates the actual names used in the SELECT string.  that
        # method is more complex because it also renders columns that are
        # fully ambiguous, e.g. same column more than once.
        conv = SelectState._column_naming_convention(self._label_style)

        return ColumnCollection(
            [
                (conv(c), c)
                for c in self._all_selected_columns
                if not c._is_text_clause
            ]
        ).as_immutable()

    @HasMemoized.memoized_attribute
    def _all_selected_columns(self):
        meth = SelectState.get_plugin_class(self).all_selected_columns
        return list(meth(self))

    def _ensure_disambiguated_names(self):
        if self._label_style is LABEL_STYLE_NONE:
            self = self.set_label_style(LABEL_STYLE_DISAMBIGUATE_ONLY)
        return self

    def _generate_columns_plus_names(self, anon_for_dupe_key):
        """Generate column names as rendered in a SELECT statement by
        the compiler.

        This is distinct from the _column_naming_convention generator that's
        intended for population of .c collections and similar, which has
        different rules.   the collection returned here calls upon the
        _column_naming_convention as well.

        """
        cols = self._all_selected_columns

        key_naming_convention = SelectState._column_naming_convention(
            self._label_style
        )

        names = {}

        result = []
        result_append = result.append

        table_qualified = self._label_style is LABEL_STYLE_TABLENAME_PLUS_COL
        label_style_none = self._label_style is LABEL_STYLE_NONE

        for c in cols:
            repeated = False

            if not c._render_label_in_columns_clause:
                effective_name = (
                    required_label_name
                ) = fallback_label_name = None
            elif label_style_none:
                effective_name = required_label_name = None
                fallback_label_name = c._non_anon_label or c._anon_name_label
            else:
                if table_qualified:
                    required_label_name = (
                        effective_name
                    ) = fallback_label_name = c._tq_label
                else:
                    effective_name = fallback_label_name = c._non_anon_label
                    required_label_name = None

                if effective_name is None:
                    # it seems like this could be _proxy_key and we would
                    # not need _expression_label but it isn't
                    # giving us a clue when to use anon_label instead
                    expr_label = c._expression_label
                    if expr_label is None:
                        repeated = c._anon_name_label in names
                        names[c._anon_name_label] = c
                        effective_name = required_label_name = None

                        if repeated:
                            # here, "required_label_name" is sent as
                            # "None" and "fallback_label_name" is sent.
                            if table_qualified:
                                fallback_label_name = c._dedupe_anon_tq_label
                            else:
                                fallback_label_name = c._dedupe_anon_label
                        else:
                            fallback_label_name = c._anon_name_label
                    else:
                        required_label_name = (
                            effective_name
                        ) = fallback_label_name = expr_label

            if effective_name is not None:
                if effective_name in names:
                    # when looking to see if names[name] is the same column as
                    # c, use hash(), so that an annotated version of the column
                    # is seen as the same as the non-annotated
                    if hash(names[effective_name]) != hash(c):

                        # different column under the same name.  apply
                        # disambiguating label
                        if table_qualified:
                            required_label_name = (
                                fallback_label_name
                            ) = c._anon_tq_label
                        else:
                            required_label_name = (
                                fallback_label_name
                            ) = c._anon_name_label

                        if anon_for_dupe_key and required_label_name in names:
                            # here, c._anon_tq_label is definitely unique to
                            # that column identity (or annotated version), so
                            # this should always be true.
                            # this is also an infrequent codepath because
                            # you need two levels of duplication to be here
                            assert hash(names[required_label_name]) == hash(c)

                            # the column under the disambiguating label is
                            # already present.  apply the "dedupe" label to
                            # subsequent occurrences of the column so that the
                            # original stays non-ambiguous
                            if table_qualified:
                                required_label_name = (
                                    fallback_label_name
                                ) = c._dedupe_anon_tq_label
                            else:
                                required_label_name = (
                                    fallback_label_name
                                ) = c._dedupe_anon_label
                            repeated = True
                        else:
                            names[required_label_name] = c
                    elif anon_for_dupe_key:
                        # same column under the same name. apply the "dedupe"
                        # label so that the original stays non-ambiguous
                        if table_qualified:
                            required_label_name = (
                                fallback_label_name
                            ) = c._dedupe_anon_tq_label
                        else:
                            required_label_name = (
                                fallback_label_name
                            ) = c._dedupe_anon_label
                        repeated = True
                else:
                    names[effective_name] = c

            result_append(
                (
                    # string label name, if non-None, must be rendered as a
                    # label, i.e. "AS <name>"
                    required_label_name,
                    # proxy_key that is to be part of the result map for this
                    # col.  this is also the key in a fromclause.c or
                    # select.selected_columns collection
                    key_naming_convention(c),
                    # name that can be used to render an "AS <name>" when
                    # we have to render a label even though
                    # required_label_name was not given
                    fallback_label_name,
                    # the ColumnElement itself
                    c,
                    # True if this is a duplicate of a previous column
                    # in the list of columns
                    repeated,
                )
            )

        return result

    def _generate_fromclause_column_proxies(self, subquery):
        """Generate column proxies to place in the exported ``.c``
        collection of a subquery."""

        prox = [
            c._make_proxy(
                subquery,
                key=proxy_key,
                name=required_label_name,
                name_is_truncatable=True,
            )
            for (
                required_label_name,
                proxy_key,
                fallback_label_name,
                c,
                repeated,
            ) in (self._generate_columns_plus_names(False))
            if not c._is_text_clause
        ]

        subquery._columns._populate_separate_keys(prox)

    def _needs_parens_for_grouping(self):
        return self._has_row_limiting_clause or bool(
            self._order_by_clause.clauses
        )

    def self_group(self, against=None):
        """Return a 'grouping' construct as per the
        :class:`_expression.ClauseElement` specification.

        This produces an element that can be embedded in an expression. Note
        that this method is called automatically as needed when constructing
        expressions and should not require explicit use.

        """
        if (
            isinstance(against, CompoundSelect)
            and not self._needs_parens_for_grouping()
        ):
            return self
        else:
            return SelectStatementGrouping(self)

    def union(self, other, **kwargs):
        """Return a SQL ``UNION`` of this select() construct against
        the given selectable.

        """
        return CompoundSelect._create_union(self, other, **kwargs)

    def union_all(self, other, **kwargs):
        """Return a SQL ``UNION ALL`` of this select() construct against
        the given selectable.

        """
        return CompoundSelect._create_union_all(self, other, **kwargs)

    def except_(self, other, **kwargs):
        """Return a SQL ``EXCEPT`` of this select() construct against
        the given selectable.

        """
        return CompoundSelect._create_except(self, other, **kwargs)

    def except_all(self, other, **kwargs):
        """Return a SQL ``EXCEPT ALL`` of this select() construct against
        the given selectable.

        """
        return CompoundSelect._create_except_all(self, other, **kwargs)

    def intersect(self, other, **kwargs):
        """Return a SQL ``INTERSECT`` of this select() construct against
        the given selectable.

        """
        return CompoundSelect._create_intersect(self, other, **kwargs)

    def intersect_all(self, other, **kwargs):
        """Return a SQL ``INTERSECT ALL`` of this select() construct
        against the given selectable.

        """
        return CompoundSelect._create_intersect_all(self, other, **kwargs)

    @property
    @util.deprecated_20(
        ":attr:`.Executable.bind`",
        alternative="Bound metadata is being removed as of SQLAlchemy 2.0.",
        enable_warnings=False,
    )
    def bind(self):
        """Returns the :class:`_engine.Engine` or :class:`_engine.Connection`
        to which this :class:`.Executable` is bound, or None if none found.

        """
        if self._bind:
            return self._bind

        for item in self._iterate_from_elements():
            if item._is_subquery and item.element is self:
                raise exc.InvalidRequestError(
                    "select() construct refers to itself as a FROM"
                )

            e = item.bind
            if e:
                self._bind = e
                return e
            else:
                break

        for c in self._raw_columns:
            e = c.bind
            if e:
                self._bind = e
                return e

    @bind.setter
    def bind(self, bind):
        self._bind = bind


class ScalarSelect(roles.InElementRole, Generative, Grouping):
    """Represent a scalar subquery.


    A :class:`_sql.ScalarSelect` is created by invoking the
    :meth:`_sql.SelectBase.scalar_subquery` method.   The object
    then participates in other SQL expressions as a SQL column expression
    within the :class:`_sql.ColumnElement` hierarchy.

    .. seealso::

        :meth:`_sql.SelectBase.scalar_subquery`

        :ref:`tutorial_scalar_subquery` - in the 2.0 tutorial

        :ref:`scalar_selects` - in the 1.x tutorial

    """

    _from_objects = []
    _is_from_container = True
    _is_implicitly_boolean = False
    inherit_cache = True

    def __init__(self, element):
        self.element = element
        self.type = element._scalar_type()

    @property
    def columns(self):
        raise exc.InvalidRequestError(
            "Scalar Select expression has no "
            "columns; use this object directly "
            "within a column-level expression."
        )

    c = columns

    @_generative
    def where(self, crit):
        """Apply a WHERE clause to the SELECT statement referred to
        by this :class:`_expression.ScalarSelect`.

        """
        self.element = self.element.where(crit)

    def self_group(self, **kwargs):
        return self

    @_generative
    def correlate(self, *fromclauses):
        r"""Return a new :class:`_expression.ScalarSelect`
        which will correlate the given FROM
        clauses to that of an enclosing :class:`_expression.Select`.

        This method is mirrored from the :meth:`_sql.Select.correlate` method
        of the underlying :class:`_sql.Select`.  The method applies the
        :meth:_sql.Select.correlate` method, then returns a new
        :class:`_sql.ScalarSelect` against that statement.

        .. versionadded:: 1.4 Previously, the
           :meth:`_sql.ScalarSelect.correlate`
           method was only available from :class:`_sql.Select`.

        :param \*fromclauses: a list of one or more
         :class:`_expression.FromClause`
         constructs, or other compatible constructs (i.e. ORM-mapped
         classes) to become part of the correlate collection.

        .. seealso::

            :meth:`_expression.ScalarSelect.correlate_except`

            :ref:`tutorial_scalar_subquery` - in the 2.0 tutorial

            :ref:`correlated_subqueries` - in the 1.x tutorial


        """
        self.element = self.element.correlate(*fromclauses)

    @_generative
    def correlate_except(self, *fromclauses):
        r"""Return a new :class:`_expression.ScalarSelect`
        which will omit the given FROM
        clauses from the auto-correlation process.

        This method is mirrored from the
        :meth:`_sql.Select.correlate_except` method of the underlying
        :class:`_sql.Select`.  The method applies the
        :meth:_sql.Select.correlate_except` method, then returns a new
        :class:`_sql.ScalarSelect` against that statement.

        .. versionadded:: 1.4 Previously, the
           :meth:`_sql.ScalarSelect.correlate_except`
           method was only available from :class:`_sql.Select`.

        :param \*fromclauses: a list of one or more
         :class:`_expression.FromClause`
         constructs, or other compatible constructs (i.e. ORM-mapped
         classes) to become part of the correlate-exception collection.

        .. seealso::

            :meth:`_expression.ScalarSelect.correlate`

            :ref:`tutorial_scalar_subquery` - in the 2.0 tutorial

            :ref:`correlated_subqueries` - in the 1.x tutorial


        """

        self.element = self.element.correlate_except(*fromclauses)


class Exists(UnaryExpression):
    """Represent an ``EXISTS`` clause.

    See :func:`_sql.exists` for a description of usage.

    """

    _from_objects = []
    inherit_cache = True

    def __init__(self, *args, **kwargs):
        """Construct a new :class:`_expression.Exists` construct.

        The :func:`_sql.exists` can be invoked by itself to produce an
        :class:`_sql.Exists` construct, which will accept simple WHERE
        criteria::

            exists_criteria = exists().where(table1.c.col1 == table2.c.col2)

        However, for greater flexibility in constructing the SELECT, an
        existing :class:`_sql.Select` construct may be converted to an
        :class:`_sql.Exists`, most conveniently by making use of the
        :meth:`_sql.SelectBase.exists` method::

            exists_criteria = (
                select(table2.c.col2).
                where(table1.c.col1 == table2.c.col2).
                exists()
            )

        The EXISTS criteria is then used inside of an enclosing SELECT::

            stmt = select(table1.c.col1).where(exists_criteria)

        The above statement will then be of the form::

            SELECT col1 FROM table1 WHERE EXISTS
            (SELECT table2.col2 FROM table2 WHERE table2.col2 = table1.col1)

        .. seealso::

            :ref:`tutorial_exists` - in the :term:`2.0 style` tutorial.

        """  # noqa E501
        if args and isinstance(args[0], (SelectBase, ScalarSelect)):
            s = args[0]
        else:
            if not args:
                args = (literal_column("*"),)
            s = Select._create(*args, **kwargs).scalar_subquery()

        UnaryExpression.__init__(
            self,
            s,
            operator=operators.exists,
            type_=type_api.BOOLEANTYPE,
            wraps_column_expression=True,
        )

    def _regroup(self, fn):
        element = self.element._ungroup()
        element = fn(element)
        return element.self_group(against=operators.exists)

    @util.deprecated_params(
        whereclause=(
            "2.0",
            "The :paramref:`_sql.Exists.select().whereclause` parameter "
            "is deprecated and will be removed in version 2.0.  "
            "Please make use "
            "of the :meth:`.Select.where` "
            "method to add WHERE criteria to the SELECT statement.",
        ),
        kwargs=(
            "2.0",
            "The :meth:`_sql.Exists.select` method will no longer accept "
            "keyword arguments in version 2.0.  "
            "Please use generative methods from the "
            ":class:`_sql.Select` construct in order to apply additional "
            "modifications.",
        ),
    )
    def select(self, whereclause=None, **kwargs):
        r"""Return a SELECT of this :class:`_expression.Exists`.

        e.g.::

            stmt = exists(some_table.c.id).where(some_table.c.id == 5).select()

        This will produce a statement resembling::

            SELECT EXISTS (SELECT id FROM some_table WHERE some_table = :param) AS anon_1

        :param whereclause: a WHERE clause, equivalent to calling the
         :meth:`_sql.Select.where` method.

        :param **kwargs: additional keyword arguments are passed to the
         legacy constructor for :class:`_sql.Select` described at
         :meth:`_sql.Select.create_legacy_select`.

        .. seealso::

            :func:`_expression.select` - general purpose
            method which allows for arbitrary column lists.

        """  # noqa

        if whereclause is not None:
            kwargs["whereclause"] = whereclause
        return Select._create_select_from_fromclause(self, [self], **kwargs)

    def correlate(self, *fromclause):
        """Apply correlation to the subquery noted by this :class:`_sql.Exists`.

        .. seealso::

            :meth:`_sql.ScalarSelect.correlate`

        """
        e = self._clone()
        e.element = self._regroup(
            lambda element: element.correlate(*fromclause)
        )
        return e

    def correlate_except(self, *fromclause):
        """Apply correlation to the subquery noted by this :class:`_sql.Exists`.

        .. seealso::

            :meth:`_sql.ScalarSelect.correlate_except`

        """

        e = self._clone()
        e.element = self._regroup(
            lambda element: element.correlate_except(*fromclause)
        )
        return e

    def select_from(self, *froms):
        """Return a new :class:`_expression.Exists` construct,
        applying the given
        expression to the :meth:`_expression.Select.select_from`
        method of the select
        statement contained.

        .. note:: it is typically preferable to build a :class:`_sql.Select`
           statement first, including the desired WHERE clause, then use the
           :meth:`_sql.SelectBase.exists` method to produce an
           :class:`_sql.Exists` object at once.

        """
        e = self._clone()
        e.element = self._regroup(lambda element: element.select_from(*froms))
        return e

    def where(self, clause):
        """Return a new :func:`_expression.exists` construct with the
        given expression added to
        its WHERE clause, joined to the existing clause via AND, if any.


        .. note:: it is typically preferable to build a :class:`_sql.Select`
           statement first, including the desired WHERE clause, then use the
           :meth:`_sql.SelectBase.exists` method to produce an
           :class:`_sql.Exists` object at once.

        """
        e = self._clone()
        e.element = self._regroup(lambda element: element.where(clause))
        return e


class TextualSelect(SelectBase):
    """Wrap a :class:`_expression.TextClause` construct within a
    :class:`_expression.SelectBase`
    interface.

    This allows the :class:`_expression.TextClause` object to gain a
    ``.c`` collection
    and other FROM-like capabilities such as
    :meth:`_expression.FromClause.alias`,
    :meth:`_expression.SelectBase.cte`, etc.

    The :class:`_expression.TextualSelect` construct is produced via the
    :meth:`_expression.TextClause.columns`
    method - see that method for details.

    .. versionchanged:: 1.4 the :class:`_expression.TextualSelect`
       class was renamed
       from ``TextAsFrom``, to more correctly suit its role as a
       SELECT-oriented object and not a FROM clause.

    .. seealso::

        :func:`_expression.text`

        :meth:`_expression.TextClause.columns` - primary creation interface.

    """

    __visit_name__ = "textual_select"

    _label_style = LABEL_STYLE_NONE

    _traverse_internals = [
        ("element", InternalTraversal.dp_clauseelement),
        ("column_args", InternalTraversal.dp_clauseelement_list),
    ] + SupportsCloneAnnotations._clone_annotations_traverse_internals

    _is_textual = True

    is_text = True
    is_select = True

    def __init__(self, text, columns, positional=False):
        self.element = text
        # convert for ORM attributes->columns, etc
        self.column_args = [
            coercions.expect(roles.ColumnsClauseRole, c) for c in columns
        ]
        self.positional = positional

    @HasMemoized.memoized_attribute
    def selected_columns(self):
        """A :class:`_expression.ColumnCollection`
        representing the columns that
        this SELECT statement or similar construct returns in its result set,
        not including :class:`_sql.TextClause` constructs.

        This collection differs from the :attr:`_expression.FromClause.columns`
        collection of a :class:`_expression.FromClause` in that the columns
        within this collection cannot be directly nested inside another SELECT
        statement; a subquery must be applied first which provides for the
        necessary parenthesization required by SQL.

        For a :class:`_expression.TextualSelect` construct, the collection
        contains the :class:`_expression.ColumnElement` objects that were
        passed to the constructor, typically via the
        :meth:`_expression.TextClause.columns` method.


        .. versionadded:: 1.4

        """
        return ColumnCollection(
            (c.key, c) for c in self.column_args
        ).as_immutable()

    @property
    def _all_selected_columns(self):
        return self.column_args

    def _set_label_style(self, style):
        return self

    def _ensure_disambiguated_names(self):
        return self

    @property
    def _bind(self):
        return self.element._bind

    @_generative
    def bindparams(self, *binds, **bind_as_values):
        self.element = self.element.bindparams(*binds, **bind_as_values)

    def _generate_fromclause_column_proxies(self, fromclause):
        fromclause._columns._populate_separate_keys(
            c._make_proxy(fromclause) for c in self.column_args
        )

    def _scalar_type(self):
        return self.column_args[0].type


TextAsFrom = TextualSelect
"""Backwards compatibility with the previous name"""


class AnnotatedFromClause(Annotated):
    def __init__(self, element, values):
        # force FromClause to generate their internal
        # collections into __dict__
        element.c
        Annotated.__init__(self, element, values)
