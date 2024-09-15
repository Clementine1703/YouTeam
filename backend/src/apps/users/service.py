from fastapi import HTTPException

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.service import pwd_context

from .schemas import UserCreateSchema, UserInfoSchema
from .models import User, UserFilter

from apps.roles.models import Role, UserRoleLink



class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filter(self, filter: UserFilter, sortBy: str, sortDesc: bool) -> list[UserInfoSchema]:
        query = select(User)
        filtered_data = await filter.apply_filters(query, sortBy, sortDesc, self.session)
        return filtered_data

    async def create(self, data_for_create: UserCreateSchema):
        role_ids = data_for_create.role_ids

        if not isinstance(role_ids, list) or not all(isinstance(pid, int) for pid in role_ids):
            raise HTTPException(status_code=400, detail="role_ids должен быть списком целых чисел")

        query = select(Role).where(Role.id.in_(role_ids))
        result = await self.session.execute(query)
        roles = result.scalars().all()

        if len(roles) != len(role_ids):
            raise HTTPException(status_code=404, detail="Некоторые роли не найдены")



        stmt = select(User).where(User.username == data_for_create.username)
        result = await self.session.execute(stmt)
        existing_user = result.scalar_one_or_none()
    
        if existing_user:
            raise HTTPException(status_code=400, detail=f"Пользователь '{data_for_create.username}' уже существует.")
        
        hashed_password = pwd_context.hash(data_for_create.password)

        new_user = User(
            username=data_for_create.username,
            email=data_for_create.email,
            full_name=data_for_create.full_name,
            hashed_password=hashed_password,
            disabled=data_for_create.disabled
        )
        self.session.add(new_user)
        await self.session.commit()

        for r in roles:
            user_role_link = UserRoleLink(user_id=new_user.id, role_id=r.id)
            self.session.add(user_role_link)

        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user
