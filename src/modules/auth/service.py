from src.core.config import JWTConfig
from src.modules.users.models import User
from src.modules.users.service import UserService

from .security import create_verification_token, hash_password


class AuthService:
    def __init__(self, user_service: UserService, jwt_config: JWTConfig):
        self.users = user_service
        self.jwt_config = jwt_config

    async def register_user(self, email: str, password: str) -> tuple[User, str]:
        hashed_password = await hash_password(password)
        user = await self.users.create_user(email, hashed_password)
        token = create_verification_token(user.id.hex, self.jwt_config)
        return user, token
