from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, paginate

from sqlalchemy.ext.asyncio import AsyncSession

from utils.db import get_async_session
from .service import PermissionService
from .models import Permission, PermissionFilter
from .schemas import PermissionCreate, PermissionUpdate, PermissionInfo


router = APIRouter(
    prefix="/permissions",
    tags=["Разрешения"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=Page[PermissionInfo])
async def get_all_permissions(
    permission_filter: PermissionFilter = FilterDepends(PermissionFilter),
    page: int = 1,
    size: int = 50,
    sortBy: str = "title",
    sortDesc: bool = False,
    session: AsyncSession = Depends(get_async_session)
):
    service = PermissionService(session)
    filtered_permissions = await service.get_permission_filter(permission_filter, sortBy, sortDesc)
    return paginate(filtered_permissions)


@router.post("/", response_model=Permission)
async def create_permission(
    data_for_create: PermissionCreate,
    session: AsyncSession = Depends(get_async_session)
):
    service = PermissionService(session)
    new_permission = await service.create_permission(data_for_create)
    return new_permission


@router.patch("/{permission_id}", response_model=Permission)
async def update_permission(
    permission_id: int,
    data_for_update: PermissionUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    service = PermissionService(session)
    updated_permission = await service.update_permission(permission_id, data_for_update)
    return updated_permission


@router.delete("/")
async def delete_permissions(
    permissions_ids: list[int],
    session: AsyncSession = Depends(get_async_session)
):
    service = PermissionService(session)
    await service.delete_permissions(permissions_ids)
    return {"ok": True}


@router.get("/{permission_id}", response_model=PermissionInfo)
async def get_permission(
    permission_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    service = PermissionService(session)
    permission = await service.get_permission(permission_id)
    return permission
