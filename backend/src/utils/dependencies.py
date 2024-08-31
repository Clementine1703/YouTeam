from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.apps.auth.service import get_current_user
from utils.db import get_async_session
from src.apps.users.models import User
from apps.permissions.models import Permission


async def check_permissions(user_id: int, required_permissions: list[str], session: AsyncSession):
    # Получаем пользователя по его ID
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Получаем роли пользователя
    user_role = user.role
    if not user_role:
        raise HTTPException(status_code=403, detail="У пользователя нет ролей")

    # Получаем разрешения всех ролей пользователя
    user_permissions = set()
    for permission in user_role.permissions:
        user_permissions.add(permission.internal_name)

    if not user_permissions:
        raise HTTPException(status_code=403, detail="У пользователя нет разрешений")

    missing_permissions = [permission_name for permission_name in required_permissions if permission_name not in user_permissions]
    if missing_permissions:
        # Получаем названия недостающих разрешений
        statement = select(Permission).where(Permission.internal_name.in_(missing_permissions))
        result = await session.execute(statement)
        missing_permissions_m = result.scalars().all()
        
        missing_permissions_titles = [permission_m.title for permission_m in missing_permissions_m]

        # Если pemission.internal_name, указанный при вызове require_permission есть в бд
        if missing_permissions_titles:
            raise HTTPException(status_code=403, detail=f"Недостающие разрешения: {', '.join(missing_permissions_titles)}")
        else:
            raise HTTPException(status_code=403, detail=f"Доступ запрещен")

    return True
        

def require_permissions(*required_permissions):
    async def dependency(user=Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
        await check_permissions(user.id, list(required_permissions), session)
    return dependency