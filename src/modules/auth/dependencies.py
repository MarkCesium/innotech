from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.core.dependencies import SettingsDep
from src.modules.users.dependencies import UserServiceDep

from .security import decode_token
from .service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)], settings: SettingsDep
) -> UUID:
    user_id = decode_token(token, expected_type="access", config=settings.jwt)
    return user_id


def get_auth_service(user_service: UserServiceDep, settings: SettingsDep) -> AuthService:
    return AuthService(user_service, settings.jwt)


AuthenticatedUserID = Annotated[UUID, Depends(get_current_user_id)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
