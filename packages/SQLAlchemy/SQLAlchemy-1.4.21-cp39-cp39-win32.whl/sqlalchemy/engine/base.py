# engine/base.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php
from __future__ import with_statement

import contextlib
import sys

from .interfaces import Connectable
from .interfaces import ExceptionContext
from .util import _distill_params
from .util import _distill_params_20
from .util import TransactionalContext
from .. import exc
from .. import inspection
from .. import log
from .. import util
from ..sql import compiler
from ..sql import util as sql_util


"""Defines :class:`_engine.Connection` and :class:`_engine.Engine`.

"""

_EMPTY_EXECUTION_OPTS = util.immutabledict()


class Connection(Connectable):
    """Provides high-level functionality for a wrapped DB-API connection.

    **This is the SQLAlchemy 1.x.x version** of the :class:`_engine.Connection`
    class.   For the :term:`2.0 style` version, which features some API
    differences, see :class:`_future.Connection`.

    The :class:`_engine.Connection` object is procured by calling
    the :meth:`_engine.Engine.connect` method of the :class:`_engine.Engine`
    object, and provides services for execution of SQL statements as well
    as transaction control.

    The Connection object is **not** thread-safe.  While a Connection can be
    shared among threads using properly synchronized access, it is still
    possible that the underlying DBAPI connection may not support shared
    access between threads.  Check the DBAPI documentation for details.

    The Connection object represents a single DBAPI connection checked out
    from the connection pool. In this state, the connection pool has no affect
    upon the connection, including its expiration or timeout state. For the
    connection pool to properly manage connections, connections should be
    returned to the connection pool (i.e. ``connection.close()``) whenever the
    connection is not in use.

    .. index::
      single: thread safety; Connection

    """

    _is_future = False
    _sqla_logger_namespace = "sqlalchemy.engine.Connection"

    # used by sqlalchemy.engine.util.TransactionalContext
    _trans_context_manager = None

    def __init__(
        self,
        engine,
        connection=None,
        close_with_result=False,
        _branch_from=None,
        _execution_options=None,
        _dispatch=None,
        _has_events=None,
        _allow_revalidate=True,
    ):
        """Construct a new Connection."""
        self.engine = engine
        self.dialect = engine.dialect
        self.__branch_from = _branch_from

        if _branch_from:
            # branching is always "from" the root connection
            assert _branch_from.__branch_from is None
            self._dbapi_connection = connection
            self._execution_options = _execution_options
            self._echo = _branch_from._echo
            self.should_close_with_result = False
            self.dispatch = _dispatch
            self._has_events = _branch_from._has_events
        else:
            self._dbapi_connection = (
                connection
                if connection is not None
                else engine.raw_connection()
            )

            self._transaction = self._nested_transaction = None
            self.__savepoint_seq = 0
            self.__in_begin = False
            self.should_close_with_result = close_with_result

            self.__can_reconnect = _allow_revalidate
            self._echo = self.engine._should_log_info()

            if _has_events is None:
                # if _has_events is sent explicitly as False,
                # then don't join the dispatch of the engine; we don't
                # want to handle any of the engine's events in that case.
                self.dispatch = self.dispatch._join(engine.dispatch)
            self._has_events = _has_events or (
                _has_events is None and engine._has_events
            )

            assert not _execution_options
            self._execution_options = engine._execution_options

        if self._has_events or self.engine._has_events:
            self.dispatch.engine_connect(self, _branch_from is not None)

    @util.memoized_property
    def _message_formatter(self):
        if "logging_token" in self._execution_options:
            token = self._execution_options["logging_token"]
            return lambda msg: "[%s] %s" % (token, msg)
        else:
            return None

    def _log_info(self, message, *arg, **kw):
        fmt = self._message_formatter

        if fmt:
            message = fmt(message)

        self.engine.logger.info(message, *arg, **kw)

    def _log_debug(self, message, *arg, **kw):
        fmt = self._message_formatter

        if fmt:
            message = fmt(message)

        self.engine.logger.debug(message, *arg, **kw)

    @property
    def _schema_translate_map(self):
        return self._execution_options.get("schema_translate_map", None)

    def schema_for_object(self, obj):
        """Return the schema name for the given schema item taking into
        account current schema translate map.

        """

        name = obj.schema
        schema_translate_map = self._execution_options.get(
            "schema_translate_map", None
        )

        if (
            schema_translate_map
            and name in schema_translate_map
            and obj._use_schema_map
        ):
            return schema_translate_map[name]
        else:
            return name

    def _branch(self):
        """Return a new Connection which references this Connection's
        engine and connection; but does not have close_with_result enabled,
        and also whose close() method does nothing.

        .. deprecated:: 1.4 the "branching" concept will be removed in
           SQLAlchemy 2.0 as well as the "Connection.connect()" method which
           is the only consumer for this.

        The Core uses this very sparingly, only in the case of
        custom SQL default functions that are to be INSERTed as the
        primary key of a row where we need to get the value back, so we have
        to invoke it distinctly - this is a very uncommon case.

        Userland code accesses _branch() when the connect()
        method is called.  The branched connection
        acts as much as possible like the parent, except that it stays
        connected when a close() event occurs.

        """
        return self.engine._connection_cls(
            self.engine,
            self._dbapi_connection,
            _branch_from=self.__branch_from if self.__branch_from else self,
            _execution_options=self._execution_options,
            _has_events=self._has_events,
            _dispatch=self.dispatch,
        )

    def _generate_for_options(self):
        """define connection method chaining behavior for execution_options"""

        if self._is_future:
            return self
        else:
            c = self.__class__.__new__(self.__class__)
            c.__dict__ = self.__dict__.copy()
            return c

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.close()

    def execution_options(self, **opt):
        r""" Set non-SQL options for the connection which take effect
        during execution.

        For a "future" style connection, this method returns this same
        :class:`_future.Connection` object with the new options added.

        For a legacy connection, this method returns a copy of this
        :class:`_engine.Connection` which references the same underlying DBAPI
        connection, but also defines the given execution options which will
        take effect for a call to
        :meth:`execute`. As the new :class:`_engine.Connection` references the
        same underlying resource, it's usually a good idea to ensure that
        the copies will be discarded immediately, which is implicit if used
        as in::

            result = connection.execution_options(stream_results=True).\
                                execute(stmt)

        Note that any key/value can be passed to
        :meth:`_engine.Connection.execution_options`,
        and it will be stored in the
        ``_execution_options`` dictionary of the :class:`_engine.Connection`.
        It
        is suitable for usage by end-user schemes to communicate with
        event listeners, for example.

        The keywords that are currently recognized by SQLAlchemy itself
        include all those listed under :meth:`.Executable.execution_options`,
        as well as others that are specific to :class:`_engine.Connection`.

        :param autocommit: Available on: Connection, statement.
          When True, a COMMIT will be invoked after execution
          when executed in 'autocommit' mode, i.e. when an explicit
          transaction is not begun on the connection.   Note that this
          is **library level, not DBAPI level autocommit**.  The DBAPI
          connection will remain in a real transaction unless the
          "AUTOCOMMIT" isolation level is used.

          .. deprecated:: 1.4  The "autocommit" execution option is deprecated
             and will be removed in SQLAlchemy 2.0.  See
             :ref:`migration_20_autocommit` for discussion.

        :param compiled_cache: Available on: Connection.
          A dictionary where :class:`.Compiled` objects
          will be cached when the :class:`_engine.Connection`
          compiles a clause
          expression into a :class:`.Compiled` object.  This dictionary will
          supersede the statement cache that may be configured on the
          :class:`_engine.Engine` itself.   If set to None, caching
          is disabled, even if the engine has a configured cache size.

          Note that the ORM makes use of its own "compiled" caches for
          some operations, including flush operations.  The caching
          used by the ORM internally supersedes a cache dictionary
          specified here.

        :param logging_token: Available on: :class:`_engine.Connection`,
          :class:`_engine.Engine`.

          Adds the specified string token surrounded by brackets in log
          messages logged by the connection, i.e. the logging that's enabled
          either via the :paramref:`_sa.create_engine.echo` flag or via the
          ``logging.getLogger("sqlalchemy.engine")`` logger. This allows a
          per-connection or per-sub-engine token to be available which is
          useful for debugging concurrent connection scenarios.

          .. versionadded:: 1.4.0b2

          .. seealso::

            :ref:`dbengine_logging_tokens` - usage example

            :paramref:`_sa.create_engine.logging_name` - adds a name to the
            name used by the Python logger object itself.

        :param isolation_level: Available on: :class:`_engine.Connection`.

          Set the transaction isolation level for the lifespan of this
          :class:`_engine.Connection` object.
          Valid values include those string
          values accepted by the :paramref:`_sa.create_engine.isolation_level`
          parameter passed to :func:`_sa.create_engine`.  These levels are
          semi-database specific; see individual dialect documentation for
          valid levels.

          The isolation level option applies the isolation level by emitting
          statements on the  DBAPI connection, and **necessarily affects the
          original Connection object overall**, not just the copy that is
          returned by the call to :meth:`_engine.Connection.execution_options`
          method.  The isolation level will remain at the given setting until
          the DBAPI connection itself is returned to the connection pool, i.e.
          the :meth:`_engine.Connection.close` method on the original
          :class:`_engine.Connection` is called,
          where  an event handler will emit
          additional statements on the DBAPI connection in order to revert the
          isolation level change.

          .. warning::  The ``isolation_level`` execution option should
             **not** be used when a transaction is already established, that
             is, the :meth:`_engine.Connection.begin`
             method or similar has been
             called.  A database cannot change the isolation level on a
             transaction in progress, and different DBAPIs and/or
             SQLAlchemy dialects may implicitly roll back or commit
             the transaction, or not affect the connection at all.

          .. note:: The ``isolation_level`` execution option is implicitly
             reset if the :class:`_engine.Connection` is invalidated, e.g. via
             the :meth:`_engine.Connection.invalidate` method, or if a
             disconnection error occurs.  The new connection produced after
             the invalidation will not have the isolation level re-applied
             to it automatically.

          .. seealso::

                :paramref:`_sa.create_engine.isolation_level`
                - set per :class:`_engine.Engine` isolation level

                :meth:`_engine.Connection.get_isolation_level`
                - view current level

                :ref:`SQLite Transaction Isolation <sqlite_isolation_level>`

                :ref:`PostgreSQL Transaction Isolation <postgresql_isolation_level>`

                :ref:`MySQL Transaction Isolation <mysql_isolation_level>`

                :ref:`SQL Server Transaction Isolation <mssql_isolation_level>`

                :ref:`session_transaction_isolation` - for the ORM

        :param no_parameters: When ``True``, if the final parameter
          list or dictionary is totally empty, will invoke the
          statement on the cursor as ``cursor.execute(statement)``,
          not passing the parameter collection at all.
          Some DBAPIs such as psycopg2 and mysql-python consider
          percent signs as significant only when parameters are
          present; this option allows code to generate SQL
          containing percent signs (and possibly other characters)
          that is neutral regarding whether it's executed by the DBAPI
          or piped into a script that's later invoked by
          command line tools.

        :param stream_results: Available on: Connection, statement.
          Indicate to the dialect that results should be
          "streamed" and not pre-buffered, if possible.  This is a limitation
          of many DBAPIs.  The flag is currently understood within a subset
          of dialects within the PostgreSQL and MySQL categories, and
          may be supported by other third party dialects as well.

          .. seealso::

            :ref:`engine_stream_results`

        :param schema_translate_map: Available on: Connection, Engine.
          A dictionary mapping schema names to schema names, that will be
          applied to the :paramref:`_schema.Table.schema` element of each
          :class:`_schema.Table`
          encountered when SQL or DDL expression elements
          are compiled into strings; the resulting schema name will be
          converted based on presence in the map of the original name.

          .. versionadded:: 1.1

          .. seealso::

            :ref:`schema_translating`

        .. seealso::

            :meth:`_engine.Engine.execution_options`

            :meth:`.Executable.execution_options`

            :meth:`_engine.Connection.get_execution_options`


        """  # noqa
        c = self._generate_for_options()
        c._execution_options = c._execution_options.union(opt)
        if self._has_events or self.engine._has_events:
            self.dispatch.set_connection_execution_options(c, opt)
        self.dialect.set_connection_execution_options(c, opt)
        return c

    def get_execution_options(self):
        """Get the non-SQL options which will take effect during execution.

        .. versionadded:: 1.3

        .. seealso::

            :meth:`_engine.Connection.execution_options`
        """
        return self._execution_options

    @property
    def closed(self):
        """Return True if this connection is closed."""

        # note this is independent for a "branched" connection vs.
        # the base

        return self._dbapi_connection is None and not self.__can_reconnect

    @property
    def invalidated(self):
        """Return True if this connection was invalidated."""

        # prior to 1.4, "invalid" was stored as a state independent of
        # "closed", meaning an invalidated connection could be "closed",
        # the _dbapi_connection would be None and closed=True, yet the
        # "invalid" flag would stay True.  This meant that there were
        # three separate states (open/valid, closed/valid, closed/invalid)
        # when there is really no reason for that; a connection that's
        # "closed" does not need to be "invalid".  So the state is now
        # represented by the two facts alone.

        if self.__branch_from:
            return self.__branch_from.invalidated

        return self._dbapi_connection is None and not self.closed

    @property
    def connection(self):
        """The underlying DB-API connection managed by this Connection.

        .. seealso::


            :ref:`dbapi_connections`

        """

        if self._dbapi_connection is None:
            try:
                return self._revalidate_connection()
            except (exc.PendingRollbackError, exc.ResourceClosedError):
                raise
            except BaseException as e:
                self._handle_dbapi_exception(e, None, None, None, None)
        else:
            return self._dbapi_connection

    def get_isolation_level(self):
        """Return the current isolation level assigned to this
        :class:`_engine.Connection`.

        This will typically be the default isolation level as determined
        by the dialect, unless if the
        :paramref:`.Connection.execution_options.isolation_level`
        feature has been used to alter the isolation level on a
        per-:class:`_engine.Connection` basis.

        This attribute will typically perform a live SQL operation in order
        to procure the current isolation level, so the value returned is the
        actual level on the underlying DBAPI connection regardless of how
        this state was set.  Compare to the
        :attr:`_engine.Connection.default_isolation_level` accessor
        which returns the dialect-level setting without performing a SQL
        query.

        .. versionadded:: 0.9.9

        .. seealso::

            :attr:`_engine.Connection.default_isolation_level`
            - view default level

            :paramref:`_sa.create_engine.isolation_level`
            - set per :class:`_engine.Engine` isolation level

            :paramref:`.Connection.execution_options.isolation_level`
            - set per :class:`_engine.Connection` isolation level

        """
        try:
            return self.dialect.get_isolation_level(self.connection)
        except BaseException as e:
            self._handle_dbapi_exception(e, None, None, None, None)

    @property
    def default_isolation_level(self):
        """The default isolation level assigned to this
        :class:`_engine.Connection`.

        This is the isolation level setting that the
        :class:`_engine.Connection`
        has when first procured via the :meth:`_engine.Engine.connect` method.
        This level stays in place until the
        :paramref:`.Connection.execution_options.isolation_level` is used
        to change the setting on a per-:class:`_engine.Connection` basis.

        Unlike :meth:`_engine.Connection.get_isolation_level`,
        this attribute is set
        ahead of time from the first connection procured by the dialect,
        so SQL query is not invoked when this accessor is called.

        .. versionadded:: 0.9.9

        .. seealso::

            :meth:`_engine.Connection.get_isolation_level`
            - view current level

            :paramref:`_sa.create_engine.isolation_level`
            - set per :class:`_engine.Engine` isolation level

            :paramref:`.Connection.execution_options.isolation_level`
            - set per :class:`_engine.Connection` isolation level

        """
        return self.dialect.default_isolation_level

    def _invalid_transaction(self):
        if self.invalidated:
            raise exc.PendingRollbackError(
                "Can't reconnect until invalid %stransaction is rolled "
                "back."
                % (
                    "savepoint "
                    if self._nested_transaction is not None
                    else ""
                ),
                code="8s2b",
            )
        else:
            assert not self._is_future
            raise exc.PendingRollbackError(
                "This connection is on an inactive %stransaction.  "
                "Please rollback() fully before proceeding."
                % (
                    "savepoint "
                    if self._nested_transaction is not None
                    else ""
                ),
                code="8s2a",
            )

    def _revalidate_connection(self):
        if self.__branch_from:
            return self.__branch_from._revalidate_connection()
        if self.__can_reconnect and self.invalidated:
            if self._transaction is not None:
                self._invalid_transaction()
            self._dbapi_connection = self.engine.raw_connection(
                _connection=self
            )
            return self._dbapi_connection
        raise exc.ResourceClosedError("This Connection is closed")

    @property
    def _still_open_and_dbapi_connection_is_valid(self):
        return self._dbapi_connection is not None and getattr(
            self._dbapi_connection, "is_valid", False
        )

    @property
    def info(self):
        """Info dictionary associated with the underlying DBAPI connection
        referred to by this :class:`_engine.Connection`, allowing user-defined
        data to be associated with the connection.

        The data here will follow along with the DBAPI connection including
        after it is returned to the connection pool and used again
        in subsequent instances of :class:`_engine.Connection`.

        """

        return self.connection.info

    @util.deprecated_20(":meth:`.Connection.connect`")
    def connect(self, close_with_result=False):
        """Returns a branched version of this :class:`_engine.Connection`.

        The :meth:`_engine.Connection.close` method on the returned
        :class:`_engine.Connection` can be called and this
        :class:`_engine.Connection` will remain open.

        This method provides usage symmetry with
        :meth:`_engine.Engine.connect`, including for usage
        with context managers.

        """

        return self._branch()

    def invalidate(self, exception=None):
        """Invalidate the underlying DBAPI connection associated with
        this :class:`_engine.Connection`.

        An attempt will be made to close the underlying DBAPI connection
        immediately; however if this operation fails, the error is logged
        but not raised.  The connection is then discarded whether or not
        close() succeeded.

        Upon the next use (where "use" typically means using the
        :meth:`_engine.Connection.execute` method or similar),
        this :class:`_engine.Connection` will attempt to
        procure a new DBAPI connection using the services of the
        :class:`_pool.Pool` as a source of connectivity (e.g.
        a "reconnection").

        If a transaction was in progress (e.g. the
        :meth:`_engine.Connection.begin` method has been called) when
        :meth:`_engine.Connection.invalidate` method is called, at the DBAPI
        level all state associated with this transaction is lost, as
        the DBAPI connection is closed.  The :class:`_engine.Connection`
        will not allow a reconnection to proceed until the
        :class:`.Transaction` object is ended, by calling the
        :meth:`.Transaction.rollback` method; until that point, any attempt at
        continuing to use the :class:`_engine.Connection` will raise an
        :class:`~sqlalchemy.exc.InvalidRequestError`.
        This is to prevent applications from accidentally
        continuing an ongoing transactional operations despite the
        fact that the transaction has been lost due to an
        invalidation.

        The :meth:`_engine.Connection.invalidate` method,
        just like auto-invalidation,
        will at the connection pool level invoke the
        :meth:`_events.PoolEvents.invalidate` event.

        :param exception: an optional ``Exception`` instance that's the
         reason for the invalidation.  is passed along to event handlers
         and logging functions.

        .. seealso::

            :ref:`pool_connection_invalidation`

        """

        if self.__branch_from:
            return self.__branch_from.invalidate(exception=exception)

        if self.invalidated:
            return

        if self.closed:
            raise exc.ResourceClosedError("This Connection is closed")

        if self._still_open_and_dbapi_connection_is_valid:
            self._dbapi_connection.invalidate(exception)
        self._dbapi_connection = None

    def detach(self):
        """Detach the underlying DB-API connection from its connection pool.

        E.g.::

            with engine.connect() as conn:
                conn.detach()
                conn.execute(text("SET search_path TO schema1, schema2"))

                # work with connection

            # connection is fully closed (since we used "with:", can
            # also call .close())

        This :class:`_engine.Connection` instance will remain usable.
        When closed
        (or exited from a context manager context as above),
        the DB-API connection will be literally closed and not
        returned to its originating pool.

        This method can be used to insulate the rest of an application
        from a modified state on a connection (such as a transaction
        isolation level or similar).

        """

        self._dbapi_connection.detach()

    def _autobegin(self):
        self.begin()

    def begin(self):
        """Begin a transaction and return a transaction handle.

        The returned object is an instance of :class:`.Transaction`.
        This object represents the "scope" of the transaction,
        which completes when either the :meth:`.Transaction.rollback`
        or :meth:`.Transaction.commit` method is called.

        .. tip::

            The :meth:`_engine.Connection.begin` method is invoked when using
            the :meth:`_engine.Engine.begin` context manager method as well.
            All documentation that refers to behaviors specific to the
            :meth:`_engine.Connection.begin` method also apply to use of the
            :meth:`_engine.Engine.begin` method.

        Legacy use: nested calls to :meth:`.begin` on the same
        :class:`_engine.Connection` will return new :class:`.Transaction`
        objects that represent an emulated transaction within the scope of the
        enclosing transaction, that is::

            trans = conn.begin()   # outermost transaction
            trans2 = conn.begin()  # "nested"
            trans2.commit()        # does nothing
            trans.commit()         # actually commits

        Calls to :meth:`.Transaction.commit` only have an effect
        when invoked via the outermost :class:`.Transaction` object, though the
        :meth:`.Transaction.rollback` method of any of the
        :class:`.Transaction` objects will roll back the
        transaction.

        .. tip::

            The above "nesting" behavior is a legacy behavior specific to
            :term:`1.x style` use and will be removed in SQLAlchemy 2.0. For
            notes on :term:`2.0 style` use, see
            :meth:`_future.Connection.begin`.


        .. seealso::

            :meth:`_engine.Connection.begin_nested` - use a SAVEPOINT

            :meth:`_engine.Connection.begin_twophase` -
            use a two phase /XID transaction

            :meth:`_engine.Engine.begin` - context manager available from
            :class:`_engine.Engine`

        """
        if self._is_future:
            assert not self.__branch_from
        elif self.__branch_from:
            return self.__branch_from.begin()

        if self.__in_begin:
            # for dialects that emit SQL within the process of
            # dialect.do_begin() or dialect.do_begin_twophase(), this
            # flag prevents "autobegin" from being emitted within that
            # process, while allowing self._transaction to remain at None
            # until it's complete.
            return
        elif self._transaction is None:
            self._transaction = RootTransaction(self)
            return self._transaction
        else:
            if self._is_future:
                raise exc.InvalidRequestError(
                    "a transaction is already begun for this connection"
                )
            else:
                return MarkerTransaction(self)

    def begin_nested(self):
        """Begin a nested transaction (i.e. SAVEPOINT) and return a
        transaction handle, assuming an outer transaction is already
        established.

        Nested transactions require SAVEPOINT support in the
        underlying database.  Any transaction in the hierarchy may
        ``commit`` and ``rollback``, however the outermost transaction
        still controls the overall ``commit`` or ``rollback`` of the
        transaction of a whole.

        The legacy form of :meth:`_engine.Connection.begin_nested` method has
        alternate behaviors based on whether or not the
        :meth:`_engine.Connection.begin` method was called previously. If
        :meth:`_engine.Connection.begin` was not called, then this method will
        behave the same as the :meth:`_engine.Connection.begin` method and
        return a :class:`.RootTransaction` object that begins and commits a
        real transaction - **no savepoint is invoked**. If
        :meth:`_engine.Connection.begin` **has** been called, and a
        :class:`.RootTransaction` is already established, then this method
        returns an instance of :class:`.NestedTransaction` which will invoke
        and manage the scope of a SAVEPOINT.

        .. tip::

            The above mentioned behavior of
            :meth:`_engine.Connection.begin_nested` is a legacy behavior
            specific to :term:`1.x style` use. In :term:`2.0 style` use, the
            :meth:`_future.Connection.begin_nested` method instead autobegins
            the outer transaction that can be committed using
            "commit-as-you-go" style; see
            :meth:`_future.Connection.begin_nested` for migration details.

        .. versionchanged:: 1.4.13 The behavior of
           :meth:`_engine.Connection.begin_nested`
           as returning a :class:`.RootTransaction` if
           :meth:`_engine.Connection.begin` were not called has been restored
           as was the case in 1.3.x versions; in previous 1.4.x versions, an
           outer transaction would be "autobegun" but would not be committed.


        .. seealso::

            :meth:`_engine.Connection.begin`

            :meth:`_engine.Connection.begin_twophase`

        """
        if self._is_future:
            assert not self.__branch_from
        elif self.__branch_from:
            return self.__branch_from.begin_nested()

        if self._transaction is None:
            if not self._is_future:
                util.warn_deprecated_20(
                    "Calling Connection.begin_nested() in 2.0 style use will "
                    "return a NestedTransaction (SAVEPOINT) in all cases, "
                    "that will not commit the outer transaction.  For code "
                    "that is cross-compatible between 1.x and 2.0 style use, "
                    "ensure Connection.begin() is called before calling "
                    "Connection.begin_nested()."
                )
                return self.begin()
            else:
                self._autobegin()

        return NestedTransaction(self)

    def begin_twophase(self, xid=None):
        """Begin a two-phase or XA transaction and return a transaction
        handle.

        The returned object is an instance of :class:`.TwoPhaseTransaction`,
        which in addition to the methods provided by
        :class:`.Transaction`, also provides a
        :meth:`~.TwoPhaseTransaction.prepare` method.

        :param xid: the two phase transaction id.  If not supplied, a
          random id will be generated.

        .. seealso::

            :meth:`_engine.Connection.begin`

            :meth:`_engine.Connection.begin_twophase`

        """

        if self.__branch_from:
            return self.__branch_from.begin_twophase(xid=xid)

        if self._transaction is not None:
            raise exc.InvalidRequestError(
                "Cannot start a two phase transaction when a transaction "
                "is already in progress."
            )
        if xid is None:
            xid = self.engine.dialect.create_xid()
        return TwoPhaseTransaction(self, xid)

    def recover_twophase(self):
        return self.engine.dialect.do_recover_twophase(self)

    def rollback_prepared(self, xid, recover=False):
        self.engine.dialect.do_rollback_twophase(self, xid, recover=recover)

    def commit_prepared(self, xid, recover=False):
        self.engine.dialect.do_commit_twophase(self, xid, recover=recover)

    def in_transaction(self):
        """Return True if a transaction is in progress."""
        if self.__branch_from is not None:
            return self.__branch_from.in_transaction()

        return self._transaction is not None and self._transaction.is_active

    def in_nested_transaction(self):
        """Return True if a transaction is in progress."""
        if self.__branch_from is not None:
            return self.__branch_from.in_nested_transaction()

        return (
            self._nested_transaction is not None
            and self._nested_transaction.is_active
        )

    def _is_autocommit(self):
        return (
            self._execution_options.get("isolation_level", None)
            == "AUTOCOMMIT"
        )

    def get_transaction(self):
        """Return the current root transaction in progress, if any.

        .. versionadded:: 1.4

        """

        if self.__branch_from is not None:
            return self.__branch_from.get_transaction()

        return self._transaction

    def get_nested_transaction(self):
        """Return the current nested transaction in progress, if any.

        .. versionadded:: 1.4

        """
        if self.__branch_from is not None:

            return self.__branch_from.get_nested_transaction()

        return self._nested_transaction

    def _begin_impl(self, transaction):
        assert not self.__branch_from

        if self._echo:
            self._log_info("BEGIN (implicit)")

        self.__in_begin = True

        if self._has_events or self.engine._has_events:
            self.dispatch.begin(self)

        try:
            self.engine.dialect.do_begin(self.connection)
        except BaseException as e:
            self._handle_dbapi_exception(e, None, None, None, None)
        finally:
            self.__in_begin = False

    def _rollback_impl(self):
        assert not self.__branch_from

        if self._has_events or self.engine._has_events:
            self.dispatch.rollback(self)

        if self._still_open_and_dbapi_connection_is_valid:
            if self._echo:
                if self._is_autocommit():
                    self._log_info(
                        "ROLLBACK using DBAPI connection.rollback(), "
                        "DBAPI should ignore due to autocommit mode"
                    )
                else:
                    self._log_info("ROLLBACK")
            try:
                self.engine.dialect.do_rollback(self.connection)
            except BaseException as e:
                self._handle_dbapi_exception(e, None, None, None, None)

    def _commit_impl(self, autocommit=False):
        assert not self.__branch_from

        # AUTOCOMMIT isolation-level is a dialect-specific concept, however
        # if a connection has this set as the isolation level, we can skip
        # the "autocommit" warning as the operation will do "autocommit"
        # in any case
        if autocommit and not self._is_autocommit():
            util.warn_deprecated_20(
                "The current statement is being autocommitted using "
                "implicit autocommit, which will be removed in "
                "SQLAlchemy 2.0. "
                "Use the .begin() method of Engine or Connection in order to "
                "use an explicit transaction for DML and DDL statements."
            )

        if self._has_events or self.engine._has_events:
            self.dispatch.commit(self)

        if self._echo:
            if self._is_autocommit():
                self._log_info(
                    "COMMIT using DBAPI connection.commit(), "
                    "DBAPI should ignore due to autocommit mode"
                )
            else:
                self._log_info("COMMIT")
        try:
            self.engine.dialect.do_commit(self.connection)
        except BaseException as e:
            self._handle_dbapi_exception(e, None, None, None, None)

    def _savepoint_impl(self, name=None):
        assert not self.__branch_from

        if self._has_events or self.engine._has_events:
            self.dispatch.savepoint(self, name)

        if name is None:
            self.__savepoint_seq += 1
            name = "sa_savepoint_%s" % self.__savepoint_seq
        if self._still_open_and_dbapi_connection_is_valid:
            self.engine.dialect.do_savepoint(self, name)
            return name

    def _rollback_to_savepoint_impl(self, name):
        assert not self.__branch_from

        if self._has_events or self.engine._has_events:
            self.dispatch.rollback_savepoint(self, name, None)

        if self._still_open_and_dbapi_connection_is_valid:
            self.engine.dialect.do_rollback_to_savepoint(self, name)

    def _release_savepoint_impl(self, name):
        assert not self.__branch_from

        if self._has_events or self.engine._has_events:
            self.dispatch.release_savepoint(self, name, None)

        if self._still_open_and_dbapi_connection_is_valid:
            self.engine.dialect.do_release_savepoint(self, name)

    def _begin_twophase_impl(self, transaction):
        assert not self.__branch_from

        if self._echo:
            self._log_info("BEGIN TWOPHASE (implicit)")
        if self._has_events or self.engine._has_events:
            self.dispatch.begin_twophase(self, transaction.xid)

        if self._still_open_and_dbapi_connection_is_valid:
            self.__in_begin = True
            try:
                self.engine.dialect.do_begin_twophase(self, transaction.xid)
            except BaseException as e:
                self._handle_dbapi_exception(e, None, None, None, None)
            finally:
                self.__in_begin = False

    def _prepare_twophase_impl(self, xid):
        assert not self.__branch_from

        if self._has_events or self.engine._has_events:
            self.dispatch.prepare_twophase(self, xid)

        if self._still_open_and_dbapi_connection_is_valid:
            assert isinstance(self._transaction, TwoPhaseTransaction)
            try:
                self.engine.dialect.do_prepare_twophase(self, xid)
            except BaseException as e:
                self._handle_dbapi_exception(e, None, None, None, None)

    def _rollback_twophase_impl(self, xid, is_prepared):
        assert not self.__branch_from

        if self._has_events or self.engine._has_events:
            self.dispatch.rollback_twophase(self, xid, is_prepared)

        if self._still_open_and_dbapi_connection_is_valid:
            assert isinstance(self._transaction, TwoPhaseTransaction)
            try:
                self.engine.dialect.do_rollback_twophase(
                    self, xid, is_prepared
                )
            except BaseException as e:
                self._handle_dbapi_exception(e, None, None, None, None)

    def _commit_twophase_impl(self, xid, is_prepared):
        assert not self.__branch_from

        if self._has_events or self.engine._has_events:
            self.dispatch.commit_twophase(self, xid, is_prepared)

        if self._still_open_and_dbapi_connection_is_valid:
            assert isinstance(self._transaction, TwoPhaseTransaction)
            try:
                self.engine.dialect.do_commit_twophase(self, xid, is_prepared)
            except BaseException as e:
                self._handle_dbapi_exception(e, None, None, None, None)

    def _autorollback(self):
        if self.__branch_from:
            self.__branch_from._autorollback()

        if not self.in_transaction():
            self._rollback_impl()

    def _warn_for_legacy_exec_format(self):
        util.warn_deprecated_20(
            "The connection.execute() method in "
            "SQLAlchemy 2.0 will accept parameters as a single "
            "dictionary or a "
            "single sequence of dictionaries only. "
            "Parameters passed as keyword arguments, tuples or positionally "
            "oriented dictionaries and/or tuples "
            "will no longer be accepted."
        )

    def close(self):
        """Close this :class:`_engine.Connection`.

        This results in a release of the underlying database
        resources, that is, the DBAPI connection referenced
        internally. The DBAPI connection is typically restored
        back to the connection-holding :class:`_pool.Pool` referenced
        by the :class:`_engine.Engine` that produced this
        :class:`_engine.Connection`. Any transactional state present on
        the DBAPI connection is also unconditionally released via
        the DBAPI connection's ``rollback()`` method, regardless
        of any :class:`.Transaction` object that may be
        outstanding with regards to this :class:`_engine.Connection`.

        After :meth:`_engine.Connection.close` is called, the
        :class:`_engine.Connection` is permanently in a closed state,
        and will allow no further operations.

        """

        if self.__branch_from:
            assert not self._is_future
            util.warn_deprecated_20(
                "The .close() method on a so-called 'branched' connection is "
                "deprecated as of 1.4, as are 'branched' connections overall, "
                "and will be removed in a future release.  If this is a "
                "default-handling function, don't close the connection."
            )
            self._dbapi_connection = None
            self.__can_reconnect = False
            return

        if self._transaction:
            self._transaction.close()
            skip_reset = True
        else:
            skip_reset = False

        if self._dbapi_connection is not None:
            conn = self._dbapi_connection

            # as we just closed the transaction, close the connection
            # pool connection without doing an additional reset
            if skip_reset:
                conn._close_no_reset()
            else:
                conn.close()

            # There is a slight chance that conn.close() may have
            # triggered an invalidation here in which case
            # _dbapi_connection would already be None, however usually
            # it will be non-None here and in a "closed" state.
            self._dbapi_connection = None
        self.__can_reconnect = False

    def scalar(self, object_, *multiparams, **params):
        """Executes and returns the first column of the first row.

        The underlying result/cursor is closed after execution.
        """

        return self.execute(object_, *multiparams, **params).scalar()

    def execute(self, statement, *multiparams, **params):
        r"""Executes a SQL statement construct and returns a
        :class:`_engine.CursorResult`.

        :param statement: The statement to be executed.  May be
         one of:

         * a plain string (deprecated)
         * any :class:`_expression.ClauseElement` construct that is also
           a subclass of :class:`.Executable`, such as a
           :func:`_expression.select` construct
         * a :class:`.FunctionElement`, such as that generated
           by :data:`.func`, will be automatically wrapped in
           a SELECT statement, which is then executed.
         * a :class:`.DDLElement` object
         * a :class:`.DefaultGenerator` object
         * a :class:`.Compiled` object

         .. deprecated:: 2.0 passing a string to
            :meth:`_engine.Connection.execute` is
            deprecated and will be removed in version 2.0.  Use the
            :func:`_expression.text` construct with
            :meth:`_engine.Connection.execute`, or the
            :meth:`_engine.Connection.exec_driver_sql`
            method to invoke a driver-level
            SQL string.

        :param \*multiparams/\**params: represent bound parameter
         values to be used in the execution.   Typically,
         the format is either a collection of one or more
         dictionaries passed to \*multiparams::

             conn.execute(
                 table.insert(),
                 {"id":1, "value":"v1"},
                 {"id":2, "value":"v2"}
             )

         ...or individual key/values interpreted by \**params::

             conn.execute(
                 table.insert(), id=1, value="v1"
             )

         In the case that a plain SQL string is passed, and the underlying
         DBAPI accepts positional bind parameters, a collection of tuples
         or individual values in \*multiparams may be passed::

             conn.execute(
                 "INSERT INTO table (id, value) VALUES (?, ?)",
                 (1, "v1"), (2, "v2")
             )

             conn.execute(
                 "INSERT INTO table (id, value) VALUES (?, ?)",
                 1, "v1"
             )

         Note above, the usage of a question mark "?" or other
         symbol is contingent upon the "paramstyle" accepted by the DBAPI
         in use, which may be any of "qmark", "named", "pyformat", "format",
         "numeric".   See `pep-249
         <https://www.python.org/dev/peps/pep-0249/>`_ for details on
         paramstyle.

         To execute a textual SQL statement which uses bound parameters in a
         DBAPI-agnostic way, use the :func:`_expression.text` construct.

         .. deprecated:: 2.0 use of tuple or scalar positional parameters
            is deprecated. All params should be dicts or sequences of dicts.
            Use :meth:`.exec_driver_sql` to execute a plain string with
            tuple or scalar positional parameters.

        """

        if isinstance(statement, util.string_types):
            util.warn_deprecated_20(
                "Passing a string to Connection.execute() is "
                "deprecated and will be removed in version 2.0.  Use the "
                "text() construct, "
                "or the Connection.exec_driver_sql() method to invoke a "
                "driver-level SQL string."
            )

            return self._exec_driver_sql(
                statement,
                multiparams,
                params,
                _EMPTY_EXECUTION_OPTS,
                future=False,
            )

        try:
            meth = statement._execute_on_connection
        except AttributeError as err:
            util.raise_(
                exc.ObjectNotExecutableError(statement), replace_context=err
            )
        else:
            return meth(self, multiparams, params, _EMPTY_EXECUTION_OPTS)

    def _execute_function(self, func, multiparams, params, execution_options):
        """Execute a sql.FunctionElement object."""

        return self._execute_clauseelement(
            func.select(), multiparams, params, execution_options
        )

    def _execute_default(
        self,
        default,
        multiparams,
        params,
        # migrate is calling this directly :(
        execution_options=_EMPTY_EXECUTION_OPTS,
    ):
        """Execute a schema.ColumnDefault object."""

        execution_options = self._execution_options.merge_with(
            execution_options
        )

        distilled_parameters = _distill_params(self, multiparams, params)

        if self._has_events or self.engine._has_events:
            (
                distilled_params,
                event_multiparams,
                event_params,
            ) = self._invoke_before_exec_event(
                default, distilled_parameters, execution_options
            )

        try:
            conn = self._dbapi_connection
            if conn is None:
                conn = self._revalidate_connection()

            dialect = self.dialect
            ctx = dialect.execution_ctx_cls._init_default(
                dialect, self, conn, execution_options
            )
        except (exc.PendingRollbackError, exc.ResourceClosedError):
            raise
        except BaseException as e:
            self._handle_dbapi_exception(e, None, None, None, None)

        ret = ctx._exec_default(None, default, None)
        if self.should_close_with_result:
            self.close()

        if self._has_events or self.engine._has_events:
            self.dispatch.after_execute(
                self,
                default,
                event_multiparams,
                event_params,
                execution_options,
                ret,
            )

        return ret

    def _execute_ddl(self, ddl, multiparams, params, execution_options):
        """Execute a schema.DDL object."""

        execution_options = ddl._execution_options.merge_with(
            self._execution_options, execution_options
        )

        distilled_parameters = _distill_params(self, multiparams, params)

        if self._has_events or self.engine._has_events:
            (
                distilled_params,
                event_multiparams,
                event_params,
            ) = self._invoke_before_exec_event(
                ddl, distilled_parameters, execution_options
            )

        exec_opts = self._execution_options.merge_with(execution_options)
        schema_translate_map = exec_opts.get("schema_translate_map", None)

        dialect = self.dialect

        compiled = ddl.compile(
            dialect=dialect, schema_translate_map=schema_translate_map
        )
        ret = self._execute_context(
            dialect,
            dialect.execution_ctx_cls._init_ddl,
            compiled,
            None,
            execution_options,
            compiled,
        )
        if self._has_events or self.engine._has_events:
            self.dispatch.after_execute(
                self,
                ddl,
                event_multiparams,
                event_params,
                execution_options,
                ret,
            )
        return ret

    def _invoke_before_exec_event(
        self, elem, distilled_params, execution_options
    ):

        if len(distilled_params) == 1:
            event_multiparams, event_params = [], distilled_params[0]
        else:
            event_multiparams, event_params = distilled_params, {}

        for fn in self.dispatch.before_execute:
            elem, event_multiparams, event_params = fn(
                self,
                elem,
                event_multiparams,
                event_params,
                execution_options,
            )

        if event_multiparams:
            distilled_params = list(event_multiparams)
            if event_params:
                raise exc.InvalidRequestError(
                    "Event handler can't return non-empty multiparams "
                    "and params at the same time"
                )
        elif event_params:
            distilled_params = [event_params]
        else:
            distilled_params = []

        return distilled_params, event_multiparams, event_params

    def _execute_clauseelement(
        self, elem, multiparams, params, execution_options
    ):
        """Execute a sql.ClauseElement object."""

        execution_options = elem._execution_options.merge_with(
            self._execution_options, execution_options
        )

        distilled_params = _distill_params(self, multiparams, params)

        has_events = self._has_events or self.engine._has_events
        if has_events:
            (
                distilled_params,
                event_multiparams,
                event_params,
            ) = self._invoke_before_exec_event(
                elem, distilled_params, execution_options
            )

        if distilled_params:
            # ensure we don't retain a link to the view object for keys()
            # which links to the values, which we don't want to cache
            keys = sorted(distilled_params[0])
            for_executemany = len(distilled_params) > 1
        else:
            keys = []
            for_executemany = False

        dialect = self.dialect

        schema_translate_map = execution_options.get(
            "schema_translate_map", None
        )

        compiled_cache = execution_options.get(
            "compiled_cache", self.engine._compiled_cache
        )

        compiled_sql, extracted_params, cache_hit = elem._compile_w_cache(
            dialect=dialect,
            compiled_cache=compiled_cache,
            column_keys=keys,
            for_executemany=for_executemany,
            schema_translate_map=schema_translate_map,
            linting=self.dialect.compiler_linting | compiler.WARN_LINTING,
        )
        ret = self._execute_context(
            dialect,
            dialect.execution_ctx_cls._init_compiled,
            compiled_sql,
            distilled_params,
            execution_options,
            compiled_sql,
            distilled_params,
            elem,
            extracted_params,
            cache_hit=cache_hit,
        )
        if has_events:
            self.dispatch.after_execute(
                self,
                elem,
                event_multiparams,
                event_params,
                execution_options,
                ret,
            )
        return ret

    def _execute_compiled(
        self,
        compiled,
        multiparams,
        params,
        execution_options=_EMPTY_EXECUTION_OPTS,
    ):
        """Execute a sql.Compiled object.

        TODO: why do we have this?   likely deprecate or remove

        """

        execution_options = compiled.execution_options.merge_with(
            self._execution_options, execution_options
        )
        distilled_parameters = _distill_params(self, multiparams, params)

        if self._has_events or self.engine._has_events:
            (
                distilled_params,
                event_multiparams,
                event_params,
            ) = self._invoke_before_exec_event(
                compiled, distilled_parameters, execution_options
            )

        dialect = self.dialect

        ret = self._execute_context(
            dialect,
            dialect.execution_ctx_cls._init_compiled,
            compiled,
            distilled_parameters,
            execution_options,
            compiled,
            distilled_parameters,
            None,
            None,
        )
        if self._has_events or self.engine._has_events:
            self.dispatch.after_execute(
                self,
                compiled,
                event_multiparams,
                event_params,
                execution_options,
                ret,
            )
        return ret

    def _exec_driver_sql(
        self, statement, multiparams, params, execution_options, future
    ):

        execution_options = self._execution_options.merge_with(
            execution_options
        )

        distilled_parameters = _distill_params(self, multiparams, params)

        if not future:
            if self._has_events or self.engine._has_events:
                (
                    distilled_params,
                    event_multiparams,
                    event_params,
                ) = self._invoke_before_exec_event(
                    statement, distilled_parameters, execution_options
                )

        dialect = self.dialect
        ret = self._execute_context(
            dialect,
            dialect.execution_ctx_cls._init_statement,
            statement,
            distilled_parameters,
            execution_options,
            statement,
            distilled_parameters,
        )

        if not future:
            if self._has_events or self.engine._has_events:
                self.dispatch.after_execute(
                    self,
                    statement,
                    event_multiparams,
                    event_params,
                    execution_options,
                    ret,
                )
        return ret

    def _execute_20(
        self,
        statement,
        parameters=None,
        execution_options=_EMPTY_EXECUTION_OPTS,
    ):
        args_10style, kwargs_10style = _distill_params_20(parameters)
        try:
            meth = statement._execute_on_connection
        except AttributeError as err:
            util.raise_(
                exc.ObjectNotExecutableError(statement), replace_context=err
            )
        else:
            return meth(self, args_10style, kwargs_10style, execution_options)

    def exec_driver_sql(
        self, statement, parameters=None, execution_options=None
    ):
        r"""Executes a SQL statement construct and returns a
        :class:`_engine.CursorResult`.

        :param statement: The statement str to be executed.   Bound parameters
         must use the underlying DBAPI's paramstyle, such as "qmark",
         "pyformat", "format", etc.

        :param parameters: represent bound parameter values to be used in the
         execution.  The format is one of:   a dictionary of named parameters,
         a tuple of positional parameters, or a list containing either
         dictionaries or tuples for multiple-execute support.

         E.g. multiple dictionaries::


             conn.exec_driver_sql(
                 "INSERT INTO table (id, value) VALUES (%(id)s, %(value)s)",
                 [{"id":1, "value":"v1"}, {"id":2, "value":"v2"}]
             )

         Single dictionary::

             conn.exec_driver_sql(
                 "INSERT INTO table (id, value) VALUES (%(id)s, %(value)s)",
                 dict(id=1, value="v1")
             )

         Single tuple::

             conn.exec_driver_sql(
                 "INSERT INTO table (id, value) VALUES (?, ?)",
                 (1, 'v1')
             )

         .. note:: The :meth:`_engine.Connection.exec_driver_sql` method does
             not participate in the
             :meth:`_events.ConnectionEvents.before_execute` and
             :meth:`_events.ConnectionEvents.after_execute` events.   To
             intercept calls to :meth:`_engine.Connection.exec_driver_sql`, use
             :meth:`_events.ConnectionEvents.before_cursor_execute` and
             :meth:`_events.ConnectionEvents.after_cursor_execute`.

         .. seealso::

            :pep:`249`

        """

        args_10style, kwargs_10style = _distill_params_20(parameters)

        return self._exec_driver_sql(
            statement,
            args_10style,
            kwargs_10style,
            execution_options,
            future=True,
        )

    def _execute_context(
        self,
        dialect,
        constructor,
        statement,
        parameters,
        execution_options,
        *args,
        **kw
    ):
        """Create an :class:`.ExecutionContext` and execute, returning
        a :class:`_engine.CursorResult`."""

        branched = self
        if self.__branch_from:
            # if this is a "branched" connection, do everything in terms
            # of the "root" connection, *except* for .close(), which is
            # the only feature that branching provides
            self = self.__branch_from

        try:
            conn = self._dbapi_connection
            if conn is None:
                conn = self._revalidate_connection()

            context = constructor(
                dialect, self, conn, execution_options, *args, **kw
            )
        except (exc.PendingRollbackError, exc.ResourceClosedError):
            raise
        except BaseException as e:
            self._handle_dbapi_exception(
                e, util.text_type(statement), parameters, None, None
            )

        if (
            self._transaction
            and not self._transaction.is_active
            or (
                self._nested_transaction
                and not self._nested_transaction.is_active
            )
        ):
            self._invalid_transaction()

        elif self._trans_context_manager:
            TransactionalContext._trans_ctx_check(self)

        if self._is_future and self._transaction is None:
            self._autobegin()

        context.pre_exec()

        if dialect.use_setinputsizes:
            context._set_input_sizes()

        cursor, statement, parameters = (
            context.cursor,
            context.statement,
            context.parameters,
        )

        if not context.executemany:
            parameters = parameters[0]

        if self._has_events or self.engine._has_events:
            for fn in self.dispatch.before_cursor_execute:
                statement, parameters = fn(
                    self,
                    cursor,
                    statement,
                    parameters,
                    context,
                    context.executemany,
                )

        if self._echo:

            self._log_info(statement)

            stats = context._get_cache_stats()

            if not self.engine.hide_parameters:
                self._log_info(
                    "[%s] %r",
                    stats,
                    sql_util._repr_params(
                        parameters, batches=10, ismulti=context.executemany
                    ),
                )
            else:
                self._log_info(
                    "[%s] [SQL parameters hidden due to hide_parameters=True]"
                    % (stats,)
                )

        evt_handled = False
        try:
            if context.executemany:
                if self.dialect._has_events:
                    for fn in self.dialect.dispatch.do_executemany:
                        if fn(cursor, statement, parameters, context):
                            evt_handled = True
                            break
                if not evt_handled:
                    self.dialect.do_executemany(
                        cursor, statement, parameters, context
                    )
            elif not parameters and context.no_parameters:
                if self.dialect._has_events:
                    for fn in self.dialect.dispatch.do_execute_no_params:
                        if fn(cursor, statement, context):
                            evt_handled = True
                            break
                if not evt_handled:
                    self.dialect.do_execute_no_params(
                        cursor, statement, context
                    )
            else:
                if self.dialect._has_events:
                    for fn in self.dialect.dispatch.do_execute:
                        if fn(cursor, statement, parameters, context):
                            evt_handled = True
                            break
                if not evt_handled:
                    self.dialect.do_execute(
                        cursor, statement, parameters, context
                    )

            if self._has_events or self.engine._has_events:
                self.dispatch.after_cursor_execute(
                    self,
                    cursor,
                    statement,
                    parameters,
                    context,
                    context.executemany,
                )

            context.post_exec()

            result = context._setup_result_proxy()

            if not self._is_future:
                should_close_with_result = branched.should_close_with_result

                if not result._soft_closed and should_close_with_result:
                    result._autoclose_connection = True

                if (
                    # usually we're in a transaction so avoid relatively
                    # expensive / legacy should_autocommit call
                    self._transaction is None
                    and context.should_autocommit
                ):
                    self._commit_impl(autocommit=True)

                # for "connectionless" execution, we have to close this
                # Connection after the statement is complete.
                # legacy stuff.
                if should_close_with_result and context._soft_closed:
                    assert not self._is_future

                    # CursorResult already exhausted rows / has no rows.
                    # close us now
                    branched.close()

        except BaseException as e:
            self._handle_dbapi_exception(
                e, statement, parameters, cursor, context
            )

        return result

    def _cursor_execute(self, cursor, statement, parameters, context=None):
        """Execute a statement + params on the given cursor.

        Adds appropriate logging and exception handling.

        This method is used by DefaultDialect for special-case
        executions, such as for sequences and column defaults.
        The path of statement execution in the majority of cases
        terminates at _execute_context().

        """
        if self._has_events or self.engine._has_events:
            for fn in self.dispatch.before_cursor_execute:
                statement, parameters = fn(
                    self, cursor, statement, parameters, context, False
                )

        if self._echo:
            self._log_info(statement)
            self._log_info("[raw sql] %r", parameters)
        try:
            for fn in (
                ()
                if not self.dialect._has_events
                else self.dialect.dispatch.do_execute
            ):
                if fn(cursor, statement, parameters, context):
                    break
            else:
                self.dialect.do_execute(cursor, statement, parameters, context)
        except BaseException as e:
            self._handle_dbapi_exception(
                e, statement, parameters, cursor, context
            )

        if self._has_events or self.engine._has_events:
            self.dispatch.after_cursor_execute(
                self, cursor, statement, parameters, context, False
            )

    def _safe_close_cursor(self, cursor):
        """Close the given cursor, catching exceptions
        and turning into log warnings.

        """
        try:
            cursor.close()
        except Exception:
            # log the error through the connection pool's logger.
            self.engine.pool.logger.error(
                "Error closing cursor", exc_info=True
            )

    _reentrant_error = False
    _is_disconnect = False

    def _handle_dbapi_exception(
        self, e, statement, parameters, cursor, context
    ):
        exc_info = sys.exc_info()

        is_exit_exception = util.is_exit_exception(e)

        if not self._is_disconnect:
            self._is_disconnect = (
                isinstance(e, self.dialect.dbapi.Error)
                and not self.closed
                and self.dialect.is_disconnect(
                    e,
                    self._dbapi_connection if not self.invalidated else None,
                    cursor,
                )
            ) or (is_exit_exception and not self.closed)

        invalidate_pool_on_disconnect = not is_exit_exception

        if self._reentrant_error:
            util.raise_(
                exc.DBAPIError.instance(
                    statement,
                    parameters,
                    e,
                    self.dialect.dbapi.Error,
                    hide_parameters=self.engine.hide_parameters,
                    dialect=self.dialect,
                    ismulti=context.executemany
                    if context is not None
                    else None,
                ),
                with_traceback=exc_info[2],
                from_=e,
            )
        self._reentrant_error = True
        try:
            # non-DBAPI error - if we already got a context,
            # or there's no string statement, don't wrap it
            should_wrap = isinstance(e, self.dialect.dbapi.Error) or (
                statement is not None
                and context is None
                and not is_exit_exception
            )

            if should_wrap:
                sqlalchemy_exception = exc.DBAPIError.instance(
                    statement,
                    parameters,
                    e,
                    self.dialect.dbapi.Error,
                    hide_parameters=self.engine.hide_parameters,
                    connection_invalidated=self._is_disconnect,
                    dialect=self.dialect,
                    ismulti=context.executemany
                    if context is not None
                    else None,
                )
            else:
                sqlalchemy_exception = None

            newraise = None

            if (
                self._has_events or self.engine._has_events
            ) and not self._execution_options.get(
                "skip_user_error_events", False
            ):
                ctx = ExceptionContextImpl(
                    e,
                    sqlalchemy_exception,
                    self.engine,
                    self,
                    cursor,
                    statement,
                    parameters,
                    context,
                    self._is_disconnect,
                    invalidate_pool_on_disconnect,
                )

                for fn in self.dispatch.handle_error:
                    try:
                        # handler returns an exception;
                        # call next handler in a chain
                        per_fn = fn(ctx)
                        if per_fn is not None:
                            ctx.chained_exception = newraise = per_fn
                    except Exception as _raised:
                        # handler raises an exception - stop processing
                        newraise = _raised
                        break

                if self._is_disconnect != ctx.is_disconnect:
                    self._is_disconnect = ctx.is_disconnect
                    if sqlalchemy_exception:
                        sqlalchemy_exception.connection_invalidated = (
                            ctx.is_disconnect
                        )

                # set up potentially user-defined value for
                # invalidate pool.
                invalidate_pool_on_disconnect = (
                    ctx.invalidate_pool_on_disconnect
                )

            if should_wrap and context:
                context.handle_dbapi_exception(e)

            if not self._is_disconnect:
                if cursor:
                    self._safe_close_cursor(cursor)
                with util.safe_reraise(warn_only=True):
                    self._autorollback()

            if newraise:
                util.raise_(newraise, with_traceback=exc_info[2], from_=e)
            elif should_wrap:
                util.raise_(
                    sqlalchemy_exception, with_traceback=exc_info[2], from_=e
                )
            else:
                util.raise_(exc_info[1], with_traceback=exc_info[2])

        finally:
            del self._reentrant_error
            if self._is_disconnect:
                del self._is_disconnect
                if not self.invalidated:
                    dbapi_conn_wrapper = self._dbapi_connection
                    if invalidate_pool_on_disconnect:
                        self.engine.pool._invalidate(dbapi_conn_wrapper, e)
                    self.invalidate(e)
            if self.should_close_with_result:
                assert not self._is_future
                self.close()

    @classmethod
    def _handle_dbapi_exception_noconnection(cls, e, dialect, engine):
        exc_info = sys.exc_info()

        is_disconnect = dialect.is_disconnect(e, None, None)

        should_wrap = isinstance(e, dialect.dbapi.Error)

        if should_wrap:
            sqlalchemy_exception = exc.DBAPIError.instance(
                None,
                None,
                e,
                dialect.dbapi.Error,
                hide_parameters=engine.hide_parameters,
                connection_invalidated=is_disconnect,
            )
        else:
            sqlalchemy_exception = None

        newraise = None

        if engine._has_events:
            ctx = ExceptionContextImpl(
                e,
                sqlalchemy_exception,
                engine,
                None,
                None,
                None,
                None,
                None,
                is_disconnect,
                True,
            )
            for fn in engine.dispatch.handle_error:
                try:
                    # handler returns an exception;
                    # call next handler in a chain
                    per_fn = fn(ctx)
                    if per_fn is not None:
                        ctx.chained_exception = newraise = per_fn
                except Exception as _raised:
                    # handler raises an exception - stop processing
                    newraise = _raised
                    break

            if sqlalchemy_exception and is_disconnect != ctx.is_disconnect:
                sqlalchemy_exception.connection_invalidated = (
                    is_disconnect
                ) = ctx.is_disconnect

        if newraise:
            util.raise_(newraise, with_traceback=exc_info[2], from_=e)
        elif should_wrap:
            util.raise_(
                sqlalchemy_exception, with_traceback=exc_info[2], from_=e
            )
        else:
            util.raise_(exc_info[1], with_traceback=exc_info[2])

    def _run_ddl_visitor(self, visitorcallable, element, **kwargs):
        """run a DDL visitor.

        This method is only here so that the MockConnection can change the
        options given to the visitor so that "checkfirst" is skipped.

        """
        visitorcallable(self.dialect, self, **kwargs).traverse_single(element)

    @util.deprecated(
        "1.4",
        "The :meth:`_engine.Connection.transaction` "
        "method is deprecated and will be "
        "removed in a future release.  Use the :meth:`_engine.Engine.begin` "
        "context manager instead.",
    )
    def transaction(self, callable_, *args, **kwargs):
        r"""Execute the given function within a transaction boundary.

        The function is passed this :class:`_engine.Connection`
        as the first argument, followed by the given \*args and \**kwargs,
        e.g.::

            def do_something(conn, x, y):
                conn.execute(text("some statement"), {'x':x, 'y':y})

            conn.transaction(do_something, 5, 10)

        The operations inside the function are all invoked within the
        context of a single :class:`.Transaction`.
        Upon success, the transaction is committed.  If an
        exception is raised, the transaction is rolled back
        before propagating the exception.

        .. note::

           The :meth:`.transaction` method is superseded by
           the usage of the Python ``with:`` statement, which can
           be used with :meth:`_engine.Connection.begin`::

               with conn.begin():
                   conn.execute(text("some statement"), {'x':5, 'y':10})

           As well as with :meth:`_engine.Engine.begin`::

               with engine.begin() as conn:
                   conn.execute(text("some statement"), {'x':5, 'y':10})

        .. seealso::

            :meth:`_engine.Engine.begin` - engine-level transactional
            context

            :meth:`_engine.Engine.transaction` - engine-level version of
            :meth:`_engine.Connection.transaction`

        """

        kwargs["_sa_skip_warning"] = True
        trans = self.begin()
        try:
            ret = self.run_callable(callable_, *args, **kwargs)
            trans.commit()
            return ret
        except:
            with util.safe_reraise():
                trans.rollback()

    @util.deprecated(
        "1.4",
        "The :meth:`_engine.Connection.run_callable` "
        "method is deprecated and will "
        "be removed in a future release.  Invoke the callable function "
        "directly, passing the Connection.",
    )
    def run_callable(self, callable_, *args, **kwargs):
        r"""Given a callable object or function, execute it, passing
        a :class:`_engine.Connection` as the first argument.

        The given \*args and \**kwargs are passed subsequent
        to the :class:`_engine.Connection` argument.

        This function, along with :meth:`_engine.Engine.run_callable`,
        allows a function to be run with a :class:`_engine.Connection`
        or :class:`_engine.Engine` object without the need to know
        which one is being dealt with.

        """
        return callable_(self, *args, **kwargs)


