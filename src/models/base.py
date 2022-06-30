from typing import Any, Type
from sqlalchemy.ext.declarative import declared_attr, as_declarative
from sqlalchemy.orm import Session, Query
from fastapi.encoders import jsonable_encoder
from ctx import g


class Base:
    id: Any
    __name__: str
    __db__: str = 'default'

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def session(cls) -> Session:
        return getattr(g, cls.__db__)

    @classmethod
    @property
    def query(cls) -> Query:
        return cls.session().query(cls)

    @classmethod
    def filter(cls, *args) -> Query:
        return cls.session().query(cls).filter(*args)

    def dump(self, skips: set[str] = None) -> dict:
        return jsonable_encoder(vars(self), exclude=skips)

    def add_to_db(self, auto_commit=True):
        self.session().add(self)
        if auto_commit:
            self.session().commit()
        else:
            self.session().flush()

    def del_from_db(self, auto_commit=True):
        self.session().delete(self)
        if auto_commit:
            self.session().commit()

    @classmethod
    def get(cls, *argv, lock=False):
        if len(argv) == 1 and isinstance(argv[0], int):
            argv = [cls.id == argv[0]]
        query = cls.session().query(cls).filter(*argv)
        if lock:
            query = query.with_for_update()
        return query.one_or_none()


def declarative_base(name: str = 'db') -> Type[Base]:
    _model = as_declarative()(Base)
    _model.__db__ = name
    return _model


MODEL = declarative_base()
