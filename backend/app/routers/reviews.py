from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.review import Review
from app.models.booking import Booking
from app.models.room import Room
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from app.routers.auth import get_current_user, get_admin_user
from app.models.user import User

router = APIRouter()

# Lấy tất cả đánh giá của 1 phòng (public, ai cũng xem được)
@router.get("/room/{room_id}", response_model=List[ReviewResponse])
def get_reviews_by_room(
    room_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Review).filter(Review.room_id == room_id).all()

# Lấy đánh giá của user hiện tại
@router.get("/my-reviews", response_model=List[ReviewResponse])
def get_my_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Review).filter(Review.user_id == current_user.id).all()

# Tạo đánh giá mới (chỉ cho phòng mà user đã từng đặt và đã trả phòng)
@router.post("/", response_model=ReviewResponse)
def create_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == review_data.booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy booking")

    if booking.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền đánh giá booking này")

    if booking.status != "checked_out":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chỉ có thể đánh giá sau khi đã trả phòng"
        )

    existing = db.query(Review).filter(Review.booking_id == booking.id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Booking này đã được đánh giá rồi")

    new_review = Review(
        user_id=current_user.id,
        room_id=booking.room_id,
        booking_id=booking.id,
        rating=review_data.rating,
        comment=review_data.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# Sửa đánh giá của chính mình
@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy đánh giá")

    if review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền sửa đánh giá này")

    if review_data.rating is not None:
        review.rating = review_data.rating
    if review_data.comment is not None:
        review.comment = review_data.comment

    db.commit()
    db.refresh(review)
    return review

# Xóa đánh giá (chủ đánh giá hoặc admin)
@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy đánh giá")

    if review.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền xóa đánh giá này")

    db.delete(review)
    db.commit()
    return {"message": "Đã xóa đánh giá thành công"}