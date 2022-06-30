from .base import CamelModel

__all__ = ["UserUpdate", "UserCreate", "UserInfo"]


class UserUpdate(CamelModel):
    email: str
    name: str


class UserCreate(UserUpdate):
    ...


class UserInfo(UserCreate):
    class Config:
        orm_mode = True
