from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import async_session
from apps.auth.service import pwd_context

from .schemas import UserCreate
from .models import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserCreate):
        hashed_password = pwd_context.hash(user.password)
        session_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
            disabled=user.disabled
        )
        self.session.add(session_user)
        await self.session.commit()
        await self.session.flush()
        await self.session.refresh(session_user)
        return session_user