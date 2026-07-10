from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.payment import Payment
from app.models.booking import Booking
from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse
from app.routers.auth import get_current_user, get_admin_user
from app.models.user import User

router = APIRouter()

# Lấy tất cả payment (chỉ admin)
@router.get("/", response_model=List[PaymentResponse])
def get_all_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    return db.query(Payment).all()

# Lấy payment của các booking thuộc về user hiện tại
@router.get("/my-payments", response_model=List[PaymentResponse])
def get_my_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Payment)
        .join(Booking, Payment.booking_id == Booking.id)
        .filter(Booking.user_id == current_user.id)
        .all()
    )

# Xem chi tiết 1 payment
@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy payment")

    booking = db.query(Booking).filter(Booking.id == payment.booking_id).first()
    if not current_user.is_admin and (not booking or booking.user_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền xem payment này")
    return payment

# Tạo payment cho 1 booking (user tự tạo khi thanh toán)
@router.post("/", response_model=PaymentResponse)
def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == payment_data.booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy booking")

    if booking.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thanh toán booking này")

    if booking.status == "cancelled":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Booking đã bị hủy, không thể thanh toán")

    existing = db.query(Payment).filter(
        Payment.booking_id == booking.id,
        Payment.status.in_(["pending", "completed"])
    ).first()
    if existing:
        detail = "Booking này đã được thanh toán" if existing.status == "completed" \
            else "Booking này đã có yêu cầu thanh toán đang chờ xác nhận"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    new_payment = Payment(
        booking_id=booking.id,
        amount=booking.total_price,
        method=payment_data.method,
        status="pending"
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

# Cập nhật trạng thái payment (chỉ admin xác nhận đã thanh toán / hoàn tiền)
@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy payment")

    payment.status = payment_data.status
    if payment_data.transaction_code:
        payment.transaction_code = payment_data.transaction_code

    if payment_data.status == "completed":
        payment.paid_at = datetime.now()
        # Khi thanh toán xong thì xác nhận luôn booking
        booking = db.query(Booking).filter(Booking.id == payment.booking_id).first()
        if booking and booking.status == "pending":
            booking.status = "confirmed"

    db.commit()
    db.refresh(payment)
    return payment