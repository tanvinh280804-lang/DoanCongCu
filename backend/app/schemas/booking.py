from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Dùng khi tạo booking mới
class BookingCreate(BaseModel):
    room_id: int
    check_in: str   # format: YYYY-MM-DD
    check_out: str  # format: YYYY-MM-DD
    guest_name: str
    guest_phone: str

# Dùng khi admin cập nhật trạng thái booking
class BookingUpdate(BaseModel):
    status: str  # pending / confirmed / cancelled

# Dữ liệu trả về cho client
class BookingResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    check_in: str
    check_out: str
    total_price: Optional[float]
    status: str
    guest_name: Optional[str]
    guest_phone: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True