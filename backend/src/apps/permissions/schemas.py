from pydantic import BaseModel, ConfigDict


class PermissionBase(BaseModel):
    internal_name: str
    title: str | None = None


class PermissionCreate(PermissionBase):
    pass


class PermissionInfo(PermissionBase):
    id: int | None
    model_config = ConfigDict(from_attributes=True)


class PermissionUpdate(BaseModel):
    internal_name: str | None = None
    title: str | None = None
