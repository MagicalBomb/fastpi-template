import schemas
from fastapi import APIRouter, Depends, Path
from models import User
from routers import deps
from utils.response import json_ok

router = APIRouter()


@router.post('/user', name="新建用户")
def new_user(data: schemas.UserCreate):
    user = User(**data.dict())
    user.add_to_db()
    return json_ok()


@router.get('/user/{id}', name="查询用户")
def get_user_info(user_obj=Depends(deps.get_user)):
    return schemas.UserInfo.from_orm(user_obj)


@router.get('/users', name='获取用户列表')
def get_user_list(
    *,
    page_info: deps.PagingParams = Depends(deps.get_paging_params),
):
    query = User.query.filter()
    total: int = query.count()
    users: list[User] = query.limit(page_info.limit).offset(page_info.skip).all()
    data = [schemas.UserInfo.from_orm(u) for u in users]
    return page_info.populate_result(total, data)
