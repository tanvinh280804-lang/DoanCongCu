from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse
from app.routers.auth import get_current_user, get_admin_user
from app.models.user import User

router = APIRouter()

# Lấy danh sách tất cả phòng (ai cũng xem được)
@router.get("/", response_model=List[RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    rooms = db.query(Room).all()
    return rooms

# Lấy thông tin 1 phòng theo id
@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy phòng"
        )
    return room

# Tạo phòng mới (chỉ admin)
@router.post("/", response_model=RoomResponse)
def create_room(
    room_data: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    new_room = Room(
        name=room_data.name,
        description=room_data.description,
        price=room_data.price,
        capacity=room_data.capacity,
        image_url=room_data.image_url or ""
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

# Cập nhật phòng (chỉ admin)
@router.put("/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: int,
    room_data: RoomUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy phòng"
        )

    # Chỉ cập nhật các trường được gửi lên
    update_data = room_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(room, field, value)

    db.commit()
    db.refresh(room)
    return room

# Xóa phòng (chỉ admin)
@router.delete("/{room_id}")
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy phòng"
        )
    db.delete(room)
    db.commit()
    return {"message": "Xóa phòng thành công"}