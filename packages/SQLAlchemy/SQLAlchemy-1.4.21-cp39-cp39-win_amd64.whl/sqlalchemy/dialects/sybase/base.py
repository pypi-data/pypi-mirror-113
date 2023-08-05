# sybase/base.py
# Copyright (C) 2010-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
# get_select_precolumns(), limit_clause() implementation
# copyright (C) 2007 Fisch Asset Management
# AG https://www.fam.ch, with coding by Alexander Houben
# alexander.houben@thor-solutions.ch
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""

.. dialect:: sybase
    :name: Sybase

.. note::

    The Sybase dialect within SQLAlchemy **is not currently supported**.
    It is not tested within continuous integration and is likely to have
    many issues and caveats not currently handled. Consider using the
    `external dialect <https://github.com/gordthompson/sqlalchemy-sybase>`_
    instead.

.. deprecated:: 1.4 The internal Sybase dialect is deprecated and will be
   removed in a future version. Use the external dialect.

"""

import re

from sqlalchemy import exc
from sqlalchemy import schema as sa_schema
from sqlalchemy import types as sqltypes
from sqlalchemy import util
from sqlalchemy.engine import default
from sqlalchemy.engine import reflection
from sqlalchemy.sql import compiler
from sqlalchemy.sql import text
from sqlalchemy.types import BIGINT
from sqlalchemy.types import BINARY
from sqlalchemy.types import CHAR
from sqlalchemy.types import DATE
from sqlalchemy.types import DATETIME
from sqlalchemy.types import DECIMAL
from sqlalchemy.types import FLOAT
from sqlalchemy.types import INT  # noqa
from sqlalchemy.types import INTEGER
from sqlalchemy.types import NCHAR
from sqlalchemy.types import NUMERIC
from sqlalchemy.types import NVARCHAR
from sqlalchemy.types import REAL
from sqlalchemy.types import SMALLINT
from sqlalchemy.types import TEXT
from sqlalchemy.types import TIME
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.types import Unicode
from sqlalchemy.types import VARBINARY
from sqlalchemy.types import VARCHAR


RESERVED_WORDS = set(
    [
        "add",
        "all",
        "alter",
        "and",
        "any",
        "as",
        "asc",
        "backup",
        "begin",
        "between",
        "bigint",
        "binary",
        "bit",
        "bottom",
        "break",
        "by",
        "call",
        "capability",
        "cascade",
        "case",
        "cast",
        "char",
        "char_convert",
        "character",
        "check",
        "checkpoint",
        "close",
        "comment",
        "commit",
        "connect",
        "constraint",
        "contains",
        "continue",
        "convert",
        "create",
        "cross",
        "cube",
        "current",
        "current_timestamp",
        "current_user",
        "cursor",
        "date",
        "dbspace",
        "deallocate",
        "dec",
        "decimal",
        "declare",
        "default",
        "delete",
        "deleting",
        "desc",
        "distinct",
        "do",
        "double",
        "drop",
        "dynamic",
        "else",
        "elseif",
        "encrypted",
        "end",
        "endif",
        "escape",
        "except",
        "exception",
        "exec",
        "execute",
        "existing",
        "exists",
        "externlogin",
        "fetch",
        "first",
        "float",
        "for",
        "force",
        "foreign",
        "forward",
        "from",
        "full",
        "goto",
        "grant",
        "group",
        "having",
        "holdlock",
        "identified",
        "if",
        "in",
        "index",
        "index_lparen",
        "inner",
        "inout",
        "insensitive",
        "insert",
        "inserting",
        "install",
        "instead",
        "int",
        "integer",
        "integrated",
        "intersect",
        "into",
        "iq",
        "is",
        "isolation",
        "join",
        "key",
        "lateral",
        "left",
        "like",
        "lock",
        "login",
        "long",
        "match",
        "membership",
        "message",
        "mode",
        "modify",
        "natural",
        "new",
        "no",
        "noholdlock",
        "not",
        "notify",
        "null",
        "numeric",
        "of",
        "off",
        "on",
        "open",
        "option",
        "options",
        "or",
        "order",
        "others",
        "out",
        "outer",
        "over",
        "passthrough",
        "precision",
        "prepare",
        "primary",
        "print",
        "privileges",
        "proc",
        "procedure",
        "publication",
        "raiserror",
        "readtext",
        "real",
        "reference",
        "references",
        "release",
        "remote",
        "remove",
        "rename",
        "reorganize",
        "resource",
        "restore",
        "restrict",
        "return",
        "revoke",
        "right",
        "rollback",
        "rollup",
        "save",
        "savepoint",
        "scroll",
        "select",
        "sensitive",
        "session",
        "set",
        "setuser",
        "share",
        "smallint",
        "some",
        "sqlcode",
        "sqlstate",
        "start",
        "stop",
        "subtrans",
        "subtransaction",
        "synchronize",
        "syntax_error",
        "table",
        "temporary",
        "then",
        "time",
        "timestamp",
        "tinyint",
        "to",
        "top",
        "tran",
        "trigger",
        "truncate",
        "tsequal",
        "unbounded",
        "union",
        "unique",
        "unknown",
        "unsigned",
        "update",
        "updating",
        "user",
        "using",
        "validate",
        "values",
        "varbinary",
        "varchar",
        "variable",
        "varying",
        "view",
        "wait",
        "waitfor",
        "when",
        "where",
        "while",
        "window",
        "with",
        "with_cube",
        "with_lparen",
        "with_rollup",
        "within",
        "work",
        "writetext",
    ]
)


class _SybaseUnitypeMixin(object):
    """these types appear to return a buffer object."""

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                return str(value)  # decode("ucs-2")
            else:
                return None

        return process


class UNICHAR(_SybaseUnitypeMixin, sqltypes.Unicode):
    __visit_name__ = "UNICHAR"


class UNIVARCHAR(_SybaseUnitypeMixin, sqltypes.Unicode):
    __visit_name__ = "UNIVARCHAR"


class UNITEXT(_SybaseUnitypeMixin, sqltypes.UnicodeText):
    __visit_name__ = "UNITEXT"


class TINYINT(sqltypes.Integer):
    __visit_name__ = "TINYINT"


class BIT(sqltypes.TypeEngine):
    __visit_name__ = "BIT"


class MONEY(sqltypes.TypeEngine):
    __visit_name__ = "MONEY"


class SMALLMONEY(sqltypes.TypeEngine):
    __visit_name__ = "SMALLMONEY"


class UNIQUEIDENTIFIER(sqltypes.TypeEngine):
    __visit_name__ = "UNIQUEIDENTIFIER"


class IMAGE(sqltypes.LargeBinary):
    __visit_name__ = "IMAGE"


class SybaseTypeCompiler(compiler.GenericTypeCompiler):
    def visit_large_binary(self, type_, **kw):
        return self.visit_IMAGE(type_)

    def visit_boolean(self, type_, **kw):
        return self.visit_BIT(type_)

    def visit_unicode(self, type_, **kw):
        return self.visit_NVARCHAR(type_)

    def visit_UNICHAR(self, type_, **kw):
        return "UNICHAR(%d)" % type_.length

    def visit_UNIVARCHAR(self, type_, **kw):
        return "UNIVARCHAR(%d)" % type_.length

    def visit_UNITEXT(self, type_, **kw):
        return "UNITEXT"

    def visit_TINYINT(self, type_, **kw):
        return "TINYINT"

    def visit_IMAGE(self, type_, **kw):
        return "IMAGE"

    def visit_BIT(self, type_, **kw):
        return "BIT"

    def visit_MONEY(self, type_, **kw):
        return "MONEY"

    def visit_SMALLMONEY(self, type_, **kw):
        return "SMALLMONEY"

    def visit_UNIQUEIDENTIFIER(self, type_, **kw):
        return "UNIQUEIDENTIFIER"


ischema_names = {
    "bigint": BIGINT,
    "int": INTEGER,
    "integer": INTEGER,
    "smallint": SMALLINT,
    "tinyint": TINYINT,
    "unsigned bigint": BIGINT,  # TODO: unsigned flags
    "unsigned int": INTEGER,  # TODO: unsigned flags
    "unsigned smallint": SMALLINT,  # TODO: unsigned flags
    "numeric": NUMERIC,
    "decimal": DECIMAL,
    "dec": DECIMAL,
    "float": FLOAT,
    "double": NUMERIC,  # TODO
    "double precision": NUMERIC,  # TODO
    "real": REAL,
    "smallmoney": SMALLMONEY,
    "money": MONEY,
    "smalldatetime": DATETIME,
    "datetime": DATETIME,
    "date": DATE,
    "time": TIME,
    "char": CHAR,
    "character": CHAR,
    "varchar": VARCHAR,
    "character varying": VARCHAR,
    "char varying": VARCHAR,
    "unichar": UNICHAR,
    "unicode character": UNIVARCHAR,
    "nchar": NCHAR,
    "national char": NCHAR,
    "national character": NCHAR,
    "nvarchar": NVARCHAR,
    "nchar varying": NVARCHAR,
    "national char varying": NVARCHAR,
    "national character varying": NVARCHAR,
    "text": TEXT,
    "unitext": UNITEXT,
    "binary": BINARY,
    "varbinary": VARBINARY,
    "image": IMAGE,
    "bit": BIT,
    # not in documentation for ASE 15.7
    "long varchar": TEXT,  # TODO
    "timestamp": TIMESTAMP,
    "uniqueidentifier": UNIQUEIDENTIFIER,
}


class SybaseInspector(reflection.Inspector):
    def __init__(self, conn):
        reflection.Inspector.__init__(self, conn)

    def get_table_id(self, table_name, schema=None):
        """Return the table id from `table_name` and `schema`."""

        return self.dialect.get_table_id(
            self.bind, table_name, schema, info_cache=self.info_cache
        )


class SybaseExecutionContext(default.DefaultExecutionContext):
    _enable_identity_insert = False

    def set_ddl_autocommit(self, connection, value):
        """Must be implemented by subclasses to accommodate DDL executions.

        "connection" is the raw unwrapped DBAPI connection.   "value"
        is True or False.  when True, the connection should be configured
        such that a DDL can take place subsequently.  when False,
        a DDL has taken place and the connection should be resumed
        into non-autocommit mode.

        """
        raise NotImplementedError()

    def pre_exec(self):
        if self.isinsert:
            tbl = self.compiled.statement.table
            seq_column = tbl._autoincrement_column
            insert_has_sequence = seq_column is not None

            if insert_has_sequence:
                self._enable_identity_insert = (
                    seq_column.key in self.compiled_parameters[0]
                )
            else:
                self._enable_identity_insert = False

            if self._enable_identity_insert:
                self.cursor.execute(
                    "SET IDENTITY_INSERT %s ON"
                    % self.dialect.identifier_preparer.format_table(tbl)
                )

        if self.isddl:
            # TODO: to enhance this, we can detect "ddl in tran" on the
            # database settings.  this error message should be improved to
            # include a note about that.
            if not self.should_autocommit:
                raise exc.InvalidRequestError(
                    "The Sybase dialect only supports "
                    "DDL in 'autocommit' mode at this time."
                )

            self.root_connection.engine.logger.info(
                "AUTOCOMMIT (Assuming no Sybase 'ddl in tran')"
            )

            self.set_ddl_autocommit(
                self.root_connection.connection.connection, True
            )

    def post_exec(self):
        if self.isddl:
            self.set_ddl_autocommit(self.root_connection, False)

        if self._enable_identity_insert:
            self.cursor.execute(
                "SET IDENTITY_INSERT %s OFF"
                % self.dialect.identifier_preparer.format_table(
                    self.compiled.statement.table
                )
            )

    def get_lastrowid(self):
        cursor = self.create_cursor()
        cursor.execute("SELECT @@identity AS lastrowid")
        lastrowid = cursor.fetchone()[0]
        cursor.close()
        return lastrowid


class SybaseSQLCompiler(compiler.SQLCompiler):
    ansi_bind_rules = True

    extract_map = util.update_copy(
        compiler.SQLCompiler.extract_map,
        {"doy": "dayofyear", "dow": "weekday", "milliseconds": "millisecond"},
    )

    def get_from_hint_text(self, table, text):
        return text

    def limit_clause(self, select, **kw):
        text = ""
        if select._limit_clause is not None:
            text += " ROWS LIMIT " + self.process(select._limit_clause, **kw)
        if select._offset_clause is not None:
            if select._limit_clause is None:
                text += " ROWS"
            text += " OFFSET " + self.process(select._offset_clause, **kw)
        return text

    def visit_extract(self, extract, **kw):
        field = self.extract_map.get(extract.field, extract.field)
        return 'DATEPART("%s", %s)' % (field, self.process(extract.expr, **kw))

    def visit_now_func(self, fn, **kw):
        return "GETDATE()"

    def for_update_clause(self, select):
        # "FOR UPDATE" is only allowed on "DECLARE CURSOR"
        # which SQLAlchemy doesn't use
        return ""

    def order_by_clause(self, select, **kw):
        kw["literal_binds"] = True
        order_by = self.process(select._order_by_clause, **kw)

        # SybaseSQL only allows ORDER BY in subqueries if there is a LIMIT
        if order_by and (not self.is_subquery() or select._limit):
            return " ORDER BY " + order_by
        else:
            return ""

    def delete_table_clause(self, delete_stmt, from_table, extra_froms):
        """If we have extra froms make sure we render any alias as hint."""
        ashint = False
        if extra_froms:
            ashint = True
        return from_table._compiler_dispatch(
            self, asfrom=True, iscrud=True, ashint=ashint
        )

    def delete_extra_from_clause(
        self, delete_stmt, from_table, extra_froms, from_hints, **kw
    ):
        """Render the DELETE .. FROM clause specific to Sybase."""
        kw["asfrom"] = True
        return "FROM " + ", ".join(
            t._compiler_dispatch(self, fromhints=from_hints, **kw)
            for t in [from_table] + extra_froms
        )


class SybaseDDLCompiler(compiler.DDLCompiler):
    def get_column_specification(self, column, **kwargs):
        colspec = (
            self.preparer.format_column(column)
            + " "
            + self.dialect.type_compiler.process(
                column.type, type_expression=column
            )
        )

        if column.table is None:
            raise exc.CompileError(
                "The Sybase dialect requires Table-bound "
                "columns in order to generate DDL"
            )
        seq_col = column.table._autoincrement_column

        # install a IDENTITY Sequence if we have an implicit IDENTITY column
        if seq_col is column:
            sequence = (
                isinstance(column.default, sa_schema.Sequence)
                and column.default
            )
            if sequence:
                start, increment = sequence.start or 1, sequence.increment or 1
            else:
                start, increment = 1, 1
            if (start, increment) == (1, 1):
                colspec += " IDENTITY"
            else:
                # TODO: need correct syntax for this
                colspec += " IDENTITY(%s,%s)" % (start, increment)
        else:
            default = self.get_column_default_string(column)
            if default is not None:
                colspec += " DEFAULT " + default

            if column.nullable is not None:
                if not column.nullable or column.primary_key:
                    colspec += " NOT NULL"
                else:
                    colspec += " NULL"

        return colspec

    def visit_drop_index(self, drop):
        index = drop.element
        return "\nDROP INDEX %s.%s" % (
            self.preparer.quote_identifier(index.table.name),
            self._prepared_index_name(drop.element, include_schema=False),
        )


class SybaseIdentifierPreparer(compiler.IdentifierPreparer):
    reserved_words = RESERVED_WORDS


class SybaseDialect(default.DefaultDialect):
    name = "sybase"
    supports_unicode_statements = False
    supports_sane_rowcount = False
    supports_sane_multi_rowcount = False
    supports_statement_cache = True

    supports_native_boolean = False
    supports_unicode_binds = False
    postfetch_lastrowid = True

    colspecs = {}
    ischema_names = ischema_names

    type_compiler = SybaseTypeCompiler
    statement_compiler = SybaseSQLCompiler
    ddl_compiler = SybaseDDLCompiler
    preparer = SybaseIdentifierPreparer
    inspector = SybaseInspector

    construct_arguments = []

    def __init__(self, *args, **kwargs):
        util.warn_deprecated(
            "The Sybase dialect is deprecated and will be removed "
            "in a future version. This dialect is superseded by the external "
            "dialect https://github.com/gordthompson/sqlalchemy-sybase.",
            version="1.4",
        )
        super(SybaseDialect, self).__init__(*args, **kwargs)

    def _get_default_schema_name(self, connection):
        return connection.scalar(
            text("SELECT user_name() as user_name").columns(username=Unicode)
        )

    def initialize(self, connection):
        super(SybaseDialect, self).initialize(connection)
        if (
            self.server_version_info is not None
            and self.server_version_info < (15,)
        ):
            self.max_identifier_length = 30
        else:
            self.max_identifier_length = 255

    def get_table_id(self, connection, table_name, schema=None, **kw):
        """Fetch the id for schema.table_name.

        Several reflection methods require the table id.  The idea for using
        this method is that it can be fetched one time and cached for
        subsequent calls.

        """

        table_id = None
        if schema is None:
            schema = self.default_schema_name

        TABLEID_SQL = text(
            """
          SELECT o.id AS id
          FROM sysobjects o JOIN sysusers u ON o.uid=u.uid
          WHERE u.name = :schema_name
              AND o.name = :table_name
              AND o.type in ('U', 'V')
        """
        )

        if util.py2k:
            if isinstance(schema, unicode):  # noqa
                schema = schema.encode("ascii")
            if isinstance(table_name, unicode):  # noqa
                table_name = table_name.encode("ascii")
        result = connection.execute(
            TABLEID_SQL, schema_name=schema, table_name=table_name
        )
        table_id = result.scalar()
        if table_id is None:
            raise exc.NoSuchTableError(table_name)
        return table_id

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        table_id = self.get_table_id(
            connection, table_name, schema, info_cache=kw.get("info_cache")
        )

        COLUMN_SQL = text(
            """
          SELECT col.name AS name,
                 t.name AS type,
                 (col.status & 8) AS nullable,
                 (col.status & 128) AS autoincrement,
                 com.text AS 'default',
                 col.prec AS precision,
                 col.scale AS scale,
                 col.length AS length
          FROM systypes t, syscolumns col LEFT OUTER JOIN syscomments com ON
              col.cdefault = com.id
          WHERE col.usertype = t.usertype
              AND col.id = :table_id
          ORDER BY col.colid
        """
        )

        results = connection.execute(COLUMN_SQL, table_id=table_id)

        columns = []
        for (
            name,
            type_,
            nullable,
            autoincrement,
            default_,
            precision,
            scale,
            length,
        ) in results:
            col_info = self._get_column_info(
                name,
                type_,
                bool(nullable),
                bool(autoincrement),
                default_,
                precision,
                scale,
                length,
            )
            columns.append(col_info)

        return columns

    def _get_column_info(
        self,
        name,
        type_,
        nullable,
        autoincrement,
        default,
        precision,
        scale,
        length,
    ):

        coltype = self.ischema_names.get(type_, None)

        kwargs = {}

        if coltype in (NUMERIC, DECIMAL):
            args = (precision, scale)
        elif coltype == FLOAT:
            args = (precision,)
        elif coltype in (CHAR, VARCHAR, UNICHAR, UNIVARCHAR, NCHAR, NVARCHAR):
            args = (length,)
        else:
            args = ()

        if coltype:
            coltype = coltype(*args, **kwargs)
            # is this necessary
            # if is_array:
            #     coltype = ARRAY(coltype)
        else:
            util.warn(
                "Did not recognize type '%s' of column '%s'" % (type_, name)
            )
            coltype = sqltypes.NULLTYPE

        if default:
            default = default.replace("DEFAULT", "").strip()
            default = re.sub("^'(.*)'$", lambda m: m.group(1), default)
        else:
            default = None

        column_info = dict(
            name=name,
            type=coltype,
            nullable=nullable,
            default=default,
            autoincrement=autoincrement,
        )
        return column_info

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):

        table_id = self.get_table_id(
            connection, table_name, schema, info_cache=kw.get("info_cache")
        )

        table_cache = {}
        column_cache = {}
        foreign_keys = []

        table_cache[table_id] = {"name": table_name, "schema": schema}

        COLUMN_SQL = text(
            """
          SELECT c.colid AS id, c.name AS name
          FROM syscolumns c
          WHERE c.id = :table_id
        """
        )

        results = connection.execute(COLUMN_SQL, table_id=table_id)
        columns = {}
        for col in results:
            columns[col["id"]] = col["name"]
        column_cache[table_id] = columns

        REFCONSTRAINT_SQL = text(
            """
          SELECT o.name AS name, r.reftabid AS reftable_id,
            r.keycnt AS 'count',
            r.fokey1 AS fokey1, r.fokey2 AS fokey2, r.fokey3 AS fokey3,
            r.fokey4 AS fokey4, r.fokey5 AS fokey5, r.fokey6 AS fokey6,
            r.fokey7 AS fokey7, r.fokey1 AS fokey8, r.fokey9 AS fokey9,
            r.fokey10 AS fokey10, r.fokey11 AS fokey11, r.fokey12 AS fokey12,
            r.fokey13 AS fokey13, r.fokey14 AS fokey14, r.fokey15 AS fokey15,
            r.fokey16 AS fokey16,
            r.refkey1 AS refkey1, r.refkey2 AS refkey2, r.refkey3 AS refkey3,
            r.refkey4 AS refkey4, r.refkey5 AS refkey5, r.refkey6 AS refkey6,
            r.refkey7 AS refkey7, r.refkey1 AS refkey8, r.refkey9 AS refkey9,
            r.refkey10 AS refkey10, r.refkey11 AS refkey11,
            r.refkey12 AS refkey12, r.refkey13 AS refkey13,
            r.refkey14 AS refkey14, r.refkey15 AS refkey15,
            r.refkey16 AS refkey16
          FROM sysreferences r JOIN sysobjects o on r.tableid = o.id
          WHERE r.tableid = :table_id
        """
        )
        referential_constraints = connection.execute(
            REFCONSTRAINT_SQL, table_id=table_id
        ).fetchall()

        REFTABLE_SQL = text(
            """
          SELECT o.name AS name, u.name AS 'schema'
          FROM sysobjects o JOIN sysusers u ON o.uid = u.uid
          WHERE o.id = :table_id
        """
        )

        for r in referential_constraints:
            reftable_id = r["reftable_id"]

            if reftable_id not in table_cache:
                c = connection.execute(REFTABLE_SQL, table_id=reftable_id)
                reftable = c.fetchone()
                c.close()
                table_info = {"name": reftable["name"], "schema": None}
                if (
                    schema is not None
                    or reftable["schema"] != self.default_schema_name
                ):
                    table_info["schema"] = reftable["schema"]

                table_cache[reftable_id] = table_info
                results = connection.execute(COLUMN_SQL, table_id=reftable_id)
                reftable_columns = {}
                for col in results:
                    reftable_columns[col["id"]] = col["name"]
                column_cache[reftable_id] = reftable_columns

            reftable = table_cache[reftable_id]
            reftable_columns = column_cache[reftable_id]

            constrained_columns = []
            referred_columns = []
            for i in range(1, r["count"] + 1):
                constrained_columns.append(columns[r["fokey%i" % i]])
                referred_columns.append(reftable_columns[r["refkey%i" % i]])

            fk_info = {
                "constrained_columns": constrained_columns,
                "referred_schema": reftable["schema"],
                "referred_table": reftable["name"],
                "referred_columns": referred_columns,
                "name": r["name"],
            }

            foreign_keys.append(fk_info)

        return foreign_keys

    @reflection.cache
    def get_indexes(self, connection, table_name, schema=None, **kw):
        table_id = self.get_table_id(
            connection, table_name, schema, info_cache=kw.get("info_cache")
        )

        INDEX_SQL = text(
            """
          SELECT object_name(i.id) AS table_name,
                 i.keycnt AS 'count',
                 i.name AS name,
                 (i.status & 0x2) AS 'unique',
                 index_col(object_name(i.id), i.indid, 1) AS col_1,
                 index_col(object_name(i.id), i.indid, 2) AS col_2,
                 index_col(object_name(i.id), i.indid, 3) AS col_3,
                 index_col(object_name(i.id), i.indid, 4) AS col_4,
                 index_col(object_name(i.id), i.indid, 5) AS col_5,
                 index_col(object_name(i.id), i.indid, 6) AS col_6,
                 index_col(object_name(i.id), i.indid, 7) AS col_7,
                 index_col(object_name(i.id), i.indid, 8) AS col_8,
                 index_col(object_name(i.id), i.indid, 9) AS col_9,
                 index_col(object_name(i.id), i.indid, 10) AS col_10,
                 index_col(object_name(i.id), i.indid, 11) AS col_11,
                 index_col(object_name(i.id), i.indid, 12) AS col_12,
                 index_col(object_name(i.id), i.indid, 13) AS col_13,
                 index_col(object_name(i.id), i.indid, 14) AS col_14,
                 index_col(object_name(i.id), i.indid, 15) AS col_15,
                 index_col(object_name(i.id), i.indid, 16) AS col_16
          FROM sysindexes i, sysobjects o
          WHERE o.id = i.id
            AND o.id = :table_id
            AND (i.status & 2048) = 0
            AND i.indid BETWEEN 1 AND 254
        """
        )

        results = connection.execute(INDEX_SQL, table_id=table_id)
        indexes = []
        for r in results:
            column_names = []
            for i in range(1, r["count"]):
                column_names.append(r["col_%i" % (i,)])
            index_info = {
                "name": r["name"],
                "unique": bool(r["unique"]),
                "column_names": column_names,
            }
            indexes.append(index_info)

        return indexes

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        table_id = self.get_table_id(
            connection, table_name, schema, info_cache=kw.get("info_cache")
        )

        PK_SQL = text(
            """
          SELECT object_name(i.id) AS table_name,
                 i.keycnt AS 'count',
                 i.name AS name,
                 index_col(object_name(i.id), i.indid, 1) AS pk_1,
                 index_col(object_name(i.id), i.indid, 2) AS pk_2,
                 index_col(object_name(i.id), i.indid, 3) AS pk_3,
                 index_col(object_name(i.id), i.indid, 4) AS pk_4,
                 index_col(object_name(i.id), i.indid, 5) AS pk_5,
                 index_col(object_name(i.id), i.indid, 6) AS pk_6,
                 index_col(object_name(i.id), i.indid, 7) AS pk_7,
                 index_col(object_name(i.id), i.indid, 8) AS pk_8,
                 index_col(object_name(i.id), i.indid, 9) AS pk_9,
                 index_col(object_name(i.id), i.indid, 10) AS pk_10,
                 index_col(object_name(i.id), i.indid, 11) AS pk_11,
                 index_col(object_name(i.id), i.indid, 12) AS pk_12,
                 index_col(object_name(i.id), i.indid, 13) AS pk_13,
                 index_col(object_name(i.id), i.indid, 14) AS pk_14,
                 index_col(object_name(i.id), i.indid, 15) AS pk_15,
                 index_col(object_name(i.id), i.indid, 16) AS pk_16
          FROM sysindexes i, sysobjects o
          WHERE o.id = i.id
            AND o.id = :table_id
            AND (i.status & 2048) = 2048
            AND i.indid BETWEEN 1 AND 254
        """
        )

        results = connection.execute(PK_SQL, table_id=table_id)
        pks = results.fetchone()
        results.close()

        constrained_columns = []
        if pks:
            for i in range(1, pks["count"] + 1):
                constrained_columns.append(pks["pk_%i" % (i,)])
            return {
                "constrained_columns": constrained_columns,
                "name": pks["name"],
            }
        else:
            return {"constrained_columns": [], "name": None}

    @reflection.cache
    def get_schema_names(self, connection, **kw):

        SCHEMA_SQL = text("SELECT u.name AS name FROM sysusers u")

        schemas = connection.execute(SCHEMA_SQL)

        return [s["name"] for s in schemas]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        if schema is None:
            schema = self.default_schema_name

        TABLE_SQL = text(
            """
          SELECT o.name AS name
          FROM sysobjects o JOIN sysusers u ON o.uid = u.uid
          WHERE u.name = :schema_name
            AND o.type = 'U'
        """
        )

        if util.py2k:
            if isinstance(schema, unicode):  # noqa
                schema = schema.encode("ascii")

        tables = connection.execute(TABLE_SQL, schema_name=schema)

        return [t["name"] for t in tables]

    @reflection.cache
    def get_view_definition(self, connection, view_name, schema=None, **kw):
        if schema is None:
            schema = self.default_schema_name

        VIEW_DEF_SQL = text(
            """
          SELECT c.text
          FROM syscomments c JOIN sysobjects o ON c.id = o.id
          WHERE o.name = :view_name
            AND o.type = 'V'
        """
        )

        if util.py2k:
            if isinstance(view_name, unicode):  # noqa
                view_name = view_name.encode("ascii")

        view = connection.execute(VIEW_DEF_SQL, view_name=view_name)

        return view.scalar()

    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        if schema is None:
            schema = self.default_schema_name

        VIEW_SQL = text(
            """
          SELECT o.name AS name
          FROM sysobjects o JOIN sysusers u ON o.uid = u.uid
          WHERE u.name = :schema_name
            AND o.type = 'V'
        """
        )

        if util.py2k:
            if isinstance(schema, unicode):  # noqa
                schema = schema.encode("ascii")
        views = connection.execute(VIEW_SQL, schema_name=schema)

        return [v["name"] for v in views]

    def has_table(self, connection, table_name, schema=None):
        self._ensure_has_table_connection(connection)

        try:
            self.get_table_id(connection, table_name, schema)
        except exc.NoSuchTableError:
            return False
        else:
            return True
