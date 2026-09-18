from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class RegisterUser(BaseModel):
    email: EmailStr
    password: str


class ReadUser(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