class ExceptionContextImpl(ExceptionContext):
    """Implement the :class:`.ExceptionContext` interface."""

    def __init__(
        self,
        exception,
        sqlalchemy_exception,
        engine,
        connection,
        cursor,
        statement,
        parameters,
        context,
        is_disconnect,
        invalidate_pool_on_disconnect,
    ):
        self.engine = engine
        self.connection = connection
        self.sqlalchemy_exception = sqlalchemy_exception
        self.original_exception = exception
        self.execution_context = context
        self.statement = statement
        self.parameters = parameters
        self.is_disconnect = is_disconnect
        self.invalidate_pool_on_disconnect = invalidate_pool_on_disconnect


class Transaction(TransactionalContext):
    """Represent a database transaction in progress.

    The :class:`.Transaction` object is procured by
    calling the :meth:`_engine.Connection.begin` method of
    :class:`_engine.Connection`::

        from sqlalchemy import create_engine
        engine = create_engine("postgresql://scott:tiger@localhost/test")
        connection = engine.connect()
        trans = connection.begin()
        connection.execute(text("insert into x (a, b) values (1, 2)"))
        trans.commit()

    The object provides :meth:`.rollback` and :meth:`.commit`
    methods in order to control transaction boundaries.  It
    also implements a context manager interface so that
    the Python ``with`` statement can be used with the
    :meth:`_engine.Connection.begin` method::

        with connection.begin():
            connection.execute(text("insert into x (a, b) values (1, 2)"))

    The Transaction object is **not** threadsafe.

    .. seealso::

        :meth:`_engine.Connection.begin`

        :meth:`_engine.Connection.begin_twophase`

        :meth:`_engine.Connection.begin_nested`

    .. index::
      single: thread safety; Transaction
    """

    __slots__ = ()

    _is_root = False

    def __init__(self, connection):
        raise NotImplementedError()

    def _do_deactivate(self):
        """do whatever steps are necessary to set this transaction as
        "deactive", however leave this transaction object in place as far
        as the connection's state.

        for a "real" transaction this should roll back the transaction
        and ensure this transaction is no longer a reset agent.

        this is used for nesting of marker transactions where the marker
        can set the "real" transaction as rolled back, however it stays
        in place.

        for 2.0 we hope to remove this nesting feature.

        """
        raise NotImplementedError()

    @property
    def _deactivated_from_connection(self):
        """True if this transaction is totally deactivated from the connection
        and therefore can no longer affect its state.

        """
        raise NotImplementedError()

    def _do_close(self):
        raise NotImplementedError()

    def _do_rollback(self):
        raise NotImplementedError()

    def _do_commit(self):
        raise NotImplementedError()

    @property
    def is_valid(self):
        return self.is_active and not self.connection.invalidated

    def close(self):
        """Close this :class:`.Transaction`.

        If this transaction is the base transaction in a begin/commit
        nesting, the transaction will rollback().  Otherwise, the
        method returns.

        This is used to cancel a Transaction without affecting the scope of
        an enclosing transaction.

        """
        try:
            self._do_close()
        finally:
            assert not self.is_active

    def rollback(self):
        """Roll back this :class:`.Transaction`.

        The implementation of this may vary based on the type of transaction in
        use:

        * For a simple database transaction (e.g. :class:`.RootTransaction`),
          it corresponds to a ROLLBACK.

        * For a :class:`.NestedTransaction`, it corresponds to a
          "ROLLBACK TO SAVEPOINT" operation.

        * For a :class:`.TwoPhaseTransaction`, DBAPI-specific methods for two
          phase transactions may be used.


        """
        try:
            self._do_rollback()
        finally:
            assert not self.is_active

    def commit(self):
        """Commit this :class:`.Transaction`.

        The implementation of this may vary based on the type of transaction in
        use:

        * For a simple database transaction (e.g. :class:`.RootTransaction`),
          it corresponds to a COMMIT.

        * For a :class:`.NestedTransaction`, it corresponds to a
          "RELEASE SAVEPOINT" operation.

        * For a :class:`.TwoPhaseTransaction`, DBAPI-specific methods for two
          phase transactions may be used.

        """
        try:
            self._do_commit()
        finally:
            assert not self.is_active

    def _get_subject(self):
        return self.connection

    def _transaction_is_active(self):
        return self.is_active

    def _transaction_is_closed(self):
        return not self._deactivated_from_connection


