from typing import Protocol

from src.core.config import JWTConfig
from src.modules.users.service import UserService

from .exceptions import AccountNotActivatedError, InvalidCredentialsError
from .schemas import ReadUser
from .security import create_access_token, create_verification_token, decode_token


class EmailSender(Protocol):
    def send_verification(self, email: str, token: str) -> None: ...


class AuthService:
    def __init__(self, user_service: UserService, jwt_config: JWTConfig, email_sender: EmailSender):
        self.users = user_service
        self.jwt_config = jwt_config
        self.email_sender = email_sender

    async def register_user(self, email: str, password: str) -> ReadUser:
        user = await self.users.create_user(email, password)
        token = create_verification_token(user.id.hex, self.jwt_config)
        self.email_sender.send_verification(email, token)
        return ReadUser.model_validate(user)

    async def login(self, email: str, password: str) -> str:
        user = await self.users.authenticate(email, password)
        if user is None:
            raise InvalidCredentialsError()
        if not user.is_active:
            raise AccountNotActivatedError()
        return create_access_token(user.id.hex, self.jwt_config)

    async def verify_email(self, token: str) -> str:
        user_id = decode_token(token, "verification", self.jwt_config)
        await self.users.activate_user(user_id)
        return create_access_token(user_id.hex, self.jwt_config)
