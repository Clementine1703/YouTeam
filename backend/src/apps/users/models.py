from fastapi import HTTPException

from sqlalchemy import Column, String, Integer, Boolean, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query, selectinload, relationship

from fastapi_filter.contrib.sqlalchemy import Filter

from apps.roles.models import Role, UserRoleLink

from .schemas import UserInfoSchema

from config.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=50), unique=True)
    email = Column(String(length=100))
    full_name = Column(String(length=50))
    hashed_password = Column(String)
    disabled = Column(Boolean())

    roles = relationship("Role", secondary=UserRoleLink.__table__, back_populates="users", lazy="selectin")\
    

class UserFilter(Filter):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    role_internal_name: str | None = None

    class Constants(Filter.Constants):
        model = User

    async def apply_filters(self, query: Query, sortBy: str, sortDesc: bool, session: AsyncSession) -> list[UserInfoSchema]:
        if self.username:
            query = query.filter(User.username.ilike(f'%{self.username}%'))
        
        if self.role_internal_name:
            query = query.outerjoin(User.roles).filter(Role.internal_name.ilike(f'%{self.role_internal_name}%'))


        if sortBy == 'role_internal_name':
            query = query.outerjoin(User.roles)
            if sortDesc:
                query = query.order_by(desc(Role.internal_name))
            else:
                query = query.order_by(asc(Role.internal_name))
        elif sortBy:
            if hasattr(Role, sortBy):
                if sortDesc:
                    query = query.order_by(desc(getattr(User, sortBy)))
                else:
                    query = query.order_by(asc(getattr(User
                    , sortBy)))
            else:
                raise HTTPException(status_code=400, detail=f"Неверное поле для сортировки: {sortBy}")

        query = query.options(selectinload(User.roles))

        result = await session.execute(query)
        filtered_users = result.scalars().all()

        return [UserInfoSchema.model_validate(role) for role in filtered_users]
