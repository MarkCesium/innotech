from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import activate_user, create_user, find_user_by_email
from .schemas import UserDTO


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> UserDTO | None:
        user = await find_user_by_email(self.session, email=email)
        return UserDTO.model_validate(user) if user else None

    async def create_user(self, email: str, hashed_password: str) -> UserDTO:
        user = await create_user(self.session, email=email, hashed_password=hashed_password)
        return UserDTO.model_validate(user)

    async def activate_user(self, id: UUID) -> None:
        await activate_user(self.session, id)
