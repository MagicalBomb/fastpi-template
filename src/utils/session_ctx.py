from contextlib import contextmanager
from utils.util import try_import

_fastapi = try_import('fastapi')


class SessionContext:
    def __init__(self, session_cls):
        self.session_cls = session_cls
        self.session_getter = None
        self.fastapi_g_key = None

    def current_session(self):
        if self.session_getter is None:
            if _fastapi and self.fastapi_g_key:
                from ctx import g
                return getattr(g, self.fastapi_g_key)
            raise Exception('can\'t detect db session')
        else:
            return self.session_getter()

    @contextmanager
    def __call__(self):
        session = self.session_cls()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            self.session_cls.remove()

    def _setup_context(
        self, app, *, fastapi_g_key, session_getter=None
    ):
        self.fastapi_g_key = fastapi_g_key
        if session_getter is not None:
            self.session_getter = session_getter

        if _fastapi and self.fastapi_g_key:
            self._setup_fastapi_g(app)

    def _setup_fastapi_g(self, app):
        if isinstance(app, _fastapi.FastAPI):
            from ctx import g

            @app.middleware("http")
            async def init_app_ctx(request: _fastapi.Request, call_next):
                if request.url.path.startswith('/static'):
                    response = await call_next(request)
                    return response

                with g.context():
                    setattr(g, self.fastapi_g_key, self.session_cls())
                    response = await call_next(request)
                    getattr(g, self.fastapi_g_key).close()

                return response
