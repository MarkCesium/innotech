import asyncio
from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from src.core.config import JWTConfig

from .exceptions import InvalidTokenError

password_hash = PasswordHash((Argon2Hasher(),))


async def hash_password(password: str) -> str:
    return await asyncio.to_thread(password_hash.hash, password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return await asyncio.to_thread(password_hash.verify, plain_password, hashed_password)


def _create_token(user_id: str, token_type: str, expire_delta: timedelta, config: JWTConfig) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + expire_delta,
        "type": token_type,
    }
    return jwt.encode(payload, config.secret, algorithm=config.algorithm)


def create_access_token(user_id: str, config: JWTConfig) -> str:
    return _create_token(
        user_id=user_id,
        token_type="access",
        expire_delta=timedelta(minutes=config.access_token_expire_minutes),
        config=config,
    )


def create_verification_token(user_id: str, config: JWTConfig) -> str:
    return _create_token(
        user_id=user_id,
        token_type="verification",
        expire_delta=timedelta(hours=24),
        config=config,
    )


def decode_token(token: str, expected_type: str, config: JWTConfig) -> UUID:
    try:
        payload = jwt.decode(
            token,
            config.secret,
            algorithms=[config.algorithm],
            options={
                "verify_signature": True,
                "require": ["exp", "sub", "type"],
            },
        )
        user_id = UUID(payload.get("sub"))
    except (jwt.PyJWTError, ValueError) as e:
        raise InvalidTokenError() from e

    if payload.get("type") != expected_type:
        raise InvalidTokenError(detail=f"Expected '{expected_type}' token")

    return user_id
