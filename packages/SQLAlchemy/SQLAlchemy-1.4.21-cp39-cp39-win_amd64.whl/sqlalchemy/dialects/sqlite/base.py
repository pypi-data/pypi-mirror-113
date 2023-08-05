# sqlite/base.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

r"""
.. dialect:: sqlite
    :name: SQLite
    :full_support: 3.21, 3.28+
    :normal_support: 3.12+
    :best_effort: 3.7.16+

.. _sqlite_datetime:

Date and Time Types
-------------------

SQLite does not have built-in DATE, TIME, or DATETIME types, and pysqlite does
not provide out of the box functionality for translating values between Python
`datetime` objects and a SQLite-supported format. SQLAlchemy's own
:class:`~sqlalchemy.types.DateTime` and related types provide date formatting
and parsing functionality when SQLite is used. The implementation classes are
:class:`_sqlite.DATETIME`, :class:`_sqlite.DATE` and :class:`_sqlite.TIME`.
These types represent dates and times as ISO formatted strings, which also
nicely support ordering. There's no reliance on typical "libc" internals for
these functions so historical dates are fully supported.

Ensuring Text affinity
^^^^^^^^^^^^^^^^^^^^^^

The DDL rendered for these types is the standard ``DATE``, ``TIME``
and ``DATETIME`` indicators.    However, custom storage formats can also be
applied to these types.   When the
storage format is detected as containing no alpha characters, the DDL for
these types is rendered as ``DATE_CHAR``, ``TIME_CHAR``, and ``DATETIME_CHAR``,
so that the column continues to have textual affinity.

.. seealso::

    `Type Affinity <https://www.sqlite.org/datatype3.html#affinity>`_ -
    in the SQLite documentation

.. _sqlite_autoincrement:

SQLite Auto Incrementing Behavior
----------------------------------

Background on SQLite's autoincrement is at: https://sqlite.org/autoinc.html

Key concepts:

* SQLite has an implicit "auto increment" feature that takes place for any
  non-composite primary-key column that is specifically created using
  "INTEGER PRIMARY KEY" for the type + primary key.

* SQLite also has an explicit "AUTOINCREMENT" keyword, that is **not**
  equivalent to the implicit autoincrement feature; this keyword is not
  recommended for general use.  SQLAlchemy does not render this keyword
  unless a special SQLite-specific directive is used (see below).  However,
  it still requires that the column's type is named "INTEGER".

Using the AUTOINCREMENT Keyword
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To specifically render the AUTOINCREMENT keyword on the primary key column
when rendering DDL, add the flag ``sqlite_autoincrement=True`` to the Table
construct::

    Table('sometable', metadata,
            Column('id', Integer, primary_key=True),
            sqlite_autoincrement=True)

Allowing autoincrement behavior SQLAlchemy types other than Integer/INTEGER
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

SQLite's typing model is based on naming conventions.  Among other things, this
means that any type name which contains the substring ``"INT"`` will be
determined to be of "integer affinity".  A type named ``"BIGINT"``,
``"SPECIAL_INT"`` or even ``"XYZINTQPR"``, will be considered by SQLite to be
of "integer" affinity.  However, **the SQLite autoincrement feature, whether
implicitly or explicitly enabled, requires that the name of the column's type
is exactly the string "INTEGER"**.  Therefore, if an application uses a type
like :class:`.BigInteger` for a primary key, on SQLite this type will need to
be rendered as the name ``"INTEGER"`` when emitting the initial ``CREATE
TABLE`` statement in order for the autoincrement behavior to be available.

One approach to achieve this is to use :class:`.Integer` on SQLite
only using :meth:`.TypeEngine.with_variant`::

    table = Table(
        "my_table", metadata,
        Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    )

Another is to use a subclass of :class:`.BigInteger` that overrides its DDL
name to be ``INTEGER`` when compiled against SQLite::

    from sqlalchemy import BigInteger
    from sqlalchemy.ext.compiler import compiles

    class SLBigInteger(BigInteger):
        pass

    @compiles(SLBigInteger, 'sqlite')
    def bi_c(element, compiler, **kw):
        return "INTEGER"

    @compiles(SLBigInteger)
    def bi_c(element, compiler, **kw):
        return compiler.visit_BIGINT(element, **kw)


    table = Table(
        "my_table", metadata,
        Column("id", SLBigInteger(), primary_key=True)
    )

.. seealso::

    :meth:`.TypeEngine.with_variant`

    :ref:`sqlalchemy.ext.compiler_toplevel`

    `Datatypes In SQLite Version 3 <https://sqlite.org/datatype3.html>`_

.. _sqlite_concurrency:

Database Locking Behavior / Concurrency
---------------------------------------

SQLite is not designed for a high level of write concurrency. The database
itself, being a file, is locked completely during write operations within
transactions, meaning exactly one "connection" (in reality a file handle)
has exclusive access to the database during this period - all other
"connections" will be blocked during this time.

The Python DBAPI specification also calls for a connection model that is
always in a transaction; there is no ``connection.begin()`` method,
only ``connection.commit()`` and ``connection.rollback()``, upon which a
new transaction is to be begun immediately.  This may seem to imply
that the SQLite driver would in theory allow only a single filehandle on a
particular database file at any time; however, there are several
factors both within SQLite itself as well as within the pysqlite driver
which loosen this restriction significantly.

However, no matter what locking modes are used, SQLite will still always
lock the database file once a transaction is started and DML (e.g. INSERT,
UPDATE, DELETE) has at least been emitted, and this will block
other transactions at least at the point that they also attempt to emit DML.
By default, the length of time on this block is very short before it times out
with an error.

This behavior becomes more critical when used in conjunction with the
SQLAlchemy ORM.  SQLAlchemy's :class:`.Session` object by default runs
within a transaction, and with its autoflush model, may emit DML preceding
any SELECT statement.   This may lead to a SQLite database that locks
more quickly than is expected.   The locking mode of SQLite and the pysqlite
driver can be manipulated to some degree, however it should be noted that
achieving a high degree of write-concurrency with SQLite is a losing battle.

For more information on SQLite's lack of write concurrency by design, please
see
`Situations Where Another RDBMS May Work Better - High Concurrency
<https://www.sqlite.org/whentouse.html>`_ near the bottom of the page.

The following subsections introduce areas that are impacted by SQLite's
file-based architecture and additionally will usually require workarounds to
work when using the pysqlite driver.

.. _sqlite_isolation_level:

Transaction Isolation Level / Autocommit
----------------------------------------

SQLite supports "transaction isolation" in a non-standard way, along two
axes.  One is that of the
`PRAGMA read_uncommitted <https://www.sqlite.org/pragma.html#pragma_read_uncommitted>`_
instruction.   This setting can essentially switch SQLite between its
default mode of ``SERIALIZABLE`` isolation, and a "dirty read" isolation
mode normally referred to as ``READ UNCOMMITTED``.

SQLAlchemy ties into this PRAGMA statement using the
:paramref:`_sa.create_engine.isolation_level` parameter of
:func:`_sa.create_engine`.
Valid values for this parameter when used with SQLite are ``"SERIALIZABLE"``
and ``"READ UNCOMMITTED"`` corresponding to a value of 0 and 1, respectively.
SQLite defaults to ``SERIALIZABLE``, however its behavior is impacted by
the pysqlite driver's default behavior.

When using the pysqlite driver, the ``"AUTOCOMMIT"`` isolation level is also
available, which will alter the pysqlite connection using the ``.isolation_level``
attribute on the DBAPI connection and set it to None for the duration
of the setting.

.. versionadded:: 1.3.16 added support for SQLite AUTOCOMMIT isolation level
   when using the pysqlite / sqlite3 SQLite driver.


The other axis along which SQLite's transactional locking is impacted is
via the nature of the ``BEGIN`` statement used.   The three varieties
are "deferred", "immediate", and "exclusive", as described at
`BEGIN TRANSACTION <https://sqlite.org/lang_transaction.html>`_.   A straight
``BEGIN`` statement uses the "deferred" mode, where the database file is
not locked until the first read or write operation, and read access remains
open to other transactions until the first write operation.  But again,
it is critical to note that the pysqlite driver interferes with this behavior
by *not even emitting BEGIN* until the first write operation.

.. warning::

    SQLite's transactional scope is impacted by unresolved
    issues in the pysqlite driver, which defers BEGIN statements to a greater
    degree than is often feasible. See the section :ref:`pysqlite_serializable`
    for techniques to work around this behavior.

.. seealso::

    :ref:`dbapi_autocommit`

SAVEPOINT Support
----------------------------

SQLite supports SAVEPOINTs, which only function once a transaction is
begun.   SQLAlchemy's SAVEPOINT support is available using the
:meth:`_engine.Connection.begin_nested` method at the Core level, and
:meth:`.Session.begin_nested` at the ORM level.   However, SAVEPOINTs
won't work at all with pysqlite unless workarounds are taken.

.. warning::

    SQLite's SAVEPOINT feature is impacted by unresolved
    issues in the pysqlite driver, which defers BEGIN statements to a greater
    degree than is often feasible. See the section :ref:`pysqlite_serializable`
    for techniques to work around this behavior.

Transactional DDL
----------------------------

The SQLite database supports transactional :term:`DDL` as well.
In this case, the pysqlite driver is not only failing to start transactions,
it also is ending any existing transaction when DDL is detected, so again,
workarounds are required.

.. warning::

    SQLite's transactional DDL is impacted by unresolved issues
    in the pysqlite driver, which fails to emit BEGIN and additionally
    forces a COMMIT to cancel any transaction when DDL is encountered.
    See the section :ref:`pysqlite_serializable`
    for techniques to work around this behavior.

.. _sqlite_foreign_keys:

Foreign Key Support
-------------------

SQLite supports FOREIGN KEY syntax when emitting CREATE statements for tables,
however by default these constraints have no effect on the operation of the
table.

Constraint checking on SQLite has three prerequisites:

* At least version 3.6.19 of SQLite must be in use
* The SQLite library must be compiled *without* the SQLITE_OMIT_FOREIGN_KEY
  or SQLITE_OMIT_TRIGGER symbols enabled.
* The ``PRAGMA foreign_keys = ON`` statement must be emitted on all
  connections before use.

SQLAlchemy allows for the ``PRAGMA`` statement to be emitted automatically for
new connections through the usage of events::

    from sqlalchemy.engine import Engine
    from sqlalchemy import event

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

.. warning::

    When SQLite foreign keys are enabled, it is **not possible**
    to emit CREATE or DROP statements for tables that contain
    mutually-dependent foreign key constraints;
    to emit the DDL for these tables requires that ALTER TABLE be used to
    create or drop these constraints separately, for which SQLite has
    no support.

.. seealso::

    `SQLite Foreign Key Support <https://www.sqlite.org/foreignkeys.html>`_
    - on the SQLite web site.

    :ref:`event_toplevel` - SQLAlchemy event API.

    :ref:`use_alter` - more information on SQLAlchemy's facilities for handling
     mutually-dependent foreign key constraints.

.. _sqlite_on_conflict_ddl:

ON CONFLICT support for constraints
-----------------------------------

.. seealso:: This section describes the :term:`DDL` version of "ON CONFLICT" for
   SQLite, which occurs within a CREATE TABLE statement.  For "ON CONFLICT" as
   applied to an INSERT statement, see :ref:`sqlite_on_conflict_insert`.

SQLite supports a non-standard DDL clause known as ON CONFLICT which can be applied
to primary key, unique, check, and not null constraints.   In DDL, it is
rendered either within the "CONSTRAINT" clause or within the column definition
itself depending on the location of the target constraint.    To render this
clause within DDL, the extension parameter ``sqlite_on_conflict`` can be
specified with a string conflict resolution algorithm within the
:class:`.PrimaryKeyConstraint`, :class:`.UniqueConstraint`,
:class:`.CheckConstraint` objects.  Within the :class:`_schema.Column` object,
there
are individual parameters ``sqlite_on_conflict_not_null``,
``sqlite_on_conflict_primary_key``, ``sqlite_on_conflict_unique`` which each
correspond to the three types of relevant constraint types that can be
indicated from a :class:`_schema.Column` object.

.. seealso::

    `ON CONFLICT <https://www.sqlite.org/lang_conflict.html>`_ - in the SQLite
    documentation

.. versionadded:: 1.3


The ``sqlite_on_conflict`` parameters accept a  string argument which is just
the resolution name to be chosen, which on SQLite can be one of ROLLBACK,
ABORT, FAIL, IGNORE, and REPLACE.   For example, to add a UNIQUE constraint
that specifies the IGNORE algorithm::

    some_table = Table(
        'some_table', metadata,
        Column('id', Integer, primary_key=True),
        Column('data', Integer),
        UniqueConstraint('id', 'data', sqlite_on_conflict='IGNORE')
    )

The above renders CREATE TABLE DDL as::

    CREATE TABLE some_table (
        id INTEGER NOT NULL,
        data INTEGER,
        PRIMARY KEY (id),
        UNIQUE (id, data) ON CONFLICT IGNORE
    )


When using the :paramref:`_schema.Column.unique`
flag to add a UNIQUE constraint
to a single column, the ``sqlite_on_conflict_unique`` parameter can
be added to the :class:`_schema.Column` as well, which will be added to the
UNIQUE constraint in the DDL::

    some_table = Table(
        'some_table', metadata,
        Column('id', Integer, primary_key=True),
        Column('data', Integer, unique=True,
               sqlite_on_conflict_unique='IGNORE')
    )

rendering::

    CREATE TABLE some_table (
        id INTEGER NOT NULL,
        data INTEGER,
        PRIMARY KEY (id),
        UNIQUE (data) ON CONFLICT IGNORE
    )

To apply the FAIL algorithm for a NOT NULL constraint,
``sqlite_on_conflict_not_null`` is used::

    some_table = Table(
        'some_table', metadata,
        Column('id', Integer, primary_key=True),
        Column('data', Integer, nullable=False,
               sqlite_on_conflict_not_null='FAIL')
    )

this renders the column inline ON CONFLICT phrase::

    CREATE TABLE some_table (
        id INTEGER NOT NULL,
        data INTEGER NOT NULL ON CONFLICT FAIL,
        PRIMARY KEY (id)
    )


Similarly, for an inline primary key, use ``sqlite_on_conflict_primary_key``::

    some_table = Table(
        'some_table', metadata,
        Column('id', Integer, primary_key=True,
               sqlite_on_conflict_primary_key='FAIL')
    )

SQLAlchemy renders the PRIMARY KEY constraint separately, so the conflict
resolution algorithm is applied to the constraint itself::

    CREATE TABLE some_table (
        id INTEGER NOT NULL,
        PRIMARY KEY (id) ON CONFLICT FAIL
    )

.. _sqlite_on_conflict_insert:

INSERT...ON CONFLICT (Upsert)
-----------------------------------

.. seealso:: This section describes the :term:`DML` version of "ON CONFLICT" for
   SQLite, which occurs within an INSERT statement.  For "ON CONFLICT" as
   applied to a CREATE TABLE statement, see :ref:`sqlite_on_conflict_ddl`.

From version 3.24.0 onwards, SQLite supports "upserts" (update or insert)
of rows into a table via the ``ON CONFLICT`` clause of the ``INSERT``
statement. A candidate row will only be inserted if that row does not violate
any unique or primary key constraints. In the case of a unique constraint violation, a
secondary action can occur which can be either "DO UPDATE", indicating that
the data in the target row should be updated, or "DO NOTHING", which indicates
to silently skip this row.

Conflicts are determined using columns that are part of existing unique
constraints and indexes.  These constraints are identified by stating the
columns and conditions that comprise the indexes.

SQLAlchemy provides ``ON CONFLICT`` support via the SQLite-specific
:func:`_sqlite.insert()` function, which provides
the generative methods :meth:`_sqlite.Insert.on_conflict_do_update`
and :meth:`_sqlite.Insert.on_conflict_do_nothing`:

.. sourcecode:: pycon+sql

    >>> from sqlalchemy.dialects.sqlite import insert

    >>> insert_stmt = insert(my_table).values(
    ...     id='some_existing_id',
    ...     data='inserted value')

    >>> do_update_stmt = insert_stmt.on_conflict_do_update(
    ...     index_elements=['id'],
    ...     set_=dict(data='updated value')
    ... )

    >>> print(do_update_stmt)
    {opensql}INSERT INTO my_table (id, data) VALUES (?, ?)
    ON CONFLICT (id) DO UPDATE SET data = ?{stop}

    >>> do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
    ...     index_elements=['id']
    ... )

    >>> print(do_nothing_stmt)
    {opensql}INSERT INTO my_table (id, data) VALUES (?, ?)
    ON CONFLICT (id) DO NOTHING

.. versionadded:: 1.4

.. seealso::

    `Upsert
    <https://sqlite.org/lang_UPSERT.html>`_
    - in the SQLite documentation.


Specifying the Target
^^^^^^^^^^^^^^^^^^^^^

Both methods supply the "target" of the conflict using column inference:

* The :paramref:`_sqlite.Insert.on_conflict_do_update.index_elements` argument
  specifies a sequence containing string column names, :class:`_schema.Column`
  objects, and/or SQL expression elements, which would identify a unique index
  or unique constraint.

* When using :paramref:`_sqlite.Insert.on_conflict_do_update.index_elements`
  to infer an index, a partial index can be inferred by also specifying the
  :paramref:`_sqlite.Insert.on_conflict_do_update.index_where` parameter:

  .. sourcecode:: pycon+sql

        >>> stmt = insert(my_table).values(user_email='a@b.com', data='inserted data')

        >>> do_update_stmt = stmt.on_conflict_do_update(
        ...     index_elements=[my_table.c.user_email],
        ...     index_where=my_table.c.user_email.like('%@gmail.com'),
        ...     set_=dict(data=stmt.excluded.data)
        ...     )

        >>> print(do_update_stmt)
        {opensql}INSERT INTO my_table (data, user_email) VALUES (?, ?)
        ON CONFLICT (user_email)
        WHERE user_email LIKE '%@gmail.com'
        DO UPDATE SET data = excluded.data
        >>>

The SET Clause
^^^^^^^^^^^^^^^

``ON CONFLICT...DO UPDATE`` is used to perform an update of the already
existing row, using any combination of new values as well as values
from the proposed insertion. These values are specified using the
:paramref:`_sqlite.Insert.on_conflict_do_update.set_` parameter.  This
parameter accepts a dictionary which consists of direct values
for UPDATE:

.. sourcecode:: pycon+sql

    >>> stmt = insert(my_table).values(id='some_id', data='inserted value')

    >>> do_update_stmt = stmt.on_conflict_do_update(
    ...     index_elements=['id'],
    ...     set_=dict(data='updated value')
    ... )

    >>> print(do_update_stmt)

    {opensql}INSERT INTO my_table (id, data) VALUES (?, ?)
    ON CONFLICT (id) DO UPDATE SET data = ?

.. warning::

    The :meth:`_sqlite.Insert.on_conflict_do_update` method does **not** take
    into account Python-side default UPDATE values or generation functions,
    e.g. those specified using :paramref:`_schema.Column.onupdate`. These
    values will not be exercised for an ON CONFLICT style of UPDATE, unless
    they are manually specified in the
    :paramref:`_sqlite.Insert.on_conflict_do_update.set_` dictionary.

Updating using the Excluded INSERT Values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to refer to the proposed insertion row, the special alias
:attr:`~.sqlite.Insert.excluded` is available as an attribute on
the :class:`_sqlite.Insert` object; this object creates an "excluded." prefix
on a column, that informs the DO UPDATE to update the row with the value that
would have been inserted had the constraint not failed:

.. sourcecode:: pycon+sql

    >>> stmt = insert(my_table).values(
    ...     id='some_id',
    ...     data='inserted value',
    ...     author='jlh'
    ... )

    >>> do_update_stmt = stmt.on_conflict_do_update(
    ...     index_elements=['id'],
    ...     set_=dict(data='updated value', author=stmt.excluded.author)
    ... )

    >>> print(do_update_stmt)
    {opensql}INSERT INTO my_table (id, data, author) VALUES (?, ?, ?)
    ON CONFLICT (id) DO UPDATE SET data = ?, author = excluded.author

Additional WHERE Criteria
^^^^^^^^^^^^^^^^^^^^^^^^^

The :meth:`_sqlite.Insert.on_conflict_do_update` method also accepts
a WHERE clause using the :paramref:`_sqlite.Insert.on_conflict_do_update.where`
parameter, which will limit those rows which receive an UPDATE:

.. sourcecode:: pycon+sql

    >>> stmt = insert(my_table).values(
    ...     id='some_id',
    ...     data='inserted value',
    ...     author='jlh'
    ... )

    >>> on_update_stmt = stmt.on_conflict_do_update(
    ...     index_elements=['id'],
    ...     set_=dict(data='updated value', author=stmt.excluded.author),
    ...     where=(my_table.c.status == 2)
    ... )
    >>> print(on_update_stmt)
    {opensql}INSERT INTO my_table (id, data, author) VALUES (?, ?, ?)
    ON CONFLICT (id) DO UPDATE SET data = ?, author = excluded.author
    WHERE my_table.status = ?


Skipping Rows with DO NOTHING
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``ON CONFLICT`` may be used to skip inserting a row entirely
if any conflict with a unique constraint occurs; below this is illustrated
using the :meth:`_sqlite.Insert.on_conflict_do_nothing` method:

.. sourcecode:: pycon+sql

    >>> stmt = insert(my_table).values(id='some_id', data='inserted value')
    >>> stmt = stmt.on_conflict_do_nothing(index_elements=['id'])
    >>> print(stmt)
    {opensql}INSERT INTO my_table (id, data) VALUES (?, ?) ON CONFLICT (id) DO NOTHING


If ``DO NOTHING`` is used without specifying any columns or constraint,
it has the effect of skipping the INSERT for any unique violation which
occurs:

.. sourcecode:: pycon+sql

    >>> stmt = insert(my_table).values(id='some_id', data='inserted value')
    >>> stmt = stmt.on_conflict_do_nothing()
    >>> print(stmt)
    {opensql}INSERT INTO my_table (id, data) VALUES (?, ?) ON CONFLICT DO NOTHING

.. _sqlite_type_reflection:

Type Reflection
---------------

SQLite types are unlike those of most other database backends, in that
the string name of the type usually does not correspond to a "type" in a
one-to-one fashion.  Instead, SQLite links per-column typing behavior
to one of five so-called "type affinities" based on a string matching
pattern for the type.

SQLAlchemy's reflection process, when inspecting types, uses a simple
lookup table to link the keywords returned to provided SQLAlchemy types.
This lookup table is present within the SQLite dialect as it is for all
other dialects.  However, the SQLite dialect has a different "fallback"
routine for when a particular type name is not located in the lookup map;
it instead implements the SQLite "type affinity" scheme located at
https://www.sqlite.org/datatype3.html section 2.1.

The provided typemap will make direct associations from an exact string
name match for the following types:

:class:`_types.BIGINT`, :class:`_types.BLOB`,
:class:`_types.BOOLEAN`, :class:`_types.BOOLEAN`,
:class:`_types.CHAR`, :class:`_types.DATE`,
:class:`_types.DATETIME`, :class:`_types.FLOAT`,
:class:`_types.DECIMAL`, :class:`_types.FLOAT`,
:class:`_types.INTEGER`, :class:`_types.INTEGER`,
:class:`_types.NUMERIC`, :class:`_types.REAL`,
:class:`_types.SMALLINT`, :class:`_types.TEXT`,
:class:`_types.TIME`, :class:`_types.TIMESTAMP`,
:class:`_types.VARCHAR`, :class:`_types.NVARCHAR`,
:class:`_types.NCHAR`

When a type name does not match one of the above types, the "type affinity"
lookup is used instead:

* :class:`_types.INTEGER` is returned if the type name includes the
  string ``INT``
* :class:`_types.TEXT` is returned if the type name includes the
  string ``CHAR``, ``CLOB`` or ``TEXT``
* :class:`_types.NullType` is returned if the type name includes the
  string ``BLOB``
* :class:`_types.REAL` is returned if the type name includes the string
  ``REAL``, ``FLOA`` or ``DOUB``.
* Otherwise, the :class:`_types.NUMERIC` type is used.

.. versionadded:: 0.9.3 Support for SQLite type affinity rules when reflecting
   columns.


.. _sqlite_partial_index:

Partial Indexes
---------------

A partial index, e.g. one which uses a WHERE clause, can be specified
with the DDL system using the argument ``sqlite_where``::

    tbl = Table('testtbl', m, Column('data', Integer))
    idx = Index('test_idx1', tbl.c.data,
                sqlite_where=and_(tbl.c.data > 5, tbl.c.data < 10))

The index will be rendered at create time as::

    CREATE INDEX test_idx1 ON testtbl (data)
    WHERE data > 5 AND data < 10

.. versionadded:: 0.9.9

.. _sqlite_dotted_column_names:

Dotted Column Names
-------------------

Using table or column names that explicitly have periods in them is
**not recommended**.   While this is generally a bad idea for relational
databases in general, as the dot is a syntactically significant character,
the SQLite driver up until version **3.10.0** of SQLite has a bug which
requires that SQLAlchemy filter out these dots in result sets.

.. versionchanged:: 1.1

    The following SQLite issue has been resolved as of version 3.10.0
    of SQLite.  SQLAlchemy as of **1.1** automatically disables its internal
    workarounds based on detection of this version.

The bug, entirely outside of SQLAlchemy, can be illustrated thusly::

    import sqlite3

    assert sqlite3.sqlite_version_info < (3, 10, 0), "bug is fixed in this version"

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("create table x (a integer, b integer)")
    cursor.execute("insert into x (a, b) values (1, 1)")
    cursor.execute("insert into x (a, b) values (2, 2)")

    cursor.execute("select x.a, x.b from x")
    assert [c[0] for c in cursor.description] == ['a', 'b']

    cursor.execute('''
        select x.a, x.b from x where a=1
        union
        select x.a, x.b from x where a=2
    ''')
    assert [c[0] for c in cursor.description] == ['a', 'b'], \
        [c[0] for c in cursor.description]

The second assertion fails::

    Traceback (most recent call last):
      File "test.py", line 19, in <module>
        [c[0] for c in cursor.description]
    AssertionError: ['x.a', 'x.b']

Where above, the driver incorrectly reports the names of the columns
including the name of the table, which is entirely inconsistent vs.
when the UNION is not present.

SQLAlchemy relies upon column names being predictable in how they match
to the original statement, so the SQLAlchemy dialect has no choice but
to filter these out::


    from sqlalchemy import create_engine

    eng = create_engine("sqlite://")
    conn = eng.connect()

    conn.exec_driver_sql("create table x (a integer, b integer)")
    conn.exec_driver_sql("insert into x (a, b) values (1, 1)")
    conn.exec_driver_sql("insert into x (a, b) values (2, 2)")

    result = conn.exec_driver_sql("select x.a, x.b from x")
    assert result.keys() == ["a", "b"]

    result = conn.exec_driver_sql('''
        select x.a, x.b from x where a=1
        union
        select x.a, x.b from x where a=2
    ''')
    assert result.keys() == ["a", "b"]

Note that above, even though SQLAlchemy filters out the dots, *both
names are still addressable*::

    >>> row = result.first()
    >>> row["a"]
    1
    >>> row["x.a"]
    1
    >>> row["b"]
    1
    >>> row["x.b"]
    1

Therefore, the workaround applied by SQLAlchemy only impacts
:meth:`_engine.CursorResult.keys` and :meth:`.Row.keys()` in the public API. In
the very specific case where an application is forced to use column names that
contain dots, and the functionality of :meth:`_engine.CursorResult.keys` and
:meth:`.Row.keys()` is required to return these dotted names unmodified,
the ``sqlite_raw_colnames`` execution option may be provided, either on a
per-:class:`_engine.Connection` basis::

    result = conn.execution_options(sqlite_raw_colnames=True).exec_driver_sql('''
        select x.a, x.b from x where a=1
        union
        select x.a, x.b from x where a=2
    ''')
    assert result.keys() == ["x.a", "x.b"]

or on a per-:class:`_engine.Engine` basis::

    engine = create_engine("sqlite://", execution_options={"sqlite_raw_colnames": True})

When using the per-:class:`_engine.Engine` execution option, note that
**Core and ORM queries that use UNION may not function properly**.

SQLite-specific table options
-----------------------------

One option for CREATE TABLE is supported directly by the SQLite
dialect in conjunction with the :class:`_schema.Table` construct:

* ``WITHOUT ROWID``::

    Table("some_table", metadata, ..., sqlite_with_rowid=False)

.. seealso::

    `SQLite CREATE TABLE options
    <https://www.sqlite.org/lang_createtable.html>`_

"""  # noqa

