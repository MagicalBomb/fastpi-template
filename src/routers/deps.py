from typing import Optional
from fastapi import HTTPException, Query
from models.user import User
from schemas.base import PagingParams


async def get_paging_params(
    offset: Optional[int] = Query(1, ge=1), limit: Optional[int] = Query(20, ge=1)
) -> PagingParams:
    return PagingParams(**{"offset": offset, "limit": limit})


async def get_user(id: int) -> User:
    user: User = User.get(id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {id=} not found.")
    return user
