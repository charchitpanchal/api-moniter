from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from app.models.user import UserRole


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"