import datetime
import numbers
import re

from .json import JSON
from .json import JSONIndexType
from .json import JSONPathType
from ... import exc
from ... import processors
from ... import schema as sa_schema
from ... import sql
from ... import types as sqltypes
from ... import util
from ...engine import default
from ...engine import reflection
from ...sql import coercions
from ...sql import ColumnElement
from ...sql import compiler
from ...sql import elements
from ...sql import roles
from ...sql import schema
from ...types import BLOB  # noqa
from ...types import BOOLEAN  # noqa
from ...types import CHAR  # noqa
from ...types import DECIMAL  # noqa
from ...types import FLOAT  # noqa
from ...types import INTEGER  # noqa
from ...types import NUMERIC  # noqa
from ...types import REAL  # noqa
from ...types import SMALLINT  # noqa
from ...types import TEXT  # noqa
from ...types import TIMESTAMP  # noqa
from ...types import VARCHAR  # noqa


class _SQliteJson(JSON):
    def result_processor(self, dialect, coltype):
        default_processor = super(_SQliteJson, self).result_processor(
            dialect, coltype
        )

        def process(value):
            try:
                return default_processor(value)
            except TypeError:
                if isinstance(value, numbers.Number):
                    return value
                else:
                    raise

        return process


class _DateTimeMixin(object):
    _reg = None
    _storage_format = None

    def __init__(self, storage_format=None, regexp=None, **kw):
        super(_DateTimeMixin, self).__init__(**kw)
        if regexp is not None:
            self._reg = re.compile(regexp)
        if storage_format is not None:
            self._storage_format = storage_format

    @property
    def format_is_text_affinity(self):
        """return True if the storage format will automatically imply
        a TEXT affinity.

        If the storage format contains no non-numeric characters,
        it will imply a NUMERIC storage format on SQLite; in this case,
        the type will generate its DDL as DATE_CHAR, DATETIME_CHAR,
        TIME_CHAR.

        .. versionadded:: 1.0.0

        """
        spec = self._storage_format % {
            "year": 0,
            "month": 0,
            "day": 0,
            "hour": 0,
            "minute": 0,
            "second": 0,
            "microsecond": 0,
        }
        return bool(re.search(r"[^0-9]", spec))

    def adapt(self, cls, **kw):
        if issubclass(cls, _DateTimeMixin):
            if self._storage_format:
                kw["storage_format"] = self._storage_format
            if self._reg:
                kw["regexp"] = self._reg
        return super(_DateTimeMixin, self).adapt(cls, **kw)

    def literal_processor(self, dialect):
        bp = self.bind_processor(dialect)

        def process(value):
            return "'%s'" % bp(value)

        return process


