from typing import Annotated

from fastapi import Depends

from src.core.dependencies import UoWDep

from .service import UserService


def get_user_service(uow: UoWDep) -> UserService:
    return UserService(uow)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
