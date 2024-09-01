from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, paginate

from sqlalchemy.ext.asyncio import AsyncSession

from utils.db import get_async_session
from .service import RoleService
from .models import RoleFilter
from .schemas import RoleCreateSchema, RoleUpdateSchema, RoleInfoSchema

# TODO
from utils.dependencies import require_permissions


router = APIRouter(
    prefix="/roles",
    tags=["Роли"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=Page[RoleInfoSchema])
async def get_all_roles(
    role_filter: RoleFilter = FilterDepends(RoleFilter),
    page: int = 1,
    size: int = 50,
    sortBy: str = "title",
    sortDesc: bool = False,
    session: AsyncSession = Depends(get_async_session)
):
    service = RoleService(session)
    filtered_roles = await service.get_role_filter(role_filter, sortBy, sortDesc)
    return paginate(filtered_roles)


@router.post("/", response_model=RoleInfoSchema)
async def create_role(
    data_for_create: RoleCreateSchema,
    session: AsyncSession = Depends(get_async_session)
):
    service = RoleService(session)
    new_role = await service.create_role(data_for_create)
    return new_role


@router.patch("/{role_id}", response_model=RoleInfoSchema)
async def update_role(
    role_id: int,
    data_for_update: RoleUpdateSchema,
    session: AsyncSession = Depends(get_async_session)
):
    service = RoleService(session)
    updated_role = await service.update_role(role_id, data_for_update)
    return updated_role


@router.delete("/")
async def delete_roles(
    role_ids: list[int],
    session: AsyncSession = Depends(get_async_session)
):
    service = RoleService(session)
    await service.delete_roles(role_ids)
    return {"ok": True}


@router.get("/{role_id}", response_model=RoleInfoSchema)
async def get_role(
    role_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    service = RoleService(session)
    role = await service.get_role(role_id)
    return role
