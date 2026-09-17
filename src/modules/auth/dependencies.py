from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.core.config import JWTConfig
from src.core.dependencies import SettingsDep
from src.modules.users.dependencies import UserServiceDep

from .security import decode_token
from .service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user_id(token: str, config: JWTConfig) -> str:
    try:
        payload = decode_token(token, expected_type="access", config=config)
        return payload["sub"]
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


def get_auth_service(user_service: UserServiceDep, settings: SettingsDep) -> AuthService:
    return AuthService(user_service, settings.jwt)


AuthenticatedUserID = Annotated[str, Depends(get_current_user_id)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
