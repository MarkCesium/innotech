from fastapi import APIRouter, FastAPI

from src.modules.auth.router import router as auth_router

app = FastAPI()
router = APIRouter(prefix="/api")

router.include_router(auth_router)
app.include_router(router)


@app.get("/")
def index() -> str:
    return "Hello!"
