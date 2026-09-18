from fastapi import status

from src.core.exceptions import BaseAppError


class UserAlreadyExistsError(BaseAppError):
    def __init__(self, detail: str = "User with this email already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class UserAlreadyActivatedOrNotFoundError(BaseAppError):
    def __init__(self, detail: str = "User already activated or not found"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
