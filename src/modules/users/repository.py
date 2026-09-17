from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import update

from .exceptions import UserAlreadyExistsError
from .models import User


async def get_user_by_id(session: AsyncSession, id: UUID) -> User | None:
    return await session.get(User, id)


async def find_user_or_none(session: AsyncSession, **filter_by) -> User | None:
    statement = select(User).filter_by(**filter_by)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, **kwargs):
    user = User(**kwargs)
    session.add(user)
    try:
        await session.flush()
    except IntegrityError as e:
        if "unique constraint" in str(e).lower():
            raise UserAlreadyExistsError("User with this email already exists") from e
        raise
    await session.refresh(user)
    return user


async def update_user(session: AsyncSession, id: UUID, **kwargs) -> None:
    statement = update(User).where(User.id == id).values(**kwargs)
    await session.execute(statement)
