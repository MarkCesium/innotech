from uuid import UUID

from .models import User
from .repository import create_user, get_user, update_user


class UserService:
    def __init__(self, session):
        self.session = session

    async def create_user(self, email: str, hashed_password: str) -> User:
        return await create_user(self.session, email=email, hashed_password=hashed_password)

    async def activate_user(self, id: UUID) -> None:
        user = await get_user(self.session, id)
        if user:
            await update_user(self.session, id, is_active=True)