class DATETIME(_DateTimeMixin, sqltypes.DateTime):
    r"""Represent a Python datetime object in SQLite using a string.

    The default string storage format is::

        "%(year)04d-%(month)02d-%(day)02d %(hour)02d:%(minute)02d:%(second)02d.%(microsecond)06d"

    e.g.::

        2021-03-15 12:05:57.105542

    The storage format can be customized to some degree using the
    ``storage_format`` and ``regexp`` parameters, such as::

        import re
        from sqlalchemy.dialects.sqlite import DATETIME

        dt = DATETIME(storage_format="%(year)04d/%(month)02d/%(day)02d "
                                     "%(hour)02d:%(minute)02d:%(second)02d",
                      regexp=r"(\d+)/(\d+)/(\d+) (\d+)-(\d+)-(\d+)"
        )

    :param storage_format: format string which will be applied to the dict
     with keys year, month, day, hour, minute, second, and microsecond.

    :param regexp: regular expression which will be applied to incoming result
     rows. If the regexp contains named groups, the resulting match dict is
     applied to the Python datetime() constructor as keyword arguments.
     Otherwise, if positional groups are used, the datetime() constructor
     is called with positional arguments via
     ``*map(int, match_obj.groups(0))``.

    """  # noqa

    _storage_format = (
        "%(year)04d-%(month)02d-%(day)02d "
        "%(hour)02d:%(minute)02d:%(second)02d.%(microsecond)06d"
    )

    def __init__(self, *args, **kwargs):
        truncate_microseconds = kwargs.pop("truncate_microseconds", False)
        super(DATETIME, self).__init__(*args, **kwargs)
        if truncate_microseconds:
            assert "storage_format" not in kwargs, (
                "You can specify only "
                "one of truncate_microseconds or storage_format."
            )
            assert "regexp" not in kwargs, (
                "You can specify only one of "
                "truncate_microseconds or regexp."
            )
            self._storage_format = (
                "%(year)04d-%(month)02d-%(day)02d "
                "%(hour)02d:%(minute)02d:%(second)02d"
            )

    def bind_processor(self, dialect):
        datetime_datetime = datetime.datetime
        datetime_date = datetime.date
        format_ = self._storage_format

        def process(value):
            if value is None:
                return None
            elif isinstance(value, datetime_datetime):
                return format_ % {
                    "year": value.year,
                    "month": value.month,
                    "day": value.day,
                    "hour": value.hour,
                    "minute": value.minute,
                    "second": value.second,
                    "microsecond": value.microsecond,
                }
            elif isinstance(value, datetime_date):
                return format_ % {
                    "year": value.year,
                    "month": value.month,
                    "day": value.day,
                    "hour": 0,
                    "minute": 0,
                    "second": 0,
                    "microsecond": 0,
                }
            else:
                raise TypeError(
                    "SQLite DateTime type only accepts Python "
                    "datetime and date objects as input."
                )

        return process

    def result_processor(self, dialect, coltype):
        if self._reg:
            return processors.str_to_datetime_processor_factory(
                self._reg, datetime.datetime
            )
        else:
            return processors.str_to_datetime


