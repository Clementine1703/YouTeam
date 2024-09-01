from pydantic import BaseModel, ConfigDict


class PermissionBaseSchema(BaseModel):
    internal_name: str
    title: str | None = None


class PermissionCreateSchema(PermissionBaseSchema):
    pass


class PermissionInfoSchema(PermissionBaseSchema):
    id: int | None
    internal_name: str
    model_config = ConfigDict(from_attributes=True)


class PermissionUpdateSchema(BaseModel):
    internal_name: str | None = None
    title: str | None = None
