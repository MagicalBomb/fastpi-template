from sqlalchemy import types, Column
from .base import MODEL


__all__ = ["User"]

class User(MODEL):

    id = Column(types.Integer, primary_key=True, comment="user id")
    email = Column(types.VARCHAR(128), comment="user email")
    name = Column(types.VARCHAR(128), comment="user name")