class MarkerTransaction(Transaction):
    """A 'marker' transaction that is used for nested begin() calls.

    .. deprecated:: 1.4 future connection for 2.0 won't support this pattern.

    """

    __slots__ = ("connection", "_is_active", "_transaction")

    def __init__(self, connection):
        assert connection._transaction is not None
        if not connection._transaction.is_active:
            raise exc.InvalidRequestError(
                "the current transaction on this connection is inactive.  "
                "Please issue a rollback first."
            )

        assert not connection._is_future
        util.warn_deprecated_20(
            "Calling .begin() when a transaction is already begun, creating "
            "a 'sub' transaction, is deprecated "
            "and will be removed in 2.0.  See the documentation section "
            "'Migrating from the nesting pattern' for background on how "
            "to migrate from this pattern."
        )

        self.connection = connection

        if connection._trans_context_manager:
            TransactionalContext._trans_ctx_check(connection)

        if connection._nested_transaction is not None:
            self._transaction = connection._nested_transaction
        else:
            self._transaction = connection._transaction
        self._is_active = True

    @property
    def _deactivated_from_connection(self):
        return not self.is_active

    @property
    def is_active(self):
        return self._is_active and self._transaction.is_active

    def _deactivate(self):
        self._is_active = False

    def _do_close(self):
        # does not actually roll back the root
        self._deactivate()

    def _do_rollback(self):
        # does roll back the root
        if self._is_active:
            try:
                self._transaction._do_deactivate()
            finally:
                self._deactivate()

    def _do_commit(self):
        self._deactivate()


