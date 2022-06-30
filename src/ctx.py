import contextvars
from typing import Generic, TypeVar
from sqlalchemy.orm import Session


DBType = TypeVar("DBType")
_global_vars = contextvars.ContextVar('_global_vars', default=None)


class GlobalVars(Generic[DBType]):
    @staticmethod
    def _set_var(name, obj):
        if _global_vars.get() is None:
            _global_vars.set({})
        _global_vars.get()[name] = obj

    @staticmethod
    def _get_var(name):
        return _global_vars.get()[name]

    @staticmethod
    def set_db(db_name: str, obj: DBType):
        GlobalVars._set_var(db_name, obj)

    @property
    def db(self) -> DBType:
        return self._get_var('db')

    def get_db(self, db_name) -> DBType:
        return self._get_var(db_name)


class G(GlobalVars[Session]):
    ...


g = G()
