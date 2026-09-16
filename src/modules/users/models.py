from uuid import UUID, uuid7

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import BaseModel


class User(BaseModel):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
