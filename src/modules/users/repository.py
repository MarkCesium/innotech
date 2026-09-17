from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import update

from .models import User


async def get_user(session: AsyncSession, id: UUID) -> User | None:
    return await session.get(User, id)


async def create_user(session: AsyncSession, **kwargs):
    user = User(**kwargs)
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


async def update_user(session: AsyncSession, id: UUID, **kwargs) -> None:
    statement = update(User).where(User.id == id).values(**kwargs)
    await session.execute(statement)
