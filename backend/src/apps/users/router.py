from fastapi import APIRouter, Depends
from fastapi.responses import Response

from sqlalchemy.ext.asyncio import AsyncSession

from utils.db import get_async_session

from .service import UserService

from apps.users.schemas import UserSchema, UserCreateSchema


router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=UserSchema)
async def create_user(user: UserCreateSchema, session: AsyncSession = Depends(get_async_session)):
    service = UserService(session)
    return await service.create_user(user)
