from typing import List

from pydantic import BaseModel, ConfigDict

from apps.permissions.schemas import PermissionInfoSchema


class RoleBaseSchema(BaseModel):
    title: str
    internal_name: str


class RoleCreateSchema(RoleBaseSchema):
    permission_ids: List[int]


class RoleInfoSchema(RoleBaseSchema):
    id: int | None
    permissions: List[PermissionInfoSchema] | None
    model_config = ConfigDict(from_attributes=True)


class RoleUpdateSchema(BaseModel):
    title: str | None = None
    internal_name: str | None = None
    permission_ids: List[int] | None = None
