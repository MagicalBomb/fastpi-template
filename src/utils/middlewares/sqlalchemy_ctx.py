from abc import ABC
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, Session
from starlette.types import ASGIApp
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from ctx import g
from utils.datasource import DataSource, setup_db


@contextmanager
def session_context(factories: dict[str, sessionmaker]) -> dict[str, Session]:
    sessions = {name: factory() for name, factory in factories.items()}
    try:
        yield sessions
    except:
        for _, s in sessions.items():
            s.rollback()
        raise
    finally:
        for _, s in sessions.items():
            s.close()


class DBMiddleware(BaseHTTPMiddleware, ABC):
    def __init__(self, app: ASGIApp, setting=None, prefix_only: str = None) -> None:
        if setting:
            setup_db(setting, app)
        self.session_factories: dict[str, sessionmaker] = {
            name: sessionmaker(bind=ds.engine, expire_on_commit=False)
            for name, ds in DataSource._datasources.items()
        }
        self.prefix_only = prefix_only
        super().__init__(app, dispatch=None)

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        request = Request(scope, receive=receive)
        injection_db = request.url.path.startswith(
            self.prefix_only) if self.prefix_only else None
        if injection_db:
            with session_context(self.session_factories) as sessions:
                for name, local_session in sessions.items():
                    db_name = "db" if name == 'default' else f"db_{name}"
                    g.set_db(db_name, local_session)
                await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)
