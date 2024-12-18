from fastapi import HTTPException

from sqlalchemy import Column, Integer, String, ForeignKey, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query, selectinload, relationship

from fastapi_filter.contrib.sqlalchemy import Filter

from config.database import Base

from .schemas import RoleInfoSchema

from apps.permissions.models import Permission, RolePermissionLink


class UserRoleLink(Base):
    __tablename__ = 'user_role_link'
    __table_args__ = {'extend_existing': True}
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)
    extend_existing=True


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    internal_name = Column(String, unique=True, index=True)
    users = relationship("User", secondary=UserRoleLink.__table__, back_populates="roles", lazy="selectin")
    permissions = relationship("Permission", secondary=RolePermissionLink.__table__, back_populates="roles", lazy="selectin")


class RoleFilter(Filter):
    title: str | None = None
    permission_internal_name: str | None = None

    class Constants(Filter.Constants):
        model = Role

    async def apply_filters(self, query: Query, sortBy: str, sortDesc: bool, session: AsyncSession) -> list[RoleInfoSchema]:
        if self.title:
            query = query.filter(Role.title.ilike(f'%{self.title}%'))
        
        if self.permission_internal_name:
            query = query.outerjoin(Role.permissions).filter(Permission.internal_name.ilike(f'%{self.permission_internal_name}%'))


        if sortBy == 'permission_internal_name':
            query = query.outerjoin(Role.permissions)
            if sortDesc:
                query = query.order_by(desc(Permission.internal_name))
            else:
                query = query.order_by(asc(Permission.internal_name))
        elif sortBy:
            if hasattr(Role, sortBy):
                if sortDesc:
                    query = query.order_by(desc(getattr(Role, sortBy)))
                else:
                    query = query.order_by(asc(getattr(Role, sortBy)))
            else:
                raise HTTPException(status_code=400, detail=f"Неверное поле для сортировки: {sortBy}")

        query = query.options(selectinload(Role.permissions))

        result = await session.execute(query)
        filtered_roles = result.scalars().all()

        return [RoleInfoSchema.model_validate(role) for role in filtered_roles]
