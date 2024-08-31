from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey, asc, desc
from sqlalchemy.orm import Query, Session, \
                           joinedload, relationship

from fastapi_filter.contrib.sqlalchemy import Filter

from config.database import Base

from schemas import RoleInfo

from src.apps.permissions.models import Permission, RolePermissionLink


class Role(Base):
    __tablename__ = 'user_role'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    internal_name = Column(String, unique=True, index=True)
    user = relationship("User", back_populates="role", uselist=False)
    permissions = relationship("Permission", secondary=RolePermissionLink.__table__, back_populates="roles")


class RoleFilter(Filter):
    title: Optional[str] = None
    permission_internal_name: Optional[str] = None

    class Constants(Filter.Constants):
        model = Role

    def apply_filters(self, query: Query, sortBy: str, sortDesc: bool, session: Session) -> list[RoleInfo]:
        if self.title:
            query = query.filter(Role.title.ilike(f'%{self.title}%'))
        
        if self.permission_internal_name:
            query = query.join(Role.permissions).filter(Permission.internal_name.ilike(f'%{self.permission_internal_name}%'))

        if sortBy == 'permission_internal_name':
            query = query.outerjoin(Role.permissions).options(joinedload(Role.permissions))
            if sortDesc:
                query = query.order_by(desc(Permission.internal_name))
            else:
                query = query.order_by(asc(Permission.internal_name))

        if sortBy:
            if sortDesc:
                query = query.order_by(desc(sortBy))
            else:
                query = query.order_by(asc(sortBy))

        user_roles = session.execute(query).scalars().all()
        return [RoleInfo.model_validate(user_role) for user_role in user_roles]
