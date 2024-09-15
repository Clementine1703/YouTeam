from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, paginate

from sqlalchemy.ext.asyncio import AsyncSession

from utils.db import get_async_session
from .service import PermissionService
from .models import PermissionFilter
from .schemas import PermissionCreateSchema, PermissionUpdateSchema, PermissionInfoSchema


router = APIRouter(
    prefix="/permissions",
    tags=["Разрешения"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=Page[PermissionInfoSchema])
async def get_all_permissions(
    filter: PermissionFilter = FilterDepends(PermissionFilter),
    page: int = 1,
    size: int = 50,
    sortBy: str = "title",
    sortDesc: bool = False,
    session: AsyncSession = Depends(get_async_session)
):
    service = PermissionService(session)
    filtered_permissions = await service.get_filter(filter, sortBy, sortDesc)
    return paginate(filtered_permissions)


@router.post("/", response_model=PermissionInfoSchema)
async def create(
    data_for_create: PermissionCreateSchema,
    session: AsyncSession = Depends(get_async_session)
):
    service = PermissionService(session)
    new_permission = await service.create(data_for_create)
    return new_permission


@router.patch("/{permission_id}", response_model=PermissionInfoSchema)
async def update(
    permission_id: int,
    data_for_update: PermissionUpdateSchema,
    session: AsyncSession = Depends(get_async_session)
):
    service = PermissionService(session)
    updated_permission = await service.update(permission_id, data_for_update)
    return updated_permission


@router.delete("/")
async def delete(
    permission_ids: list[int],
    session: AsyncSession = Depends(get_async_session)
):
    service = PermissionService(session)
    await service.delete(permission_ids)
    return {"ok": True}


@router.get("/{permission_id}", response_model=PermissionInfoSchema)
async def get(
    permission_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    service = PermissionService(session)
    permission = await service.get(permission_id)
    return permission
