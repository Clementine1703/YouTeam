from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class User(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str