class DATE(_DateTimeMixin, sqltypes.Date):
    r"""Represent a Python date object in SQLite using a string.

    The default string storage format is::

        "%(year)04d-%(month)02d-%(day)02d"

    e.g.::

        2011-03-15

    The storage format can be customized to some degree using the
    ``storage_format`` and ``regexp`` parameters, such as::

        import re
        from sqlalchemy.dialects.sqlite import DATE

        d = DATE(
                storage_format="%(month)02d/%(day)02d/%(year)04d",
                regexp=re.compile("(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)")
            )

    :param storage_format: format string which will be applied to the
     dict with keys year, month, and day.

    :param regexp: regular expression which will be applied to
     incoming result rows. If the regexp contains named groups, the
     resulting match dict is applied to the Python date() constructor
     as keyword arguments. Otherwise, if positional groups are used, the
     date() constructor is called with positional arguments via
     ``*map(int, match_obj.groups(0))``.
    """

    _storage_format = "%(year)04d-%(month)02d-%(day)02d"

    def bind_processor(self, dialect):
        datetime_date = datetime.date
        format_ = self._storage_format

        def process(value):
            if value is None:
                return None
            elif isinstance(value, datetime_date):
                return format_ % {
                    "year": value.year,
                    "month": value.month,
                    "day": value.day,
                }
            else:
                raise TypeError(
                    "SQLite Date type only accepts Python "
                    "date objects as input."
                )

        return process

    def result_processor(self, dialect, coltype):
        if self._reg:
            return processors.str_to_datetime_processor_factory(
                self._reg, datetime.date
            )
        else:
            return processors.str_to_date


class TIME(_DateTimeMixin, sqltypes.Time):
    r"""Represent a Python time object in SQLite using a string.

    The default string storage format is::

        "%(hour)02d:%(minute)02d:%(second)02d.%(microsecond)06d"

    e.g.::

        12:05:57.10558

    The storage format can be customized to some degree using the
    ``storage_format`` and ``regexp`` parameters, such as::

        import re
        from sqlalchemy.dialects.sqlite import TIME

        t = TIME(storage_format="%(hour)02d-%(minute)02d-"
                                "%(second)02d-%(microsecond)06d",
                 regexp=re.compile("(\d+)-(\d+)-(\d+)-(?:-(\d+))?")
        )

    :param storage_format: format string which will be applied to the dict
     with keys hour, minute, second, and microsecond.

    :param regexp: regular expression which will be applied to incoming result
     rows. If the regexp contains named groups, the resulting match dict is
     applied to the Python time() constructor as keyword arguments. Otherwise,
     if positional groups are used, the time() constructor is called with
     positional arguments via ``*map(int, match_obj.groups(0))``.
    """

    _storage_format = "%(hour)02d:%(minute)02d:%(second)02d.%(microsecond)06d"

    def __init__(self, *args, **kwargs):
        truncate_microseconds = kwargs.pop("truncate_microseconds", False)
        super(TIME, self).__init__(*args, **kwargs)
        if truncate_microseconds:
            assert "storage_format" not in kwargs, (
                "You can specify only "
                "one of truncate_microseconds or storage_format."
            )
            assert "regexp" not in kwargs, (
                "You can specify only one of "
                "truncate_microseconds or regexp."
            )
            self._storage_format = "%(hour)02d:%(minute)02d:%(second)02d"

    def bind_processor(self, dialect):
        datetime_time = datetime.time
        format_ = self._storage_format

        def process(value):
            if value is None:
                return None
            elif isinstance(value, datetime_time):
                return format_ % {
                    "hour": value.hour,
                    "minute": value.minute,
                    "second": value.second,
                    "microsecond": value.microsecond,
                }
            else:
                raise TypeError(
                    "SQLite Time type only accepts Python "
                    "time objects as input."
                )

        return process

    def result_processor(self, dialect, coltype):
        if self._reg:
            return processors.str_to_datetime_processor_factory(
                self._reg, datetime.time
            )
        else:
            return processors.str_to_time


colspecs = {
    sqltypes.Date: DATE,
    sqltypes.DateTime: DATETIME,
    sqltypes.JSON: _SQliteJson,
    sqltypes.JSON.JSONIndexType: JSONIndexType,
    sqltypes.JSON.JSONPathType: JSONPathType,
    sqltypes.Time: TIME,
}

