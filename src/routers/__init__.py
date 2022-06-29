from fastapi import APIRouter


api_router = APIRouter()


from .user import router

api_router.include_router(router)
