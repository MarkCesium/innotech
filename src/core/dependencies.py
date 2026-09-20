from typing import Annotated

from fastapi import Depends, Request

from .config import Settings, get_settings
from .uow import UnitOfWork


def get_uow(request: Request) -> UnitOfWork:
    return UnitOfWork(request.app.state.async_session_factory)


UoWDep = Annotated[UnitOfWork, Depends(get_uow)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
