import os
from datetime import timedelta
from typing import Annotated, Dict

import jwt
from jose import JWTError

from fastapi import APIRouter
from fastapi.responses import Response
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from utils.db import get_async_session

from .service import authenticate_user, get_current_active_user,\
      create_access_token, create_refresh_token

from .schemas import AccessTokenSchema, TokensSchema
from apps.users.schemas import UserBaseSchema

from config.auth import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    tags=["Авторизация"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
) -> TokensSchema:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    return TokensSchema(access_token=access_token, token_type="bearer", refresh_token=refresh_token)


@router.get("/users/me/", response_model=UserBaseSchema)
async def read_users_me(
    current_user: Annotated[UserBaseSchema, Depends(get_current_active_user)],
):
    return current_user


@router.post("/refresh")
async def refresh_access_token(refresh_token: str) -> AccessTokenSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: Dict = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("refresh") is not True:
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError as e:
        raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    
    return AccessTokenSchema(access_token=access_token, token_type="bearer")
