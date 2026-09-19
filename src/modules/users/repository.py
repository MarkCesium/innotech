from typing import cast
from uuid import UUID

from sqlalchemy import CursorResult, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import update

from .exceptions import UserAlreadyActivatedOrNotFoundError, UserAlreadyExistsError
from .models import User


async def find_user_by_email(session: AsyncSession, email: str) -> User | None:
    statement = select(User).filter_by(email=email)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, email: str, hashed_password: str) -> User:
    user = User(email=email, hashed_password=hashed_password)
    session.add(user)
    try:
        await session.flush()
    except IntegrityError as e:
        if "unique constraint" in str(e).lower():
            raise UserAlreadyExistsError() from e
        raise
    # await session.refresh(user)
    return user


async def activate_user(session: AsyncSession, id: UUID) -> None:
    statement = (
        update(User)
        .where(
            User.id == id,
            User.is_active.is_(False),
        )
        .values(is_active=True)
    )

    result = await session.execute(statement)
    cursor_result = cast(CursorResult[tuple[User]], result)
    if cursor_result.rowcount == 0:
        raise UserAlreadyActivatedOrNotFoundError()
