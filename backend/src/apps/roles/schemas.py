from typing import List

from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    title: str
    internal_name: str


class RoleCreate(RoleBase):
    permissions_ids: List[int]


class RoleInfo(RoleBase):
    id: int | None
    permissions: list | None
    model_config = ConfigDict(from_attributes=True)


class RoleUpdate(BaseModel):
    title: str | None = None
    internal_name: str | None = None
    permissions_ids: List[int] | None = None
