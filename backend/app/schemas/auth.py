from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from app.models.user import UserRole


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "password": "securepassword123",
            }
        }
    }


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