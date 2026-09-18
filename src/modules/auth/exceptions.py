from fastapi import status

from src.core.exceptions import BaseAppError


class InvalidTokenError(BaseAppError):
    def __init__(self, detail: str = "Invalid or expired token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
