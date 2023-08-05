# mssql/mxodbc.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""
.. dialect:: mssql+mxodbc
    :name: mxODBC
    :dbapi: mxodbc
    :connectstring: mssql+mxodbc://<username>:<password>@<dsnname>
    :url: https://www.egenix.com/

.. deprecated:: 1.4 The mxODBC DBAPI is deprecated and will be removed
   in a future version. Please use one of the supported DBAPIs to
   connect to mssql.

Execution Modes
---------------

mxODBC features two styles of statement execution, using the
``cursor.execute()`` and ``cursor.executedirect()`` methods (the second being
an extension to the DBAPI specification). The former makes use of a particular
API call specific to the SQL Server Native Client ODBC driver known
SQLDescribeParam, while the latter does not.

mxODBC apparently only makes repeated use of a single prepared statement
when SQLDescribeParam is used. The advantage to prepared statement reuse is
one of performance. The disadvantage is that SQLDescribeParam has a limited
set of scenarios in which bind parameters are understood, including that they
cannot be placed within the argument lists of function calls, anywhere outside
the FROM, or even within subqueries within the FROM clause - making the usage
of bind parameters within SELECT statements impossible for all but the most
simplistic statements.

For this reason, the mxODBC dialect uses the "native" mode by default only for
INSERT, UPDATE, and DELETE statements, and uses the escaped string mode for
all other statements.

This behavior can be controlled via
:meth:`~sqlalchemy.sql.expression.Executable.execution_options` using the
``native_odbc_execute`` flag with a value of ``True`` or ``False``, where a
value of ``True`` will unconditionally use native bind parameters and a value
of ``False`` will unconditionally use string-escaped parameters.

"""


from .base import _MSDate
from .base import _MSDateTime
from .base import _MSTime
from .base import MSDialect
from .base import VARBINARY
from .pyodbc import _MSNumeric_pyodbc
from .pyodbc import MSExecutionContext_pyodbc
from ... import types as sqltypes
from ...connectors.mxodbc import MxODBCConnector


class _MSNumeric_mxodbc(_MSNumeric_pyodbc):
    """Include pyodbc's numeric processor."""


class _MSDate_mxodbc(_MSDate):
    def bind_processor(self, dialect):
        def process(value):
            if value is not None:
                return "%s-%s-%s" % (value.year, value.month, value.day)
            else:
                return None

        return process


class _MSTime_mxodbc(_MSTime):
    def bind_processor(self, dialect):
        def process(value):
            if value is not None:
                return "%s:%s:%s" % (value.hour, value.minute, value.second)
            else:
                return None

        return process


class _VARBINARY_mxodbc(VARBINARY):

    """
    mxODBC Support for VARBINARY column types.

    This handles the special case for null VARBINARY values,
    which maps None values to the mx.ODBC.Manager.BinaryNull symbol.
    """

    def bind_processor(self, dialect):
        if dialect.dbapi is None:
            return None

        DBAPIBinary = dialect.dbapi.Binary

        def process(value):
            if value is not None:
                return DBAPIBinary(value)
            else:
                # should pull from mx.ODBC.Manager.BinaryNull
                return dialect.dbapi.BinaryNull

        return process


class MSExecutionContext_mxodbc(MSExecutionContext_pyodbc):
    """
    The pyodbc execution context is useful for enabling
    SELECT SCOPE_IDENTITY in cases where OUTPUT clause
    does not work (tables with insert triggers).
    """

    # todo - investigate whether the pyodbc execution context
    #       is really only being used in cases where OUTPUT
    #       won't work.


class MSDialect_mxodbc(MxODBCConnector, MSDialect):

    # this is only needed if "native ODBC" mode is used,
    # which is now disabled by default.
    # statement_compiler = MSSQLStrictCompiler
    supports_statement_cache = True

    execution_ctx_cls = MSExecutionContext_mxodbc

    # flag used by _MSNumeric_mxodbc
    _need_decimal_fix = True

    colspecs = {
        sqltypes.Numeric: _MSNumeric_mxodbc,
        sqltypes.DateTime: _MSDateTime,
        sqltypes.Date: _MSDate_mxodbc,
        sqltypes.Time: _MSTime_mxodbc,
        VARBINARY: _VARBINARY_mxodbc,
        sqltypes.LargeBinary: _VARBINARY_mxodbc,
    }

    def __init__(self, description_encoding=None, **params):
        super(MSDialect_mxodbc, self).__init__(**params)
        self.description_encoding = description_encoding


dialect = MSDialect_mxodbc