ischema_names = {
    "BIGINT": sqltypes.BIGINT,
    "BLOB": sqltypes.BLOB,
    "BOOL": sqltypes.BOOLEAN,
    "BOOLEAN": sqltypes.BOOLEAN,
    "CHAR": sqltypes.CHAR,
    "DATE": sqltypes.DATE,
    "DATE_CHAR": sqltypes.DATE,
    "DATETIME": sqltypes.DATETIME,
    "DATETIME_CHAR": sqltypes.DATETIME,
    "DOUBLE": sqltypes.FLOAT,
    "DECIMAL": sqltypes.DECIMAL,
    "FLOAT": sqltypes.FLOAT,
    "INT": sqltypes.INTEGER,
    "INTEGER": sqltypes.INTEGER,
    "JSON": JSON,
    "NUMERIC": sqltypes.NUMERIC,
    "REAL": sqltypes.REAL,
    "SMALLINT": sqltypes.SMALLINT,
    "TEXT": sqltypes.TEXT,
    "TIME": sqltypes.TIME,
    "TIME_CHAR": sqltypes.TIME,
    "TIMESTAMP": sqltypes.TIMESTAMP,
    "VARCHAR": sqltypes.VARCHAR,
    "NVARCHAR": sqltypes.NVARCHAR,
    "NCHAR": sqltypes.NCHAR,
}


class SQLiteCompiler(compiler.SQLCompiler):
    extract_map = util.update_copy(
        compiler.SQLCompiler.extract_map,
        {
            "month": "%m",
            "day": "%d",
            "year": "%Y",
            "second": "%S",
            "hour": "%H",
            "doy": "%j",
            "minute": "%M",
            "epoch": "%s",
            "dow": "%w",
            "week": "%W",
        },
    )

    def visit_now_func(self, fn, **kw):
        return "CURRENT_TIMESTAMP"

    def visit_localtimestamp_func(self, func, **kw):
        return 'DATETIME(CURRENT_TIMESTAMP, "localtime")'

    def visit_true(self, expr, **kw):
        return "1"

    def visit_false(self, expr, **kw):
        return "0"

    def visit_char_length_func(self, fn, **kw):
        return "length%s" % self.function_argspec(fn)

    def visit_cast(self, cast, **kwargs):
        if self.dialect.supports_cast:
            return super(SQLiteCompiler, self).visit_cast(cast, **kwargs)
        else:
            return self.process(cast.clause, **kwargs)

    def visit_extract(self, extract, **kw):
        try:
            return "CAST(STRFTIME('%s', %s) AS INTEGER)" % (
                self.extract_map[extract.field],
                self.process(extract.expr, **kw),
            )
        except KeyError as err:
            util.raise_(
                exc.CompileError(
                    "%s is not a valid extract argument." % extract.field
                ),
                replace_context=err,
            )

    def limit_clause(self, select, **kw):
        text = ""
        if select._limit_clause is not None:
            text += "\n LIMIT " + self.process(select._limit_clause, **kw)
        if select._offset_clause is not None:
            if select._limit_clause is None:
                text += "\n LIMIT " + self.process(sql.literal(-1))
            text += " OFFSET " + self.process(select._offset_clause, **kw)
        else:
            text += " OFFSET " + self.process(sql.literal(0), **kw)
        return text

    def for_update_clause(self, select, **kw):
        # sqlite has no "FOR UPDATE" AFAICT
        return ""

    def visit_is_distinct_from_binary(self, binary, operator, **kw):
        return "%s IS NOT %s" % (
            self.process(binary.left),
            self.process(binary.right),
        )

    def visit_is_not_distinct_from_binary(self, binary, operator, **kw):
        return "%s IS %s" % (
            self.process(binary.left),
            self.process(binary.right),
        )

    def visit_json_getitem_op_binary(self, binary, operator, **kw):
        if binary.type._type_affinity is sqltypes.JSON:
            expr = "JSON_QUOTE(JSON_EXTRACT(%s, %s))"
        else:
            expr = "JSON_EXTRACT(%s, %s)"

        return expr % (
            self.process(binary.left, **kw),
            self.process(binary.right, **kw),
        )

    def visit_json_path_getitem_op_binary(self, binary, operator, **kw):
        if binary.type._type_affinity is sqltypes.JSON:
            expr = "JSON_QUOTE(JSON_EXTRACT(%s, %s))"
        else:
            expr = "JSON_EXTRACT(%s, %s)"

        return expr % (
            self.process(binary.left, **kw),
            self.process(binary.right, **kw),
        )

    def visit_empty_set_op_expr(self, type_, expand_op):
        # slightly old SQLite versions don't seem to be able to handle
        # the empty set impl
        return self.visit_empty_set_expr(type_)

    def visit_empty_set_expr(self, element_types):
        return "SELECT %s FROM (SELECT %s) WHERE 1!=1" % (
            ", ".join("1" for type_ in element_types or [INTEGER()]),
            ", ".join("1" for type_ in element_types or [INTEGER()]),
        )

    def visit_regexp_match_op_binary(self, binary, operator, **kw):
        return self._generate_generic_binary(binary, " REGEXP ", **kw)

    def visit_not_regexp_match_op_binary(self, binary, operator, **kw):
        return self._generate_generic_binary(binary, " NOT REGEXP ", **kw)

    def _on_conflict_target(self, clause, **kw):
        if clause.constraint_target is not None:
            target_text = "(%s)" % clause.constraint_target
        elif clause.inferred_target_elements is not None:
            target_text = "(%s)" % ", ".join(
                (
                    self.preparer.quote(c)
                    if isinstance(c, util.string_types)
                    else self.process(c, include_table=False, use_schema=False)
                )
                for c in clause.inferred_target_elements
            )
            if clause.inferred_target_whereclause is not None:
                target_text += " WHERE %s" % self.process(
                    clause.inferred_target_whereclause,
                    include_table=False,
                    use_schema=False,
                    literal_binds=True,
                )

        else:
            target_text = ""

        return target_text

    def visit_on_conflict_do_nothing(self, on_conflict, **kw):

        target_text = self._on_conflict_target(on_conflict, **kw)

        if target_text:
            return "ON CONFLICT %s DO NOTHING" % target_text
        else:
            return "ON CONFLICT DO NOTHING"

    def visit_on_conflict_do_update(self, on_conflict, **kw):
        clause = on_conflict

        target_text = self._on_conflict_target(on_conflict, **kw)

        action_set_ops = []

        set_parameters = dict(clause.update_values_to_set)
        # create a list of column assignment clauses as tuples

        insert_statement = self.stack[-1]["selectable"]
        cols = insert_statement.table.c
        for c in cols:
            col_key = c.key

            if col_key in set_parameters:
                value = set_parameters.pop(col_key)
            elif c in set_parameters:
                value = set_parameters.pop(c)
            else:
                continue

            if coercions._is_literal(value):
                value = elements.BindParameter(None, value, type_=c.type)

            else:
                if (
                    isinstance(value, elements.BindParameter)
                    and value.type._isnull
                ):
                    value = value._clone()
                    value.type = c.type
            value_text = self.process(value.self_group(), use_schema=False)

            key_text = self.preparer.quote(col_key)
            action_set_ops.append("%s = %s" % (key_text, value_text))

        # check for names that don't match columns
        if set_parameters:
            util.warn(
                "Additional column names not matching "
                "any column keys in table '%s': %s"
                % (
                    self.current_executable.table.name,
                    (", ".join("'%s'" % c for c in set_parameters)),
                )
            )
            for k, v in set_parameters.items():
                key_text = (
                    self.preparer.quote(k)
                    if isinstance(k, util.string_types)
                    else self.process(k, use_schema=False)
                )
                value_text = self.process(
                    coercions.expect(roles.ExpressionElementRole, v),
                    use_schema=False,
                )
                action_set_ops.append("%s = %s" % (key_text, value_text))

        action_text = ", ".join(action_set_ops)
        if clause.update_whereclause is not None:
            action_text += " WHERE %s" % self.process(
                clause.update_whereclause, include_table=True, use_schema=False
            )

        return "ON CONFLICT %s DO UPDATE SET %s" % (target_text, action_text)


