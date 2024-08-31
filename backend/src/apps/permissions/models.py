from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey, asc, desc
from sqlalchemy.orm import Query, Session, \
                           joinedload, relationship

from fastapi_filter.contrib.sqlalchemy import Filter

from config.database import Base

from schemas import PermissionInfo


class RolePermissionLink(Base):
    __tablename__ = 'role_permission_link'
    role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permission.id'), primary_key=True)


class Permission(Base):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True, index=True)
    internal_name = Column(String, unique=True, index=True)
    title = Column(String, nullable=True)
    roles = relationship("Role", secondary=RolePermissionLink.__table__, back_populates="permissions")


class PermissionFilter(Filter):
    internal_name: Optional[str] = None
    title: Optional[str] = None

    class Constants(Filter.Constants):
        model = Permission

    def apply_filters(self, query: Query, sortBy: str, sortDesc: bool, session: Session) -> list[PermissionInfo]:
        if self.internal_name:
            query = query.filter(Permission.internal_name.ilike(f'%{self.internal_name}%'))
        if self.title:
            query = query.filter(Permission.title.ilike(f'%{self.title}%'))

        if sortBy:
            if sortDesc:
                query = query.order_by(desc(sortBy))
            else:
                query = query.order_by(asc(sortBy))

        permissions = session.execute(query).scalars().all()
        return [PermissionInfo.model_validate(permission) for permission in permissions]
