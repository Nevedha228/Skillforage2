from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    year: int = Field(..., ge=1, le=4)
    degree: str = Field(..., min_length=2, max_length=100)
    branch: str = Field(..., min_length=2, max_length=100)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()


class ResendOTPRequest(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    year: int
    degree: str
    branch: str
    target_role: Optional[str] = None
    timezone: str
    daily_study_hours: float
    learning_style: str
    notifications_enabled: bool
    email_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    success: bool
    message: str
    user: Optional[UserResponse] = None