class SQLiteDDLCompiler(compiler.DDLCompiler):
    def get_column_specification(self, column, **kwargs):

        coltype = self.dialect.type_compiler.process(
            column.type, type_expression=column
        )
        colspec = self.preparer.format_column(column) + " " + coltype
        default = self.get_column_default_string(column)
        if default is not None:
            if isinstance(column.server_default.arg, ColumnElement):
                default = "(" + default + ")"
            colspec += " DEFAULT " + default

        if not column.nullable:
            colspec += " NOT NULL"

            on_conflict_clause = column.dialect_options["sqlite"][
                "on_conflict_not_null"
            ]
            if on_conflict_clause is not None:
                colspec += " ON CONFLICT " + on_conflict_clause

        if column.primary_key:
            if (
                column.autoincrement is True
                and len(column.table.primary_key.columns) != 1
            ):
                raise exc.CompileError(
                    "SQLite does not support autoincrement for "
                    "composite primary keys"
                )

            if (
                column.table.dialect_options["sqlite"]["autoincrement"]
                and len(column.table.primary_key.columns) == 1
                and issubclass(column.type._type_affinity, sqltypes.Integer)
                and not column.foreign_keys
            ):
                colspec += " PRIMARY KEY"

                on_conflict_clause = column.dialect_options["sqlite"][
                    "on_conflict_primary_key"
                ]
                if on_conflict_clause is not None:
                    colspec += " ON CONFLICT " + on_conflict_clause

                colspec += " AUTOINCREMENT"

        if column.computed is not None:
            colspec += " " + self.process(column.computed)

        return colspec

    def visit_primary_key_constraint(self, constraint):
        # for columns with sqlite_autoincrement=True,
        # the PRIMARY KEY constraint can only be inline
        # with the column itself.
        if len(constraint.columns) == 1:
            c = list(constraint)[0]
            if (
                c.primary_key
                and c.table.dialect_options["sqlite"]["autoincrement"]
                and issubclass(c.type._type_affinity, sqltypes.Integer)
                and not c.foreign_keys
            ):
                return None

        text = super(SQLiteDDLCompiler, self).visit_primary_key_constraint(
            constraint
        )

        on_conflict_clause = constraint.dialect_options["sqlite"][
            "on_conflict"
        ]
        if on_conflict_clause is None and len(constraint.columns) == 1:
            on_conflict_clause = list(constraint)[0].dialect_options["sqlite"][
                "on_conflict_primary_key"
            ]

        if on_conflict_clause is not None:
            text += " ON CONFLICT " + on_conflict_clause

        return text

    def visit_unique_constraint(self, constraint):
        text = super(SQLiteDDLCompiler, self).visit_unique_constraint(
            constraint
        )

        on_conflict_clause = constraint.dialect_options["sqlite"][
            "on_conflict"
        ]
        if on_conflict_clause is None and len(constraint.columns) == 1:
            col1 = list(constraint)[0]
            if isinstance(col1, schema.SchemaItem):
                on_conflict_clause = list(constraint)[0].dialect_options[
                    "sqlite"
                ]["on_conflict_unique"]

        if on_conflict_clause is not None:
            text += " ON CONFLICT " + on_conflict_clause

        return text

    def visit_check_constraint(self, constraint):
        text = super(SQLiteDDLCompiler, self).visit_check_constraint(
            constraint
        )

        on_conflict_clause = constraint.dialect_options["sqlite"][
            "on_conflict"
        ]

        if on_conflict_clause is not None:
            text += " ON CONFLICT " + on_conflict_clause

        return text

    def visit_column_check_constraint(self, constraint):
        text = super(SQLiteDDLCompiler, self).visit_column_check_constraint(
            constraint
        )

        if constraint.dialect_options["sqlite"]["on_conflict"] is not None:
            raise exc.CompileError(
                "SQLite does not support on conflict clause for "
                "column check constraint"
            )

        return text

    def visit_foreign_key_constraint(self, constraint):

        local_table = constraint.elements[0].parent.table
        remote_table = constraint.elements[0].column.table

        if local_table.schema != remote_table.schema:
            return None
        else:
            return super(SQLiteDDLCompiler, self).visit_foreign_key_constraint(
                constraint
            )

    def define_constraint_remote_table(self, constraint, table, preparer):
        """Format the remote table clause of a CREATE CONSTRAINT clause."""

        return preparer.format_table(table, use_schema=False)

    def visit_create_index(
        self, create, include_schema=False, include_table_schema=True
    ):
        index = create.element
        self._verify_index_table(index)
        preparer = self.preparer
        text = "CREATE "
        if index.unique:
            text += "UNIQUE "

        text += "INDEX "

        if create.if_not_exists:
            text += "IF NOT EXISTS "

        text += "%s ON %s (%s)" % (
            self._prepared_index_name(index, include_schema=True),
            preparer.format_table(index.table, use_schema=False),
            ", ".join(
                self.sql_compiler.process(
                    expr, include_table=False, literal_binds=True
                )
                for expr in index.expressions
            ),
        )

        whereclause = index.dialect_options["sqlite"]["where"]
        if whereclause is not None:
            where_compiled = self.sql_compiler.process(
                whereclause, include_table=False, literal_binds=True
            )
            text += " WHERE " + where_compiled

        return text

    def post_create_table(self, table):
        if table.dialect_options["sqlite"]["with_rowid"] is False:
            return "\n WITHOUT ROWID"
        return ""


class SQLiteTypeCompiler(compiler.GenericTypeCompiler):
    def visit_large_binary(self, type_, **kw):
        return self.visit_BLOB(type_)

    def visit_DATETIME(self, type_, **kw):
        if (
            not isinstance(type_, _DateTimeMixin)
            or type_.format_is_text_affinity
        ):
            return super(SQLiteTypeCompiler, self).visit_DATETIME(type_)
        else:
            return "DATETIME_CHAR"

    def visit_DATE(self, type_, **kw):
        if (
            not isinstance(type_, _DateTimeMixin)
            or type_.format_is_text_affinity
        ):
            return super(SQLiteTypeCompiler, self).visit_DATE(type_)
        else:
            return "DATE_CHAR"

    def visit_TIME(self, type_, **kw):
        if (
            not isinstance(type_, _DateTimeMixin)
            or type_.format_is_text_affinity
        ):
            return super(SQLiteTypeCompiler, self).visit_TIME(type_)
        else:
            return "TIME_CHAR"

    def visit_JSON(self, type_, **kw):
        # note this name provides NUMERIC affinity, not TEXT.
        # should not be an issue unless the JSON value consists of a single
        # numeric value.   JSONTEXT can be used if this case is required.
        return "JSON"


class SQLiteIdentifierPreparer(compiler.IdentifierPreparer):
    reserved_words = set(
        [
            "add",
            "after",
            "all",
            "alter",
            "analyze",
            "and",
            "as",
            "asc",
            "attach",
            "autoincrement",
            "before",
            "begin",
            "between",
            "by",
            "cascade",
            "case",
            "cast",
            "check",
            "collate",
            "column",
            "commit",
            "conflict",
            "constraint",
            "create",
            "cross",
            "current_date",
            "current_time",
            "current_timestamp",
            "database",
            "default",
            "deferrable",
            "deferred",
            "delete",
            "desc",
            "detach",
            "distinct",
            "drop",
            "each",
            "else",
            "end",
            "escape",
            "except",
            "exclusive",
            "exists",
            "explain",
            "false",
            "fail",
            "for",
            "foreign",
            "from",
            "full",
            "glob",
            "group",
            "having",
            "if",
            "ignore",
            "immediate",
            "in",
            "index",
            "indexed",
            "initially",
            "inner",
            "insert",
            "instead",
            "intersect",
            "into",
            "is",
            "isnull",
            "join",
            "key",
            "left",
            "like",
            "limit",
            "match",
            "natural",
            "not",
            "notnull",
            "null",
            "of",
            "offset",
            "on",
            "or",
            "order",
            "outer",
            "plan",
            "pragma",
            "primary",
            "query",
            "raise",
            "references",
            "reindex",
            "rename",
            "replace",
            "restrict",
            "right",
            "rollback",
            "row",
            "select",
            "set",
            "table",
            "temp",
            "temporary",
            "then",
            "to",
            "transaction",
            "trigger",
            "true",
            "union",
            "unique",
            "update",
            "using",
            "vacuum",
            "values",
            "view",
            "virtual",
            "when",
            "where",
        ]
    )


class SQLiteExecutionContext(default.DefaultExecutionContext):
    @util.memoized_property
    def _preserve_raw_colnames(self):
        return (
            not self.dialect._broken_dotted_colnames
            or self.execution_options.get("sqlite_raw_colnames", False)
        )

    def _translate_colname(self, colname):
        # TODO: detect SQLite version 3.10.0 or greater;
        # see [ticket:3633]

        # adjust for dotted column names.  SQLite
        # in the case of UNION may store col names as
        # "tablename.colname", or if using an attached database,
        # "database.tablename.colname", in cursor.description
        if not self._preserve_raw_colnames and "." in colname:
            return colname.split(".")[-1], colname
        else:
            return colname, None


