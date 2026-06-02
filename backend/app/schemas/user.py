from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Dùng khi đăng ký tài khoản
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

# Dùng khi đăng nhập
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Dữ liệu trả về cho client (không bao giờ trả password)
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    is_admin: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Dùng khi trả về token đăng nhập
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"