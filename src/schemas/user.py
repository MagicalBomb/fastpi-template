from .base import CamelModel

__all__ = ["User"]


class User(CamelModel):
    email: str