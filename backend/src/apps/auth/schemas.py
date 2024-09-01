from pydantic import BaseModel


class AccessTokenSchema(BaseModel):
    access_token: str
    token_type: str

class RefreshTokenSchema(BaseModel):
    refresh_token: str

class TokensSchema(AccessTokenSchema, RefreshTokenSchema):
    ...

class TokenDataSchema(BaseModel):
    username: str | None = None