class RootTransaction(Transaction):
    """Represent the "root" transaction on a :class:`_engine.Connection`.

    This corresponds to the current "BEGIN/COMMIT/ROLLBACK" that's occurring
    for the :class:`_engine.Connection`. The :class:`_engine.RootTransaction`
    is created by calling upon the :meth:`_engine.Connection.begin` method, and
    remains associated with the :class:`_engine.Connection` throughout its
    active span. The current :class:`_engine.RootTransaction` in use is
    accessible via the :attr:`_engine.Connection.get_transaction` method of
    :class:`_engine.Connection`.

    In :term:`2.0 style` use, the :class:`_future.Connection` also employs
    "autobegin" behavior that will create a new
    :class:`_engine.RootTransaction` whenever a connection in a
    non-transactional state is used to emit commands on the DBAPI connection.
    The scope of the :class:`_engine.RootTransaction` in 2.0 style
    use can be controlled using the :meth:`_future.Connection.commit` and
    :meth:`_future.Connection.rollback` methods.


    """

    _is_root = True

    __slots__ = ("connection", "is_active")

    def __init__(self, connection):
        assert connection._transaction is None
        if connection._trans_context_manager:
            TransactionalContext._trans_ctx_check(connection)
        self.connection = connection
        self._connection_begin_impl()
        connection._transaction = self

        self.is_active = True

    def _deactivate_from_connection(self):
        if self.is_active:
            assert self.connection._transaction is self
            self.is_active = False

        elif self.connection._transaction is not self:
            util.warn("transaction already deassociated from connection")

    @property
    def _deactivated_from_connection(self):
        return self.connection._transaction is not self

    def _do_deactivate(self):
        # called from a MarkerTransaction to cancel this root transaction.
        # the transaction stays in place as connection._transaction, but
        # is no longer active and is no longer the reset agent for the
        # pooled connection.   the connection won't support a new begin()
        # until this transaction is explicitly closed, rolled back,
        # or committed.

        assert self.connection._transaction is self

        if self.is_active:
            self._connection_rollback_impl()

        # handle case where a savepoint was created inside of a marker
        # transaction that refers to a root.  nested has to be cancelled
        # also.
        if self.connection._nested_transaction:
            self.connection._nested_transaction._cancel()

        self._deactivate_from_connection()

    def _connection_begin_impl(self):
        self.connection._begin_impl(self)

    def _connection_rollback_impl(self):
        self.connection._rollback_impl()

    def _connection_commit_impl(self):
        self.connection._commit_impl()

    def _close_impl(self, try_deactivate=False):
        try:
            if self.is_active:
                self._connection_rollback_impl()

            if self.connection._nested_transaction:
                self.connection._nested_transaction._cancel()
        finally:
            if self.is_active or try_deactivate:
                self._deactivate_from_connection()
            if self.connection._transaction is self:
                self.connection._transaction = None

        assert not self.is_active
        assert self.connection._transaction is not self

    def _do_close(self):
        self._close_impl()

    def _do_rollback(self):
        self._close_impl(try_deactivate=True)

    def _do_commit(self):
        if self.is_active:
            assert self.connection._transaction is self

            try:
                self._connection_commit_impl()
            finally:
                # whether or not commit succeeds, cancel any
                # nested transactions, make this transaction "inactive"
                # and remove it as a reset agent
                if self.connection._nested_transaction:
                    self.connection._nested_transaction._cancel()

                self._deactivate_from_connection()

            # ...however only remove as the connection's current transaction
            # if commit succeeded.  otherwise it stays on so that a rollback
            # needs to occur.
            self.connection._transaction = None
        else:
            if self.connection._transaction is self:
                self.connection._invalid_transaction()
            else:
                raise exc.InvalidRequestError("This transaction is inactive")

        assert not self.is_active
        assert self.connection._transaction is not self


