from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str

class Tokens(AccessToken, RefreshToken):
    ...

class TokenData(BaseModel):
    username: str | None = None
