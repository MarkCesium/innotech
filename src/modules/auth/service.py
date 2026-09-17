from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.service import UserService

from .security import hash_password


class AuthService:
    def __init__(self, session: AsyncSession, user_service: UserService):
        self.session = session
        self.users = user_service

    async def register_user(self, email: str, password: str) -> None:
        hashed_password = await hash_password(password)
        await self.users.create_user(email, hashed_password)
        # TODO: Send notification
