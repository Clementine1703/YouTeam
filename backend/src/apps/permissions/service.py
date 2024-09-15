from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from .models import Permission, PermissionFilter
from .schemas import PermissionCreateSchema, PermissionInfoSchema, PermissionUpdateSchema


class PermissionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def get_filter(self, filter: PermissionFilter, sortBy: str, sortDesc: bool) -> list[PermissionInfoSchema]:
        query = select(Permission)
        filtered_data = await filter.apply_filters(query, sortBy, sortDesc, self.session)
        return filtered_data
    
    async def create(self, permission_create: PermissionCreateSchema) -> Permission:
        statement = select(Permission).where(Permission.internal_name == permission_create.internal_name)
        result = await self.session.execute(statement)
        existing_permission = result.scalars().first()
        if existing_permission:
            raise HTTPException(status_code=404, detail="Разрешение с таким internal_name уже существует")
        new_permission = Permission(**permission_create.model_dump())
        self.session.add(new_permission)
        await self.session.commit()
        await self.session.refresh(new_permission)

        return new_permission
    
    async def update(self, permission_id: int, data_for_update: PermissionUpdateSchema) -> Permission:
        statement = select(Permission).where(Permission.id == permission_id)
        result = await self.session.execute(statement)
        permission = result.scalars().first()
        if not permission:
            raise HTTPException(status_code=404, detail="Разрешение не найдено")
        new_permission_data = data_for_update.model_dump(exclude_unset=True)
        try:
            for key, value in new_permission_data.items():
                setattr(permission, key, value)
            self.session.add(permission)
            await self.session.commit()
            await self.session.refresh(permission)
        except IntegrityError as e:
            await self.session.rollback()  # Откатываем транзакцию, чтобы избежать несогласованного состояния
            raise HTTPException(status_code=404, detail="Вы пытаетесь установить уже существующее значение unique полю")
        return permission
    
    async def delete(self, permission_ids: list[int]) -> None:
        statement = select(Permission).where(Permission.id.in_(permission_ids))
        result = await self.session.execute(statement)
        permissions = result.scalars().all()

        if not permissions:
            raise HTTPException(status_code=404, detail=f"Разрешения с указанными id не найдены")

        for permission in permissions:
            await self.session.delete(permission)
        await self.session.commit()

    async def get(self, permission_id: int) -> PermissionInfoSchema:
        statement = select(Permission).where(Permission.id == permission_id)
        result = await self.session.execute(statement)
        permission = result.scalars().first()
        if not permission:
            raise HTTPException(status_code=404, detail="Разрешение не найдено")
        
        return permission
