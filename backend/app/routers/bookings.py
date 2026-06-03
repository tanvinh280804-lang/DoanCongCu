from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.booking import Booking
from app.models.room import Room
from app.schemas.booking import BookingCreate, BookingUpdate, BookingResponse
from app.routers.auth import get_current_user, get_admin_user
from app.models.user import User

router = APIRouter()

# Lấy tất cả booking (chỉ admin)
@router.get("/", response_model=List[BookingResponse])
def get_all_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    bookings = db.query(Booking).all()
    return bookings

# Lấy booking của user đang đăng nhập
@router.get("/my-bookings", response_model=List[BookingResponse])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    return bookings

# Lấy chi tiết 1 booking
@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy booking"
        )
    # Chỉ admin hoặc chủ booking mới xem được
    if not current_user.is_admin and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem booking này"
        )
    return booking

# Tạo booking mới
@router.post("/", response_model=BookingResponse)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Kiểm tra phòng có tồn tại không
    room = db.query(Room).filter(Room.id == booking_data.room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy phòng"
        )

    # Kiểm tra phòng còn trống không
    if not room.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phòng này đã được đặt"
        )

    # Tính tổng tiền
    from datetime import datetime
    check_in = datetime.strptime(booking_data.check_in, "%Y-%m-%d")
    check_out = datetime.strptime(booking_data.check_out, "%Y-%m-%d")
    nights = (check_out - check_in).days
    if nights <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ngày check-out phải sau ngày check-in"
        )
    total_price = nights * room.price

    # Tạo booking
    new_booking = Booking(
        user_id=current_user.id,
        room_id=booking_data.room_id,
        check_in=booking_data.check_in,
        check_out=booking_data.check_out,
        total_price=total_price,
        guest_name=booking_data.guest_name,
        guest_phone=booking_data.guest_phone,
        status="pending"
    )

    # Đánh dấu phòng đã được đặt
    room.is_available = False

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

# Cập nhật trạng thái booking (chỉ admin)
@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy booking"
        )

    booking.status = booking_data.status

    # Nếu hủy hoặc trả phòng thì phòng về trạng thái còn trống
    if booking_data.status in ["cancelled", "checked_out"]:
        room = db.query(Room).filter(Room.id == booking.room_id).first()
        if room:
            room.is_available = True

    db.commit()
    db.refresh(booking)
    return booking

# Hủy booking (user tự hủy)
@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy booking"
        )

    # Chỉ chủ booking mới hủy được
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền hủy booking này"
        )

    # Trả phòng về trạng thái trống
    room = db.query(Room).filter(Room.id == booking.room_id).first()
    if room:
        room.is_available = True

    booking.status = "cancelled"
    db.commit()
    return {"message": "Hủy booking thành công"}