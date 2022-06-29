from sqlalchemy import types, Column
from .base import MODEL


__all__ = ["User"]

class User(MODEL):
    __tablename__ = 'user'
    email = Column(types.VARCHAR(128), primary_key=True, comment="user email")