class NestedTransaction(Transaction):
    """Represent a 'nested', or SAVEPOINT transaction.

    The :class:`.NestedTransaction` object is created by calling the
    :meth:`_engine.Connection.begin_nested` method of
    :class:`_engine.Connection`.

    When using :class:`.NestedTransaction`, the semantics of "begin" /
    "commit" / "rollback" are as follows:

    * the "begin" operation corresponds to the "BEGIN SAVEPOINT" command, where
      the savepoint is given an explicit name that is part of the state
      of this object.

    * The :meth:`.NestedTransaction.commit` method corresponds to a
      "RELEASE SAVEPOINT" operation, using the savepoint identifier associated
      with this :class:`.NestedTransaction`.

    * The :meth:`.NestedTransaction.rollback` method corresponds to a
      "ROLLBACK TO SAVEPOINT" operation, using the savepoint identifier
      associated with this :class:`.NestedTransaction`.

    The rationale for mimicking the semantics of an outer transaction in
    terms of savepoints so that code may deal with a "savepoint" transaction
    and an "outer" transaction in an agnostic way.

    .. seealso::

        :ref:`session_begin_nested` - ORM version of the SAVEPOINT API.

    """

    __slots__ = ("connection", "is_active", "_savepoint", "_previous_nested")

    def __init__(self, connection):
        assert connection._transaction is not None
        if connection._trans_context_manager:
            TransactionalContext._trans_ctx_check(connection)
        self.connection = connection
        self._savepoint = self.connection._savepoint_impl()
        self.is_active = True
        self._previous_nested = connection._nested_transaction
        connection._nested_transaction = self

    def _deactivate_from_connection(self, warn=True):
        if self.connection._nested_transaction is self:
            self.connection._nested_transaction = self._previous_nested
        elif warn:
            util.warn(
                "nested transaction already deassociated from connection"
            )

    @property
    def _deactivated_from_connection(self):
        return self.connection._nested_transaction is not self

    def _cancel(self):
        # called by RootTransaction when the outer transaction is
        # committed, rolled back, or closed to cancel all savepoints
        # without any action being taken
        self.is_active = False
        self._deactivate_from_connection()
        if self._previous_nested:
            self._previous_nested._cancel()

    def _close_impl(self, deactivate_from_connection, warn_already_deactive):
        try:
            if self.is_active and self.connection._transaction.is_active:
                self.connection._rollback_to_savepoint_impl(self._savepoint)
        finally:
            self.is_active = False

            if deactivate_from_connection:
                self._deactivate_from_connection(warn=warn_already_deactive)

        assert not self.is_active
        if deactivate_from_connection:
            assert self.connection._nested_transaction is not self

    def _do_deactivate(self):
        self._close_impl(False, False)

    def _do_close(self):
        self._close_impl(True, False)

    def _do_rollback(self):
        self._close_impl(True, True)

    def _do_commit(self):
        if self.is_active:
            try:
                self.connection._release_savepoint_impl(self._savepoint)
            finally:
                # nested trans becomes inactive on failed release
                # unconditionally.  this prevents it from trying to
                # emit SQL when it rolls back.
                self.is_active = False

            # but only de-associate from connection if it succeeded
            self._deactivate_from_connection()
        else:
            if self.connection._nested_transaction is self:
                self.connection._invalid_transaction()
            else:
                raise exc.InvalidRequestError(
                    "This nested transaction is inactive"
                )


