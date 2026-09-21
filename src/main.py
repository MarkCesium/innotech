from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import get_settings
from src.core.exception_handlers import app_exception_handler
from src.core.exceptions import BaseAppError
from src.modules.auth.router import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    engine = create_async_engine(
        url=settings.db.url,
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
        pool_pre_ping=settings.db.pool_pre_ping,
        pool_timeout=settings.db.pool_timeout,
    )
    async_session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    app.state.async_session_factory = async_session_factory
    try:
        yield
    finally:
        await engine.dispose()


settings = get_settings()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.app.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
router = APIRouter(prefix="/api")

router.include_router(auth_router)
app.include_router(router)
app.add_exception_handler(BaseAppError, app_exception_handler)  # type: ignore[arg-type]


@app.get("/")
def index() -> str:
    return "Hello!"
