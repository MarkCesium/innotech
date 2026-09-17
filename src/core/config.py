from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class PostgresConfig(BaseModel):
    dsn: PostgresDsn = Field(...)
    echo: bool = Field(default=False)
    echo_pool: bool = Field(default=False)
    pool_size: int = Field(default=10)
    max_overflow: int = Field(default=5)
    pool_pre_ping: bool = Field(default=True)
    pool_timeout: int = Field(default=30)

    @property
    def url(self) -> str:
        return self.dsn.unicode_string()


class JWTConfig(BaseModel):
    secret: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class AppConfig(BaseModel):
    allowed_origins: list[str] = Field(default=["http://localhost:8000"])


class Settings(BaseSettings):
    app: AppConfig = Field(...)
    db: PostgresConfig = Field(...)
    jwt: JWTConfig = Field(...)

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
