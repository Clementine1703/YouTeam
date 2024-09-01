from fastapi import HTTPException

from sqlalchemy import text
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import async_session
from apps.auth.service import pwd_context

from .schemas import UserCreateSchema
from .models import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_create_data: UserCreateSchema):
        stmt = select(User).where(User.username == user_create_data.username)
        result = await self.session.execute(stmt)
        existing_user = result.scalar_one_or_none()
    
        if existing_user:
            raise HTTPException(status_code=400, detail=f"Пользователь '{user_create_data.username}' уже существует.")
        
        hashed_password = pwd_context.hash(user_create_data.password)
        session_user = User(
            username=user_create_data.username,
            email=user_create_data.email,
            full_name=user_create_data.full_name,
            hashed_password=hashed_password,
            disabled=user_create_data.disabled
        )
        self.session.add(session_user)
        await self.session.commit()
        await self.session.flush()
        await self.session.refresh(session_user)
        return session_user