from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.core.dependencies import UoWDep

from .dependencies import AuthServiceDep
from .openapi import (
    INVALID_CREDENTIALS_RESPONSE,
    NOT_ACTIVATED_RESPONSE,
    UNAUTHORIZED_RESPONSE,
    USER_ALREADY_ACTIVATED_OR_NOT_FOUND_RESPONSE,
    USER_ALREADY_EXISTS_RESPONSE,
)
from .schemas import ReadUser, RegisterUser, Token

router = APIRouter(prefix="/auth")


@router.post(
    "/register",
    response_model=ReadUser,
    responses={**USER_ALREADY_EXISTS_RESPONSE},
)
async def register_user(
    data: RegisterUser,
    uow: UoWDep,
    auth_service: AuthServiceDep,
):
    async with uow:
        return await auth_service.register_user(data.email, data.password)


@router.post(
    "/login",
    response_model=Token,
    responses={**INVALID_CREDENTIALS_RESPONSE, **NOT_ACTIVATED_RESPONSE},
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: UoWDep,
    auth_service: AuthServiceDep,
) -> Token:
    async with uow:
        token = await auth_service.login(form_data.username, form_data.password)
    return Token(access_token=token, token_type="bearer")


@router.get(
    "/verify-email",
    name="verify_email",
    responses={
        **UNAUTHORIZED_RESPONSE,
        **USER_ALREADY_ACTIVATED_OR_NOT_FOUND_RESPONSE,
    },
)
async def verify_email(token: str, uow: UoWDep, auth_service: AuthServiceDep) -> Token:
    async with uow:
        access_token = await auth_service.verify_email(token)
    return Token(access_token=access_token, token_type="bearer")
