import logging
import time

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utils.util import try_import

from .session_ctx import SessionContext

_empty = object()
_fastapi = try_import('fastapi')


class DataSource:
    _datasources = {}

    def __init__(self, name):
        if name in self._datasources:
            raise Exception('duplicated datasource: %s' % name)

        self._datasources[name] = self
        self.name = name
        self.session_cls = sessionmaker() if _fastapi else scoped_session(
            sessionmaker())
        self.session_context = SessionContext(self.session_cls)
        self.engine = None
        self.session_config = None
        self.used_by_model = False

    def current_session(self):
        return self.session_context.current_session()

    @classmethod
    def get(cls, name):
        return cls._datasources.get(name)

    @classmethod
    def get_or_create(cls, name):
        if name not in cls._datasources:
            cls._datasources[name] = cls(name)
        return cls._datasources[name]

    @property
    def _default_g_key(self):
        return 'db' if self.name == 'default' else f'db_{self.name}'

    def session_configure(self,
                          *,
                          fastapi_g_key=_empty,
                          session_getter=None):
        if self.session_config is not None:
            raise Exception('session_configure can only call once')
        if fastapi_g_key is _empty:
            fastapi_g_key = self._default_g_key
        self.session_config = dict(session_getter=session_getter,
                                   fastapi_g_key=fastapi_g_key)

    def _setup(self,
               app,
               app_settings,
               db_settings,
               *,
               ignore_resetup=False,
               session_getter=None):
        if self.engine is not None:
            if ignore_resetup:
                return
            raise Exception('engine has already bind')

        self._bind_engine(db_settings['uri'],
                          pool_size=db_settings.get('pool_size', 20),
                          echo=db_settings.get(
                              'echo', app_settings.get('SQL_TRACE', False)),
                          isolation_level=db_settings.get('isolation_level'),
                          pool_recycle=db_settings.get('pool_recycle', 3600))
        if self.session_config is None:
            self.session_configure(session_getter=session_getter)
        self.session_context._setup_context(app, **self.session_config)

    def _bind_engine(self,
                     uri,
                     pool_size=20,
                     echo=False,
                     isolation_level=None,
                     pool_recycle=3600):
        kwargs = dict(echo=echo, pool_pre_ping=True, pool_recycle=pool_recycle)
        if isolation_level:
            kwargs['isolation_level'] = isolation_level
        if pool_size:
            kwargs['pool_size'] = pool_size
        self.engine = create_engine(uri, **kwargs)
        self.session_cls.configure(bind=self.engine)


DEFAULT_DATASOURCE = DataSource('default')


def setup_db(app_settings,
             app=None,
             ignore_resetup=True,
             session_getter=None):
    db_settings = app_settings.get('SQLALCHEMY_DATABASES', {})
    for name, settings in db_settings.items():
        DataSource.get_or_create(name)._setup(app,
                                              app_settings,
                                              settings,
                                              ignore_resetup=ignore_resetup,
                                              session_getter=session_getter)
    for name, ds in DataSource._datasources.items():
        if ds.used_by_model and ds.engine is None:
            raise Exception(
                f'missing config for datasource[{name}], forgot SQLALCHEMY_DATABASES or SQLALCHEMY_DATABASE_URI?'
            )

    if app_settings.get('SQL_TRACE'):
        logger = logging.getLogger("sqltrace")
        logger.setLevel(logging.DEBUG)

        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context,
                                  executemany):
            conn.info.setdefault('query_start_time', []).append(time.time())

        @event.listens_for(Engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context,
                                 executemany):
            total = time.time() - conn.info['query_start_time'].pop(-1)
            logger.info(
                "%r, %s", total,
                statement % {k: repr(v)
                             for k, v in parameters.items()})
