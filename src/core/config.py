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


class SMTPConfig(BaseModel):
    from_email: str
    host: str
    port: int
    user: str | None = Field(default=None)
    password: str | None = Field(default=None)
    use_tls: bool = Field(default=False)


class AppConfig(BaseModel):
    base_url: str = Field(default="http://localhost:8000")
    allowed_origins: list[str] = Field(default=["http://localhost:8000"])


class DatabaseSettings(BaseSettings):
    db: PostgresConfig = Field(...)

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


class Settings(BaseSettings):
    app: AppConfig = Field(...)
    db: PostgresConfig = Field(...)
    jwt: JWTConfig = Field(...)
    smtp: SMTPConfig = Field(...)

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
