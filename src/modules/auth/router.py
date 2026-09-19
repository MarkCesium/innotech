from fastapi import APIRouter

from src.modules.users.openapi import (
    USER_ALREADY_ACTIVATED_OR_NOT_FOUND_RESPONSE,
    USER_ALREADY_EXISTS_RESPONSE,
)

from .dependencies import AuthServiceDep
from .openapi import UNAUTHORIZED_RESPONSE
from .schemas import ReadUser, RegisterUser, Token

router = APIRouter(prefix="/auth")


@router.post(
    "/register",
    response_model=ReadUser,
    responses={**USER_ALREADY_EXISTS_RESPONSE},
)
async def register_user(
    data: RegisterUser,
    auth_service: AuthServiceDep,
):
    user = await auth_service.register_user(data.email, data.password)
    return user


@router.get(
    "/verify-email",
    name="verify_email",
    responses={
        **UNAUTHORIZED_RESPONSE,
        **USER_ALREADY_ACTIVATED_OR_NOT_FOUND_RESPONSE,
    },
)
async def verify_email(token: str, auth_service: AuthServiceDep) -> Token:
    token = await auth_service.verify_email(token)
    return Token(access_token=token, token_type="bearer")
