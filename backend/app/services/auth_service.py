from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

# Cấu hình thuật toán mã hóa mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =====================
# MÃ HÓA MẬT KHẨU
# =====================

def hash_password(password: str) -> str:
    """Mã hóa mật khẩu thô thành chuỗi hash"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """So sánh mật khẩu thô với mật khẩu đã mã hóa"""
    return pwd_context.verify(plain_password, hashed_password)

# =====================
# JWT TOKEN
# =====================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Tạo JWT token từ data (thường là user_id và email)"""
    to_encode = data.copy()

    # Tính thời gian hết hạn
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    # Mã hóa thành token
    token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return token

def decode_access_token(token: str) -> Optional[dict]:
    """Giải mã JWT token, trả về data bên trong hoặc None nếu token không hợp lệ"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None