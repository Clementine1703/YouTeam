from typing import Optional

from fastapi import HTTPException

from sqlalchemy import Column, Integer, String, ForeignKey, asc, desc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query, Session, \
                           joinedload, relationship

from pydantic import BaseModel

from fastapi_filter.contrib.sqlalchemy import Filter

from config.database import Base

from .schemas import PermissionInfoSchema


class RolePermissionLink(Base):
    __tablename__ = 'role_permission_link'
    __table_args__ = {'extend_existing': True}
    role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permission.id'), primary_key=True)
    extend_existing=True


class Permission(Base):
    __tablename__ = 'permission'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    internal_name = Column(String, unique=True, index=True)
    title = Column(String, nullable=True)
    roles = relationship("Role", secondary=RolePermissionLink.__table__, back_populates="permissions")


class PermissionFilter(Filter):
    internal_name: Optional[str] = None
    title: Optional[str] = None

    async def apply_filters(self, query: Query, sortBy: str, sortDesc: bool, session: AsyncSession) -> list[PermissionInfoSchema]:

        if self.internal_name:
            query = query.filter(Permission.internal_name.ilike(f'%{self.internal_name}%'))
        if self.title:
            query = query.filter(Permission.title.ilike(f'%{self.title}%'))

        elif sortBy:
            if hasattr(Permission, sortBy):
                if sortDesc:
                    query = query.order_by(desc(getattr(Permission, sortBy)))
                else:
                    query = query.order_by(asc(getattr(Permission, sortBy)))
            else:
                raise HTTPException(status_code=400, detail=f"Неверное поле для сортировки: {sortBy}")

        result = await session.execute(query)
        permissions = result.scalars().all()
        return [PermissionInfoSchema.model_validate(permission) for permission in permissions]
