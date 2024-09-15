from typing import List

from pydantic import BaseModel, ConfigDict

from apps.roles.schemas import RoleInfoSchema



class UserBaseSchema(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserSchema(UserBaseSchema):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True


class UserCreateSchema(UserBaseSchema):
    password: str
    role_ids: List[int]


class UserInfoSchema(UserBaseSchema):
    id: int | None
    roles: List[RoleInfoSchema] | None
    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    role_ids: List[int] | None = None
