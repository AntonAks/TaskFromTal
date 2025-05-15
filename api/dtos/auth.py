from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):  # type: ignore[misc]
    username: str
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):  # type: ignore[misc]
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):  # type: ignore[misc]
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):  # type: ignore[misc]
    username: Optional[str] = None
    user_id: Optional[str] = None
    is_admin: Optional[bool] = False


class AuthDTO(BaseModel):
    username: str
    password: str