class SQLiteDialect(default.DefaultDialect):
    name = "sqlite"
    supports_alter = False
    supports_unicode_statements = True
    supports_unicode_binds = True

    # SQlite supports "DEFAULT VALUES" but *does not* support
    # "VALUES (DEFAULT)"
    supports_default_values = True
    supports_default_metavalue = False

    supports_empty_insert = False
    supports_cast = True
    supports_multivalues_insert = True
    tuple_in_values = True
    supports_statement_cache = True

    default_paramstyle = "qmark"
    execution_ctx_cls = SQLiteExecutionContext
    statement_compiler = SQLiteCompiler
    ddl_compiler = SQLiteDDLCompiler
    type_compiler = SQLiteTypeCompiler
    preparer = SQLiteIdentifierPreparer
    ischema_names = ischema_names
    colspecs = colspecs
    isolation_level = None

    construct_arguments = [
        (
            sa_schema.Table,
            {
                "autoincrement": False,
                "with_rowid": True,
            },
        ),
        (sa_schema.Index, {"where": None}),
        (
            sa_schema.Column,
            {
                "on_conflict_primary_key": None,
                "on_conflict_not_null": None,
                "on_conflict_unique": None,
            },
        ),
        (sa_schema.Constraint, {"on_conflict": None}),
    ]

    _broken_fk_pragma_quotes = False
    _broken_dotted_colnames = False

    @util.deprecated_params(
        _json_serializer=(
            "1.3.7",
            "The _json_serializer argument to the SQLite dialect has "
            "been renamed to the correct name of json_serializer.  The old "
            "argument name will be removed in a future release.",
        ),
        _json_deserializer=(
            "1.3.7",
            "The _json_deserializer argument to the SQLite dialect has "
            "been renamed to the correct name of json_deserializer.  The old "
            "argument name will be removed in a future release.",
        ),
    )
    def __init__(
        self,
        isolation_level=None,
        native_datetime=False,
        json_serializer=None,
        json_deserializer=None,
        _json_serializer=None,
        _json_deserializer=None,
        **kwargs
    ):
        default.DefaultDialect.__init__(self, **kwargs)
        self.isolation_level = isolation_level

        if _json_serializer:
            json_serializer = _json_serializer
        if _json_deserializer:
            json_deserializer = _json_deserializer
        self._json_serializer = json_serializer
        self._json_deserializer = json_deserializer

        # this flag used by pysqlite dialect, and perhaps others in the
        # future, to indicate the driver is handling date/timestamp
        # conversions (and perhaps datetime/time as well on some hypothetical
        # driver ?)
        self.native_datetime = native_datetime

        if self.dbapi is not None:
            if self.dbapi.sqlite_version_info < (3, 7, 16):
                util.warn(
                    "SQLite version %s is older than 3.7.16, and will not "
                    "support right nested joins, as are sometimes used in "
                    "more complex ORM scenarios.  SQLAlchemy 1.4 and above "
                    "no longer tries to rewrite these joins."
                    % (self.dbapi.sqlite_version_info,)
                )

            self._broken_dotted_colnames = self.dbapi.sqlite_version_info < (
                3,
                10,
                0,
            )
            self.supports_default_values = self.dbapi.sqlite_version_info >= (
                3,
                3,
                8,
            )
            self.supports_cast = self.dbapi.sqlite_version_info >= (3, 2, 3)
            self.supports_multivalues_insert = (
                # https://www.sqlite.org/releaselog/3_7_11.html
                self.dbapi.sqlite_version_info
                >= (3, 7, 11)
            )
            # see https://www.sqlalchemy.org/trac/ticket/2568
            # as well as https://www.sqlite.org/src/info/600482d161
            self._broken_fk_pragma_quotes = self.dbapi.sqlite_version_info < (
                3,
                6,
                14,
            )

    _isolation_lookup = {"READ UNCOMMITTED": 1, "SERIALIZABLE": 0}

    def set_isolation_level(self, connection, level):
        try:
            isolation_level = self._isolation_lookup[level.replace("_", " ")]
        except KeyError as err:
            util.raise_(
                exc.ArgumentError(
                    "Invalid value '%s' for isolation_level. "
                    "Valid isolation levels for %s are %s"
                    % (level, self.name, ", ".join(self._isolation_lookup))
                ),
                replace_context=err,
            )
        cursor = connection.cursor()
        cursor.execute("PRAGMA read_uncommitted = %d" % isolation_level)
        cursor.close()

    def get_isolation_level(self, connection):
        cursor = connection.cursor()
        cursor.execute("PRAGMA read_uncommitted")
        res = cursor.fetchone()
        if res:
            value = res[0]
        else:
            # https://www.sqlite.org/changes.html#version_3_3_3
            # "Optional READ UNCOMMITTED isolation (instead of the
            # default isolation level of SERIALIZABLE) and
            # table level locking when database connections
            # share a common cache.""
            # pre-SQLite 3.3.0 default to 0
            value = 0
        cursor.close()
        if value == 0:
            return "SERIALIZABLE"
        elif value == 1:
            return "READ UNCOMMITTED"
        else:
            assert False, "Unknown isolation level %s" % value

    def on_connect(self):
        if self.isolation_level is not None:

            def connect(conn):
                self.set_isolation_level(conn, self.isolation_level)

            return connect
        else:
            return None

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        s = "PRAGMA database_list"
        dl = connection.exec_driver_sql(s)

        return [db[1] for db in dl if db[1] != "temp"]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        if schema is not None:
            qschema = self.identifier_preparer.quote_identifier(schema)
            master = "%s.sqlite_master" % qschema
        else:
            master = "sqlite_master"
        s = ("SELECT name FROM %s " "WHERE type='table' ORDER BY name") % (
            master,
        )
        rs = connection.exec_driver_sql(s)
        return [row[0] for row in rs]

    @reflection.cache
    def get_temp_table_names(self, connection, **kw):
        s = (
            "SELECT name FROM sqlite_temp_master "
            "WHERE type='table' ORDER BY name "
        )
        rs = connection.exec_driver_sql(s)

        return [row[0] for row in rs]

    @reflection.cache
    def get_temp_view_names(self, connection, **kw):
        s = (
            "SELECT name FROM sqlite_temp_master "
            "WHERE type='view' ORDER BY name "
        )
        rs = connection.exec_driver_sql(s)

        return [row[0] for row in rs]

    def has_table(self, connection, table_name, schema=None):
        self._ensure_has_table_connection(connection)

        info = self._get_table_pragma(
            connection, "table_info", table_name, schema=schema
        )
        return bool(info)

    def _get_default_schema_name(self, connection):
        return "main"

    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        if schema is not None:
            qschema = self.identifier_preparer.quote_identifier(schema)
            master = "%s.sqlite_master" % qschema
        else:
            master = "sqlite_master"
        s = ("SELECT name FROM %s " "WHERE type='view' ORDER BY name") % (
            master,
        )
        rs = connection.exec_driver_sql(s)

        return [row[0] for row in rs]

    @reflection.cache
    def get_view_definition(self, connection, view_name, schema=None, **kw):
        if schema is not None:
            qschema = self.identifier_preparer.quote_identifier(schema)
            master = "%s.sqlite_master" % qschema
            s = ("SELECT sql FROM %s WHERE name = ? AND type='view'") % (
                master,
            )
            rs = connection.exec_driver_sql(s, (view_name,))
        else:
            try:
                s = (
                    "SELECT sql FROM "
                    " (SELECT * FROM sqlite_master UNION ALL "
                    "  SELECT * FROM sqlite_temp_master) "
                    "WHERE name = ? "
                    "AND type='view'"
                )
                rs = connection.exec_driver_sql(s, (view_name,))
            except exc.DBAPIError:
                s = (
                    "SELECT sql FROM sqlite_master WHERE name = ? "
                    "AND type='view'"
                )
                rs = connection.exec_driver_sql(s, (view_name,))

        result = rs.fetchall()
        if result:
            return result[0].sql

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        pragma = "table_info"
        # computed columns are threaded as hidden, they require table_xinfo
        if self.server_version_info >= (3, 31):
            pragma = "table_xinfo"
        info = self._get_table_pragma(
            connection, pragma, table_name, schema=schema
        )
        columns = []
        tablesql = None
        for row in info:
            name = row[1]
            type_ = row[2].upper()
            nullable = not row[3]
            default = row[4]
            primary_key = row[5]
            hidden = row[6] if pragma == "table_xinfo" else 0

            # hidden has value 0 for normal columns, 1 for hidden columns,
            # 2 for computed virtual columns and 3 for computed stored columns
            # https://www.sqlite.org/src/info/069351b85f9a706f60d3e98fbc8aaf40c374356b967c0464aede30ead3d9d18b
            if hidden == 1:
                continue

            generated = bool(hidden)
            persisted = hidden == 3

            if tablesql is None and generated:
                tablesql = self._get_table_sql(
                    connection, table_name, schema, **kw
                )

            columns.append(
                self._get_column_info(
                    name,
                    type_,
                    nullable,
                    default,
                    primary_key,
                    generated,
                    persisted,
                    tablesql,
                )
            )
        return columns

    def _get_column_info(
        self,
        name,
        type_,
        nullable,
        default,
        primary_key,
        generated,
        persisted,
        tablesql,
    ):

        if generated:
            # the type of a column "cc INTEGER GENERATED ALWAYS AS (1 + 42)"
            # somehow is "INTEGER GENERATED ALWAYS"
            type_ = re.sub("generated", "", type_, flags=re.IGNORECASE)
            type_ = re.sub("always", "", type_, flags=re.IGNORECASE).strip()

        coltype = self._resolve_type_affinity(type_)

        if default is not None:
            default = util.text_type(default)

        colspec = {
            "name": name,
            "type": coltype,
            "nullable": nullable,
            "default": default,
            "autoincrement": "auto",
            "primary_key": primary_key,
        }
        if generated:
            sqltext = ""
            if tablesql:
                pattern = r"[^,]*\s+AS\s+\(([^,]*)\)\s*(?:virtual|stored)?"
                match = re.search(
                    re.escape(name) + pattern, tablesql, re.IGNORECASE
                )
                if match:
                    sqltext = match.group(1)
            colspec["computed"] = {"sqltext": sqltext, "persisted": persisted}
        return colspec

    def _resolve_type_affinity(self, type_):
        """Return a data type from a reflected column, using affinity rules.

        SQLite's goal for universal compatibility introduces some complexity
        during reflection, as a column's defined type might not actually be a
        type that SQLite understands - or indeed, my not be defined *at all*.
        Internally, SQLite handles this with a 'data type affinity' for each
        column definition, mapping to one of 'TEXT', 'NUMERIC', 'INTEGER',
        'REAL', or 'NONE' (raw bits). The algorithm that determines this is
        listed in https://www.sqlite.org/datatype3.html section 2.1.

        This method allows SQLAlchemy to support that algorithm, while still
        providing access to smarter reflection utilities by recognizing
        column definitions that SQLite only supports through affinity (like
        DATE and DOUBLE).

        """
        match = re.match(r"([\w ]+)(\(.*?\))?", type_)
        if match:
            coltype = match.group(1)
            args = match.group(2)
        else:
            coltype = ""
            args = ""

        if coltype in self.ischema_names:
            coltype = self.ischema_names[coltype]
        elif "INT" in coltype:
            coltype = sqltypes.INTEGER
        elif "CHAR" in coltype or "CLOB" in coltype or "TEXT" in coltype:
            coltype = sqltypes.TEXT
        elif "BLOB" in coltype or not coltype:
            coltype = sqltypes.NullType
        elif "REAL" in coltype or "FLOA" in coltype or "DOUB" in coltype:
            coltype = sqltypes.REAL
        else:
            coltype = sqltypes.NUMERIC

        if args is not None:
            args = re.findall(r"(\d+)", args)
            try:
                coltype = coltype(*[int(a) for a in args])
            except TypeError:
                util.warn(
                    "Could not instantiate type %s with "
                    "reflected arguments %s; using no arguments."
                    % (coltype, args)
                )
                coltype = coltype()
        else:
            coltype = coltype()

        return coltype

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        constraint_name = None
        table_data = self._get_table_sql(connection, table_name, schema=schema)
        if table_data:
            PK_PATTERN = r"CONSTRAINT (\w+) PRIMARY KEY"
            result = re.search(PK_PATTERN, table_data, re.I)
            constraint_name = result.group(1) if result else None

        cols = self.get_columns(connection, table_name, schema, **kw)
        cols.sort(key=lambda col: col.get("primary_key"))
        pkeys = []
        for col in cols:
            if col["primary_key"]:
                pkeys.append(col["name"])

        return {"constrained_columns": pkeys, "name": constraint_name}

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        # sqlite makes this *extremely difficult*.
        # First, use the pragma to get the actual FKs.
        pragma_fks = self._get_table_pragma(
            connection, "foreign_key_list", table_name, schema=schema
        )

        fks = {}

        for row in pragma_fks:
            (numerical_id, rtbl, lcol, rcol) = (row[0], row[2], row[3], row[4])

            if not rcol:
                # no referred column, which means it was not named in the
                # original DDL.  The referred columns of the foreign key
                # constraint are therefore the primary key of the referred
                # table.
                referred_pk = self.get_pk_constraint(
                    connection, rtbl, schema=schema, **kw
                )
                # note that if table doesn't exist, we still get back a record,
                # just it has no columns in it
                referred_columns = referred_pk["constrained_columns"]
            else:
                # note we use this list only if this is the first column
                # in the constraint.  for subsequent columns we ignore the
                # list and append "rcol" if present.
                referred_columns = []

            if self._broken_fk_pragma_quotes:
                rtbl = re.sub(r"^[\"\[`\']|[\"\]`\']$", "", rtbl)

            if numerical_id in fks:
                fk = fks[numerical_id]
            else:
                fk = fks[numerical_id] = {
                    "name": None,
                    "constrained_columns": [],
                    "referred_schema": schema,
                    "referred_table": rtbl,
                    "referred_columns": referred_columns,
                    "options": {},
                }
                fks[numerical_id] = fk

            fk["constrained_columns"].append(lcol)

            if rcol:
                fk["referred_columns"].append(rcol)

        def fk_sig(constrained_columns, referred_table, referred_columns):
            return (
                tuple(constrained_columns)
                + (referred_table,)
                + tuple(referred_columns)
            )

        # then, parse the actual SQL and attempt to find DDL that matches
        # the names as well.   SQLite saves the DDL in whatever format
        # it was typed in as, so need to be liberal here.

        keys_by_signature = dict(
            (
                fk_sig(
                    fk["constrained_columns"],
                    fk["referred_table"],
                    fk["referred_columns"],
                ),
                fk,
            )
            for fk in fks.values()
        )

        table_data = self._get_table_sql(connection, table_name, schema=schema)
        if table_data is None:
            # system tables, etc.
            return []

        def parse_fks():
            FK_PATTERN = (
                r"(?:CONSTRAINT (\w+) +)?"
                r"FOREIGN KEY *\( *(.+?) *\) +"
                r'REFERENCES +(?:(?:"(.+?)")|([a-z0-9_]+)) *\((.+?)\) *'
                r"((?:ON (?:DELETE|UPDATE) "
                r"(?:SET NULL|SET DEFAULT|CASCADE|RESTRICT|NO ACTION) *)*)"
            )
            for match in re.finditer(FK_PATTERN, table_data, re.I):
                (
                    constraint_name,
                    constrained_columns,
                    referred_quoted_name,
                    referred_name,
                    referred_columns,
                    onupdatedelete,
                ) = match.group(1, 2, 3, 4, 5, 6)
                constrained_columns = list(
                    self._find_cols_in_sig(constrained_columns)
                )
                if not referred_columns:
                    referred_columns = constrained_columns
                else:
                    referred_columns = list(
                        self._find_cols_in_sig(referred_columns)
                    )
                referred_name = referred_quoted_name or referred_name
                options = {}

                for token in re.split(r" *\bON\b *", onupdatedelete.upper()):
                    if token.startswith("DELETE"):
                        ondelete = token[6:].strip()
                        if ondelete and ondelete != "NO ACTION":
                            options["ondelete"] = ondelete
                    elif token.startswith("UPDATE"):
                        onupdate = token[6:].strip()
                        if onupdate and onupdate != "NO ACTION":
                            options["onupdate"] = onupdate
                yield (
                    constraint_name,
                    constrained_columns,
                    referred_name,
                    referred_columns,
                    options,
                )

        fkeys = []

        for (
            constraint_name,
            constrained_columns,
            referred_name,
            referred_columns,
            options,
        ) in parse_fks():
            sig = fk_sig(constrained_columns, referred_name, referred_columns)
            if sig not in keys_by_signature:
                util.warn(
                    "WARNING: SQL-parsed foreign key constraint "
                    "'%s' could not be located in PRAGMA "
                    "foreign_keys for table %s" % (sig, table_name)
                )
                continue
            key = keys_by_signature.pop(sig)
            key["name"] = constraint_name
            key["options"] = options
            fkeys.append(key)
        # assume the remainders are the unnamed, inline constraints, just
        # use them as is as it's extremely difficult to parse inline
        # constraints
        fkeys.extend(keys_by_signature.values())
        return fkeys

    def _find_cols_in_sig(self, sig):
        for match in re.finditer(r'(?:"(.+?)")|([a-z0-9_]+)', sig, re.I):
            yield match.group(1) or match.group(2)

    @reflection.cache
    def get_unique_constraints(
        self, connection, table_name, schema=None, **kw
    ):

        auto_index_by_sig = {}
        for idx in self.get_indexes(
            connection,
            table_name,
            schema=schema,
            include_auto_indexes=True,
            **kw
        ):
            if not idx["name"].startswith("sqlite_autoindex"):
                continue
            sig = tuple(idx["column_names"])
            auto_index_by_sig[sig] = idx

        table_data = self._get_table_sql(
            connection, table_name, schema=schema, **kw
        )
        if not table_data:
            return []

        unique_constraints = []

        def parse_uqs():
            UNIQUE_PATTERN = r'(?:CONSTRAINT "?(.+?)"? +)?UNIQUE *\((.+?)\)'
            INLINE_UNIQUE_PATTERN = (
                r'(?:(".+?")|([a-z0-9]+)) ' r"+[a-z0-9_ ]+? +UNIQUE"
            )

            for match in re.finditer(UNIQUE_PATTERN, table_data, re.I):
                name, cols = match.group(1, 2)
                yield name, list(self._find_cols_in_sig(cols))

            # we need to match inlines as well, as we seek to differentiate
            # a UNIQUE constraint from a UNIQUE INDEX, even though these
            # are kind of the same thing :)
            for match in re.finditer(INLINE_UNIQUE_PATTERN, table_data, re.I):
                cols = list(
                    self._find_cols_in_sig(match.group(1) or match.group(2))
                )
                yield None, cols

        for name, cols in parse_uqs():
            sig = tuple(cols)
            if sig in auto_index_by_sig:
                auto_index_by_sig.pop(sig)
                parsed_constraint = {"name": name, "column_names": cols}
                unique_constraints.append(parsed_constraint)
        # NOTE: auto_index_by_sig might not be empty here,
        # the PRIMARY KEY may have an entry.
        return unique_constraints

    @reflection.cache
    def get_check_constraints(self, connection, table_name, schema=None, **kw):
        table_data = self._get_table_sql(
            connection, table_name, schema=schema, **kw
        )
        if not table_data:
            return []

        CHECK_PATTERN = r"(?:CONSTRAINT (\w+) +)?" r"CHECK *\( *(.+) *\),? *"
        check_constraints = []
        # NOTE: we aren't using re.S here because we actually are
        # taking advantage of each CHECK constraint being all on one
        # line in the table definition in order to delineate.  This
        # necessarily makes assumptions as to how the CREATE TABLE
        # was emitted.
        for match in re.finditer(CHECK_PATTERN, table_data, re.I):
            check_constraints.append(
                {"sqltext": match.group(2), "name": match.group(1)}
            )

        return check_constraints

    @reflection.cache
    def get_indexes(self, connection, table_name, schema=None, **kw):
        pragma_indexes = self._get_table_pragma(
            connection, "index_list", table_name, schema=schema
        )
        indexes = []

        include_auto_indexes = kw.pop("include_auto_indexes", False)
        for row in pragma_indexes:
            # ignore implicit primary key index.
            # https://www.mail-archive.com/sqlite-users@sqlite.org/msg30517.html
            if not include_auto_indexes and row[1].startswith(
                "sqlite_autoindex"
            ):
                continue
            indexes.append(dict(name=row[1], column_names=[], unique=row[2]))

        # loop thru unique indexes to get the column names.
        for idx in list(indexes):
            pragma_index = self._get_table_pragma(
                connection, "index_info", idx["name"]
            )

            for row in pragma_index:
                if row[2] is None:
                    util.warn(
                        "Skipped unsupported reflection of "
                        "expression-based index %s" % idx["name"]
                    )
                    indexes.remove(idx)
                    break
                else:
                    idx["column_names"].append(row[2])
        return indexes

    @reflection.cache
    def _get_table_sql(self, connection, table_name, schema=None, **kw):
        if schema:
            schema_expr = "%s." % (
                self.identifier_preparer.quote_identifier(schema)
            )
        else:
            schema_expr = ""
        try:
            s = (
                "SELECT sql FROM "
                " (SELECT * FROM %(schema)ssqlite_master UNION ALL "
                "  SELECT * FROM %(schema)ssqlite_temp_master) "
                "WHERE name = ? "
                "AND type = 'table'" % {"schema": schema_expr}
            )
            rs = connection.exec_driver_sql(s, (table_name,))
        except exc.DBAPIError:
            s = (
                "SELECT sql FROM %(schema)ssqlite_master "
                "WHERE name = ? "
                "AND type = 'table'" % {"schema": schema_expr}
            )
            rs = connection.exec_driver_sql(s, (table_name,))
        return rs.scalar()

    def _get_table_pragma(self, connection, pragma, table_name, schema=None):
        quote = self.identifier_preparer.quote_identifier
        if schema is not None:
            statements = ["PRAGMA %s." % quote(schema)]
        else:
            # because PRAGMA looks in all attached databases if no schema
            # given, need to specify "main" schema, however since we want
            # 'temp' tables in the same namespace as 'main', need to run
            # the PRAGMA twice
            statements = ["PRAGMA main.", "PRAGMA temp."]

        qtable = quote(table_name)
        for statement in statements:
            statement = "%s%s(%s)" % (statement, pragma, qtable)
            cursor = connection.exec_driver_sql(statement)
            if not cursor._soft_closed:
                # work around SQLite issue whereby cursor.description
                # is blank when PRAGMA returns no rows:
                # https://www.sqlite.org/cvstrac/tktview?tn=1884
                result = cursor.fetchall()
            else:
                result = []
            if result:
                return result
        else:
            return []
