import asyncio
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from src.core.config import JWTConfig

password_hash = PasswordHash((Argon2Hasher(),))


async def hash_password(password: str) -> str:
    return await asyncio.to_thread(password_hash.hash, password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return await asyncio.to_thread(password_hash.verify, plain_password, hashed_password)


def create_access_token(user_id: str, config: JWTConfig) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(minutes=config.access_token_expire_minutes),
        "type": "access",
    }
    return jwt.encode(payload, config.secret, algorithm=config.algorithm)


def decode_access_token(token: str, config: JWTConfig) -> dict[str, Any]:
    return jwt.decode(
        token,
        config.secret,
        algorithms=["HS256"],
        options={
            "verify_signature": True,
            "require": [
                "exp",
                "sub",
                "type",
            ],
        },
    )
