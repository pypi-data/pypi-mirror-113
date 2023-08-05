# ext/asyncio/scoping.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

from .session import AsyncSession
from ...orm.scoping import ScopedSessionMixin
from ...util import create_proxy_methods
from ...util import ScopedRegistry


@create_proxy_methods(
    AsyncSession,
    ":class:`_asyncio.AsyncSession`",
    ":class:`_asyncio.scoping.async_scoped_session`",
    classmethods=["close_all", "object_session", "identity_key"],
    methods=[
        "__contains__",
        "__iter__",
        "add",
        "add_all",
        "begin",
        "begin_nested",
        "close",
        "commit",
        "connection",
        "delete",
        "execute",
        "expire",
        "expire_all",
        "expunge",
        "expunge_all",
        "flush",
        "get",
        "get_bind",
        "is_modified",
        "merge",
        "refresh",
        "rollback",
        "scalar",
    ],
    attributes=[
        "bind",
        "dirty",
        "deleted",
        "new",
        "identity_map",
        "is_active",
        "autoflush",
        "no_autoflush",
        "info",
    ],
)
class async_scoped_session(ScopedSessionMixin):
    """Provides scoped management of :class:`.AsyncSession` objects.

    See the section :ref:`asyncio_scoped_session` for usage details.

    .. versionadded:: 1.4.19


    """

    def __init__(self, session_factory, scopefunc):
        """Construct a new :class:`_asyncio.async_scoped_session`.

        :param session_factory: a factory to create new :class:`_asyncio.AsyncSession`
         instances. This is usually, but not necessarily, an instance
         of :class:`_orm.sessionmaker` which itself was passed the
         :class:`_asyncio.AsyncSession` to its :paramref:`_orm.sessionmaker.class_`
         parameter::

            async_session_factory = sessionmaker(some_async_engine, class_= AsyncSession)
            AsyncSession = async_scoped_session(async_session_factory, scopefunc=current_task)

        :param scopefunc: function which defines
         the current scope.   A function such as ``asyncio.current_task``
         may be useful here.

        """  # noqa E501

        self.session_factory = session_factory
        self.registry = ScopedRegistry(session_factory, scopefunc)

    @property
    def _proxied(self):
        return self.registry()

    async def remove(self):
        """Dispose of the current :class:`.AsyncSession`, if present.

        Different from scoped_session's remove method, this method would use
        await to wait for the close method of AsyncSession.

        """

        if self.registry.has():
            await self.registry().close()
        self.registry.clear()
