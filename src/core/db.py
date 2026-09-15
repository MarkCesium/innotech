from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .config import settings

engine = create_async_engine(
    url=settings.db.url,
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
    pool_pre_ping=settings.db.pool_pre_ping,
    pool_timeout=settings.db.pool_timeout,
)
async_session_factory = async_sessionmaker[AsyncSession](
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
