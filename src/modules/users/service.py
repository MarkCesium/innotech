from uuid import UUID

from .models import User
from .repository import activate_user, create_user, find_user_or_none


class UserService:
    def __init__(self, session):
        self.session = session

    async def get_user_by_email(self, email: str) -> User | None:
        return await find_user_or_none(self.session, email=email)

    async def create_user(self, email: str, hashed_password: str) -> User:
        return await create_user(self.session, email=email, hashed_password=hashed_password)

    async def activate_user(self, id: UUID) -> None:
        await activate_user(self.session, id)
