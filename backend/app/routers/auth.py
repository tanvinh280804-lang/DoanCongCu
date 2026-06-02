from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)
from app.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# =====================
# HÀM PHỤ - Lấy user hiện tại từ token
# =====================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Kiểm tra token hợp lệ và trả về user hiện tại"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token không hợp lệ hoặc đã hết hạn",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Giải mã token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # Lấy email từ token
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    # Tìm user trong DB
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user

def get_admin_user(current_user: User = Depends(get_current_user)):
    """Kiểm tra user có phải admin không"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền thực hiện thao tác này"
        )
    return current_user

# =====================
# API ĐĂNG KÝ
# =====================

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Đăng ký tài khoản mới"""

    # Kiểm tra email đã tồn tại chưa
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email này đã được đăng ký"
        )

    # Tạo user mới
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# =====================
# API ĐĂNG NHẬP
# =====================

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Đăng nhập và nhận JWT token"""

    # Tìm user theo email
    user = db.query(User).filter(User.email == user_data.email).first()

    # Kiểm tra user tồn tại và mật khẩu đúng
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng"
        )

    # Kiểm tra tài khoản có bị khóa không
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản đã bị khóa"
        )

    # Tạo token
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )

    return {"access_token": access_token, "token_type": "bearer"}

# =====================
# API LẤY THÔNG TIN USER
# =====================

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Lấy thông tin user đang đăng nhập"""
    return current_user

# =====================
# API SET ADMIN (chỉ admin mới dùng được)
# =====================

@router.put("/set-admin/{user_id}", response_model=UserResponse)
def set_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Set quyền admin cho user theo id"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy user"
        )
    if user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User này đã là admin rồi"
        )
    user.is_admin = True
    db.commit()
    db.refresh(user)
    return user

@router.put("/remove-admin/{user_id}", response_model=UserResponse)
def remove_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Gỡ quyền admin của user theo id"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy user"
        )
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User này không phải admin"
        )
    user.is_admin = False
    db.commit()
    db.refresh(user)
    return user

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Lấy danh sách tất cả user (chỉ admin)"""
    users = db.query(User).all()
    return users