from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete

from .models import Role, RoleFilter
from .schemas import RoleCreateSchema, RoleInfoSchema, RoleUpdateSchema

from apps.permissions.models import Permission, RolePermissionLink


class RoleService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_filter(self, filter: RoleFilter, sortBy: str, sortDesc: bool) -> list[RoleInfoSchema]:
        query = select(Role)
        filtered_data = await filter.apply_filters(query, sortBy, sortDesc, self.session)
        return filtered_data

    async def create(self, data_for_create: RoleCreateSchema) -> Role:
        permission_ids = data_for_create.permission_ids

        # Проверка, что permission_ids является списком целых чисел
        if not isinstance(permission_ids, list) or not all(isinstance(pid, int) for pid in permission_ids):
            raise HTTPException(status_code=400, detail="permission_ids должен быть списком целых чисел")

        # Выборка разрешений
        query = select(Permission).where(Permission.id.in_(permission_ids))
        result = await self.session.execute(query)
        permissions = result.scalars().all()

        # Проверка, что все разрешения найдены
        if len(permissions) != len(permission_ids):
            raise HTTPException(status_code=404, detail="Некоторые разрешения не найдены")

        # Проверка, что роль с таким internal_name не существует
        query = select(Role).where(Role.internal_name == data_for_create.internal_name)
        result = await self.session.execute(query)
        existing_role = result.scalars().first()
        if existing_role:
            raise HTTPException(status_code=404, detail="Роль с таким internal_name уже существует")

        # Создание новой роли пользователя
        new_role = Role(**data_for_create.model_dump(exclude={"permission_ids"}))

        # Добавление новой роли в сессию
        self.session.add(new_role)
        await self.session.commit()

        # Добавление разрешений к роли пользователя
        for p in permissions:
            role_permission_link = RolePermissionLink(role_id=new_role.id, permission_id=p.id)
            self.session.add(role_permission_link)

        await self.session.commit()
        await self.session.refresh(new_role)

        return new_role

    async def update(self, role_id: int, data_for_update: RoleUpdateSchema) -> Role:
        query = select(Role).where(Role.id == role_id).options(selectinload(Role.permissions))
        result = await self.session.execute(query)
        role = result.scalars().first()
        if not role:
            raise HTTPException(status_code=404, detail="Роль не найдена")

        permission_ids = data_for_update.permission_ids

        # Проверка, что permission_ids не является None
        if permission_ids is not None:
            # Выборка разрешений
            await delete_all_permissions_from_role(self.session, role)
            query = select(Permission).where(Permission.id.in_(permission_ids))
            result = await self.session.execute(query)
            permissions = result.scalars().all()

            # Проверка, что все разрешения найдены
            if len(permissions) != len(permission_ids):
                raise HTTPException(status_code=404, detail="Некоторые разрешения не найдены")

            for permission in permissions:
                role_permission_link = RolePermissionLink(role_id=role.id, permission_id=permission.id)
                self.session.add(role_permission_link)

        # Проверка, что роль с таким internal_name не существует
        query = select(Role).where(Role.internal_name == data_for_update.internal_name).filter(Role.id != role_id)
        result = await self.session.execute(query)
        existing_role = result.scalars().first()
        if existing_role:
            raise HTTPException(status_code=409, detail="Роль с таким internal_name уже существует")

        new_role_data = data_for_update.model_dump(exclude_unset=True, exclude={"permission_ids"})
        try:
            for key, value in new_role_data.items():
                setattr(role, key, value)
            self.session.add(role)
            await self.session.commit()
            await self.session.refresh(role)

        except IntegrityError as e:
            await self.session.rollback()  # Откатываем транзакцию, чтобы избежать несогласованного состояния
            raise HTTPException(status_code=400, detail=str(e))

        return role

    async def delete(self, role_ids: list[int]) -> None:
        query = select(Role).where(Role.id.in_(role_ids))
        result = await self.session.execute(query)
        roles = result.scalars().all()

        if not roles:
            raise HTTPException(status_code=404, detail=f"Роли с указанными id не найдены")

        for role in roles:
            await self.session.delete(role)
        await self.session.commit()

    async def get(self, role_id: int) -> RoleInfoSchema:
        query = select(Role).where(Role.id == role_id)
        result = await self.session.execute(query)
        role = result.scalars().first()
        if not role:
            raise HTTPException(status_code=404, detail="Роль не найдена")

        return role


async def delete_all_permissions_from_role(session: AsyncSession, role: Role):
    await session.execute(delete(RolePermissionLink).where(RolePermissionLink.role_id == role.id))
