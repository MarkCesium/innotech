from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserDTO(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