class TwoPhaseTransaction(RootTransaction):
    """Represent a two-phase transaction.

    A new :class:`.TwoPhaseTransaction` object may be procured
    using the :meth:`_engine.Connection.begin_twophase` method.

    The interface is the same as that of :class:`.Transaction`
    with the addition of the :meth:`prepare` method.

    """

    __slots__ = ("connection", "is_active", "xid", "_is_prepared")

    def __init__(self, connection, xid):
        self._is_prepared = False
        self.xid = xid
        super(TwoPhaseTransaction, self).__init__(connection)

    def prepare(self):
        """Prepare this :class:`.TwoPhaseTransaction`.

        After a PREPARE, the transaction can be committed.

        """
        if not self.is_active:
            raise exc.InvalidRequestError("This transaction is inactive")
        self.connection._prepare_twophase_impl(self.xid)
        self._is_prepared = True

    def _connection_begin_impl(self):
        self.connection._begin_twophase_impl(self)

    def _connection_rollback_impl(self):
        self.connection._rollback_twophase_impl(self.xid, self._is_prepared)

    def _connection_commit_impl(self):
        self.connection._commit_twophase_impl(self.xid, self._is_prepared)


class Engine(Connectable, log.Identified):
    """
    Connects a :class:`~sqlalchemy.pool.Pool` and
    :class:`~sqlalchemy.engine.interfaces.Dialect` together to provide a
    source of database connectivity and behavior.

    This is the **SQLAlchemy 1.x version** of :class:`_engine.Engine`.  For
    the :term:`2.0 style` version, which includes  some API differences,
    see :class:`_future.Engine`.

    An :class:`_engine.Engine` object is instantiated publicly using the
    :func:`~sqlalchemy.create_engine` function.

    .. seealso::

        :doc:`/core/engines`

        :ref:`connections_toplevel`

    """

    _execution_options = _EMPTY_EXECUTION_OPTS
    _has_events = False
    _connection_cls = Connection
    _sqla_logger_namespace = "sqlalchemy.engine.Engine"
    _is_future = False

    _schema_translate_map = None

    def __init__(
        self,
        pool,
        dialect,
        url,
        logging_name=None,
        echo=None,
        query_cache_size=500,
        execution_options=None,
        hide_parameters=False,
    ):
        self.pool = pool
        self.url = url
        self.dialect = dialect
        if logging_name:
            self.logging_name = logging_name
        self.echo = echo
        self.hide_parameters = hide_parameters
        if query_cache_size != 0:
            self._compiled_cache = util.LRUCache(
                query_cache_size, size_alert=self._lru_size_alert
            )
        else:
            self._compiled_cache = None
        log.instance_logger(self, echoflag=echo)
        if execution_options:
            self.update_execution_options(**execution_options)

    def _lru_size_alert(self, cache):
        if self._should_log_info:
            self.logger.info(
                "Compiled cache size pruning from %d items to %d.  "
                "Increase cache size to reduce the frequency of pruning.",
                len(cache),
                cache.capacity,
            )

    @property
    def engine(self):
        return self

    def clear_compiled_cache(self):
        """Clear the compiled cache associated with the dialect.

        This applies **only** to the built-in cache that is established
        via the :paramref:`_engine.create_engine.query_cache_size` parameter.
        It will not impact any dictionary caches that were passed via the
        :paramref:`.Connection.execution_options.query_cache` parameter.

        .. versionadded:: 1.4

        """
        if self._compiled_cache:
            self._compiled_cache.clear()

    def update_execution_options(self, **opt):
        r"""Update the default execution_options dictionary
        of this :class:`_engine.Engine`.

        The given keys/values in \**opt are added to the
        default execution options that will be used for
        all connections.  The initial contents of this dictionary
        can be sent via the ``execution_options`` parameter
        to :func:`_sa.create_engine`.

        .. seealso::

            :meth:`_engine.Connection.execution_options`

            :meth:`_engine.Engine.execution_options`

        """
        self._execution_options = self._execution_options.union(opt)
        self.dispatch.set_engine_execution_options(self, opt)
        self.dialect.set_engine_execution_options(self, opt)

    def execution_options(self, **opt):
        """Return a new :class:`_engine.Engine` that will provide
        :class:`_engine.Connection` objects with the given execution options.

        The returned :class:`_engine.Engine` remains related to the original
        :class:`_engine.Engine` in that it shares the same connection pool and
        other state:

        * The :class:`_pool.Pool` used by the new :class:`_engine.Engine`
          is the
          same instance.  The :meth:`_engine.Engine.dispose`
          method will replace
          the connection pool instance for the parent engine as well
          as this one.
        * Event listeners are "cascaded" - meaning, the new
          :class:`_engine.Engine`
          inherits the events of the parent, and new events can be associated
          with the new :class:`_engine.Engine` individually.
        * The logging configuration and logging_name is copied from the parent
          :class:`_engine.Engine`.

        The intent of the :meth:`_engine.Engine.execution_options` method is
        to implement "sharding" schemes where multiple :class:`_engine.Engine`
        objects refer to the same connection pool, but are differentiated
        by options that would be consumed by a custom event::

            primary_engine = create_engine("mysql://")
            shard1 = primary_engine.execution_options(shard_id="shard1")
            shard2 = primary_engine.execution_options(shard_id="shard2")

        Above, the ``shard1`` engine serves as a factory for
        :class:`_engine.Connection`
        objects that will contain the execution option
        ``shard_id=shard1``, and ``shard2`` will produce
        :class:`_engine.Connection`
        objects that contain the execution option ``shard_id=shard2``.

        An event handler can consume the above execution option to perform
        a schema switch or other operation, given a connection.  Below
        we emit a MySQL ``use`` statement to switch databases, at the same
        time keeping track of which database we've established using the
        :attr:`_engine.Connection.info` dictionary,
        which gives us a persistent
        storage space that follows the DBAPI connection::

            from sqlalchemy import event
            from sqlalchemy.engine import Engine

            shards = {"default": "base", shard_1: "db1", "shard_2": "db2"}

            @event.listens_for(Engine, "before_cursor_execute")
            def _switch_shard(conn, cursor, stmt,
                    params, context, executemany):
                shard_id = conn._execution_options.get('shard_id', "default")
                current_shard = conn.info.get("current_shard", None)

                if current_shard != shard_id:
                    cursor.execute("use %s" % shards[shard_id])
                    conn.info["current_shard"] = shard_id

        .. seealso::

            :meth:`_engine.Connection.execution_options`
            - update execution options
            on a :class:`_engine.Connection` object.

            :meth:`_engine.Engine.update_execution_options`
            - update the execution
            options for a given :class:`_engine.Engine` in place.

            :meth:`_engine.Engine.get_execution_options`


        """
        return self._option_cls(self, opt)

    def get_execution_options(self):
        """Get the non-SQL options which will take effect during execution.

        .. versionadded: 1.3

        .. seealso::

            :meth:`_engine.Engine.execution_options`
        """
        return self._execution_options

    @property
    def name(self):
        """String name of the :class:`~sqlalchemy.engine.interfaces.Dialect`
        in use by this :class:`Engine`."""

        return self.dialect.name

    @property
    def driver(self):
        """Driver name of the :class:`~sqlalchemy.engine.interfaces.Dialect`
        in use by this :class:`Engine`."""

        return self.dialect.driver

    echo = log.echo_property()

    def __repr__(self):
        return "Engine(%r)" % (self.url,)

    def dispose(self):
        """Dispose of the connection pool used by this
        :class:`_engine.Engine`.

        This has the effect of fully closing all **currently checked in**
        database connections.  Connections that are still checked out
        will **not** be closed, however they will no longer be associated
        with this :class:`_engine.Engine`,
        so when they are closed individually,
        eventually the :class:`_pool.Pool` which they are associated with will
        be garbage collected and they will be closed out fully, if
        not already closed on checkin.

        A new connection pool is created immediately after the old one has
        been disposed.   This new pool, like all SQLAlchemy connection pools,
        does not make any actual connections to the database until one is
        first requested, so as long as the :class:`_engine.Engine`
        isn't used again,
        no new connections will be made.

        .. seealso::

            :ref:`engine_disposal`

        """
        self.pool.dispose()
        self.pool = self.pool.recreate()
        self.dispatch.engine_disposed(self)

    def _execute_default(
        self, default, multiparams=(), params=util.EMPTY_DICT
    ):
        with self.connect() as conn:
            return conn._execute_default(default, multiparams, params)

    @contextlib.contextmanager
    def _optional_conn_ctx_manager(self, connection=None):
        if connection is None:
            with self.connect() as conn:
                yield conn
        else:
            yield connection

    class _trans_ctx(object):
        def __init__(self, conn, transaction, close_with_result):
            self.conn = conn
            self.transaction = transaction
            self.close_with_result = close_with_result

        def __enter__(self):
            self.transaction.__enter__()
            return self.conn

        def __exit__(self, type_, value, traceback):
            try:
                self.transaction.__exit__(type_, value, traceback)
            finally:
                if not self.close_with_result:
                    self.conn.close()

    def begin(self, close_with_result=False):
        """Return a context manager delivering a :class:`_engine.Connection`
        with a :class:`.Transaction` established.

        E.g.::

            with engine.begin() as conn:
                conn.execute(
                    text("insert into table (x, y, z) values (1, 2, 3)")
                )
                conn.execute(text("my_special_procedure(5)"))

        Upon successful operation, the :class:`.Transaction`
        is committed.  If an error is raised, the :class:`.Transaction`
        is rolled back.

        Legacy use only: the ``close_with_result`` flag is normally ``False``,
        and indicates that the :class:`_engine.Connection` will be closed when
        the operation is complete. When set to ``True``, it indicates the
        :class:`_engine.Connection` is in "single use" mode, where the
        :class:`_engine.CursorResult` returned by the first call to
        :meth:`_engine.Connection.execute` will close the
        :class:`_engine.Connection` when that :class:`_engine.CursorResult` has
        exhausted all result rows.

        .. seealso::

            :meth:`_engine.Engine.connect` - procure a
            :class:`_engine.Connection` from
            an :class:`_engine.Engine`.

            :meth:`_engine.Connection.begin` - start a :class:`.Transaction`
            for a particular :class:`_engine.Connection`.

        """
        if self._connection_cls._is_future:
            conn = self.connect()
        else:
            conn = self.connect(close_with_result=close_with_result)
        try:
            trans = conn.begin()
        except:
            with util.safe_reraise():
                conn.close()
        return Engine._trans_ctx(conn, trans, close_with_result)

    @util.deprecated(
        "1.4",
        "The :meth:`_engine.Engine.transaction` "
        "method is deprecated and will be "
        "removed in a future release.  Use the :meth:`_engine.Engine.begin` "
        "context "
        "manager instead.",
    )
    def transaction(self, callable_, *args, **kwargs):
        r"""Execute the given function within a transaction boundary.

        The function is passed a :class:`_engine.Connection` newly procured
        from :meth:`_engine.Engine.connect` as the first argument,
        followed by the given \*args and \**kwargs.

        e.g.::

            def do_something(conn, x, y):
                conn.execute(text("some statement"), {'x':x, 'y':y})

            engine.transaction(do_something, 5, 10)

        The operations inside the function are all invoked within the
        context of a single :class:`.Transaction`.
        Upon success, the transaction is committed.  If an
        exception is raised, the transaction is rolled back
        before propagating the exception.

        .. note::

           The :meth:`.transaction` method is superseded by
           the usage of the Python ``with:`` statement, which can
           be used with :meth:`_engine.Engine.begin`::

               with engine.begin() as conn:
                   conn.execute(text("some statement"), {'x':5, 'y':10})

        .. seealso::

            :meth:`_engine.Engine.begin` - engine-level transactional
            context

            :meth:`_engine.Connection.transaction`
            - connection-level version of
            :meth:`_engine.Engine.transaction`

        """
        kwargs["_sa_skip_warning"] = True
        with self.connect() as conn:
            return conn.transaction(callable_, *args, **kwargs)

    @util.deprecated(
        "1.4",
        "The :meth:`_engine.Engine.run_callable` "
        "method is deprecated and will be "
        "removed in a future release.  Use the :meth:`_engine.Engine.begin` "
        "context manager instead.",
    )
    def run_callable(self, callable_, *args, **kwargs):
        r"""Given a callable object or function, execute it, passing
        a :class:`_engine.Connection` as the first argument.

        The given \*args and \**kwargs are passed subsequent
        to the :class:`_engine.Connection` argument.

        This function, along with :meth:`_engine.Connection.run_callable`,
        allows a function to be run with a :class:`_engine.Connection`
        or :class:`_engine.Engine` object without the need to know
        which one is being dealt with.

        """
        kwargs["_sa_skip_warning"] = True
        with self.connect() as conn:
            return conn.run_callable(callable_, *args, **kwargs)

    def _run_ddl_visitor(self, visitorcallable, element, **kwargs):
        with self.begin() as conn:
            conn._run_ddl_visitor(visitorcallable, element, **kwargs)

    @util.deprecated_20(
        ":meth:`_engine.Engine.execute`",
        alternative="All statement execution in SQLAlchemy 2.0 is performed "
        "by the :meth:`_engine.Connection.execute` method of "
        ":class:`_engine.Connection`, "
        "or in the ORM by the :meth:`.Session.execute` method of "
        ":class:`.Session`.",
    )
    def execute(self, statement, *multiparams, **params):
        """Executes the given construct and returns a
        :class:`_engine.CursorResult`.

        The arguments are the same as those used by
        :meth:`_engine.Connection.execute`.

        Here, a :class:`_engine.Connection` is acquired using the
        :meth:`_engine.Engine.connect` method, and the statement executed
        with that connection. The returned :class:`_engine.CursorResult`
        is flagged
        such that when the :class:`_engine.CursorResult` is exhausted and its
        underlying cursor is closed, the :class:`_engine.Connection`
        created here
        will also be closed, which allows its associated DBAPI connection
        resource to be returned to the connection pool.

        """
        connection = self.connect(close_with_result=True)
        return connection.execute(statement, *multiparams, **params)

    @util.deprecated_20(
        ":meth:`_engine.Engine.scalar`",
        alternative="All statement execution in SQLAlchemy 2.0 is performed "
        "by the :meth:`_engine.Connection.execute` method of "
        ":class:`_engine.Connection`, "
        "or in the ORM by the :meth:`.Session.execute` method of "
        ":class:`.Session`; the :meth:`_future.Result.scalar` "
        "method can then be "
        "used to return a scalar result.",
    )
    def scalar(self, statement, *multiparams, **params):
        """Executes and returns the first column of the first row.

        The underlying result/cursor is closed after execution.
        """
        return self.execute(statement, *multiparams, **params).scalar()

    def _execute_clauseelement(
        self,
        elem,
        multiparams=None,
        params=None,
        execution_options=_EMPTY_EXECUTION_OPTS,
    ):
        connection = self.connect(close_with_result=True)
        return connection._execute_clauseelement(
            elem, multiparams, params, execution_options
        )

    def _execute_compiled(
        self,
        compiled,
        multiparams,
        params,
        execution_options=_EMPTY_EXECUTION_OPTS,
    ):
        connection = self.connect(close_with_result=True)
        return connection._execute_compiled(
            compiled, multiparams, params, execution_options
        )

    def connect(self, close_with_result=False):
        """Return a new :class:`_engine.Connection` object.

        The :class:`_engine.Connection` object is a facade that uses a DBAPI
        connection internally in order to communicate with the database.  This
        connection is procured from the connection-holding :class:`_pool.Pool`
        referenced by this :class:`_engine.Engine`. When the
        :meth:`_engine.Connection.close` method of the
        :class:`_engine.Connection` object
        is called, the underlying DBAPI connection is then returned to the
        connection pool, where it may be used again in a subsequent call to
        :meth:`_engine.Engine.connect`.

        """

        return self._connection_cls(self, close_with_result=close_with_result)

    @util.deprecated(
        "1.4",
        "The :meth:`_engine.Engine.table_names` "
        "method is deprecated and will be "
        "removed in a future release.  Please refer to "
        ":meth:`_reflection.Inspector.get_table_names`.",
    )
    def table_names(self, schema=None, connection=None):
        """Return a list of all table names available in the database.

        :param schema: Optional, retrieve names from a non-default schema.

        :param connection: Optional, use a specified connection.
        """
        with self._optional_conn_ctx_manager(connection) as conn:
            insp = inspection.inspect(conn)
            return insp.get_table_names(schema)

    @util.deprecated(
        "1.4",
        "The :meth:`_engine.Engine.has_table` "
        "method is deprecated and will be "
        "removed in a future release.  Please refer to "
        ":meth:`_reflection.Inspector.has_table`.",
    )
    def has_table(self, table_name, schema=None):
        """Return True if the given backend has a table of the given name.

        .. seealso::

            :ref:`metadata_reflection_inspector` - detailed schema inspection
            using the :class:`_reflection.Inspector` interface.

            :class:`.quoted_name` - used to pass quoting information along
            with a schema identifier.

        """
        with self._optional_conn_ctx_manager(None) as conn:
            insp = inspection.inspect(conn)
            return insp.has_table(table_name, schema=schema)

    def _wrap_pool_connect(self, fn, connection):
        dialect = self.dialect
        try:
            return fn()
        except dialect.dbapi.Error as e:
            if connection is None:
                Connection._handle_dbapi_exception_noconnection(
                    e, dialect, self
                )
            else:
                util.raise_(
                    sys.exc_info()[1], with_traceback=sys.exc_info()[2]
                )

    def raw_connection(self, _connection=None):
        """Return a "raw" DBAPI connection from the connection pool.

        The returned object is a proxied version of the DBAPI
        connection object used by the underlying driver in use.
        The object will have all the same behavior as the real DBAPI
        connection, except that its ``close()`` method will result in the
        connection being returned to the pool, rather than being closed
        for real.

        This method provides direct DBAPI connection access for
        special situations when the API provided by
        :class:`_engine.Connection`
        is not needed.   When a :class:`_engine.Connection` object is already
        present, the DBAPI connection is available using
        the :attr:`_engine.Connection.connection` accessor.

        .. seealso::

            :ref:`dbapi_connections`

        """
        return self._wrap_pool_connect(self.pool.connect, _connection)


