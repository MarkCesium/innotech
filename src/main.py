from fastapi import APIRouter, FastAPI

from src.core.exception_handlers import app_exception_handler
from src.core.exceptions import BaseAppError
from src.modules.auth.router import router as auth_router

app = FastAPI()
router = APIRouter(prefix="/api")

router.include_router(auth_router)
app.include_router(router)
app.add_exception_handler(BaseAppError, app_exception_handler)  # type: ignore[arg-type]


@app.get("/")
def index() -> str:
    return "Hello!"
