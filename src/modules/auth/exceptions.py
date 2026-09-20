from fastapi import status

from src.core.exceptions import BaseAppError


class InvalidTokenError(BaseAppError):
    def __init__(self, detail: str = "Invalid or expired token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidCredentialsError(BaseAppError):
    def __init__(self, detail: str = "Incorrect email or password"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class AccountNotActivatedError(BaseAppError):
    def __init__(self, detail: str = "Email is not verified"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