class OptionEngineMixin(object):
    _sa_propagate_class_events = False

    def __init__(self, proxied, execution_options):
        self._proxied = proxied
        self.url = proxied.url
        self.dialect = proxied.dialect
        self.logging_name = proxied.logging_name
        self.echo = proxied.echo
        self._compiled_cache = proxied._compiled_cache
        self.hide_parameters = proxied.hide_parameters
        log.instance_logger(self, echoflag=self.echo)

        # note: this will propagate events that are assigned to the parent
        # engine after this OptionEngine is created.   Since we share
        # the events of the parent we also disallow class-level events
        # to apply to the OptionEngine class directly.
        #
        # the other way this can work would be to transfer existing
        # events only, using:
        # self.dispatch._update(proxied.dispatch)
        #
        # that might be more appropriate however it would be a behavioral
        # change for logic that assigns events to the parent engine and
        # would like it to take effect for the already-created sub-engine.
        self.dispatch = self.dispatch._join(proxied.dispatch)

        self._execution_options = proxied._execution_options
        self.update_execution_options(**execution_options)

    def _get_pool(self):
        return self._proxied.pool

    def _set_pool(self, pool):
        self._proxied.pool = pool

    pool = property(_get_pool, _set_pool)

    def _get_has_events(self):
        return self._proxied._has_events or self.__dict__.get(
            "_has_events", False
        )

    def _set_has_events(self, value):
        self.__dict__["_has_events"] = value

    _has_events = property(_get_has_events, _set_has_events)


class OptionEngine(OptionEngineMixin, Engine):
    pass


Engine._option_cls = OptionEngine
