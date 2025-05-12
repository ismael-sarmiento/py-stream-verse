# services/auth_service/schemas.py
from pydantic import BaseModel, EmailStr
import enum


class RoleEnum(str, enum.Enum):
    admin = "admin"
    client = "client"


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: RoleEnum


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleEnum

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int
    role: RoleEnum
