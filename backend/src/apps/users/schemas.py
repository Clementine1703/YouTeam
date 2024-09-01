from pydantic import BaseModel


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