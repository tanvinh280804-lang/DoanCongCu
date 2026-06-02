from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Dùng khi tạo phòng mới
class RoomCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    capacity: int = 2
    image_url: Optional[str] = ""

# Dùng khi cập nhật phòng (tất cả đều Optional vì có thể chỉ sửa 1 trường)
class RoomUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    capacity: Optional[int] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None

# Dữ liệu trả về cho client
class RoomResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    capacity: int
    image_url: str
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True