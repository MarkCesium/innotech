from fastapi import Request
from fastapi.responses import JSONResponse

from .exceptions import BaseAppError


async def app_exception_handler(request: Request, exc: BaseAppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )
