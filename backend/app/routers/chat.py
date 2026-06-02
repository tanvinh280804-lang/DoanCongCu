from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from app.services.chat_service import get_chat_response
from app.routers.auth import get_current_user
from app.models.user import User
from app.models.room import Room
from app.database import get_db

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    reply: str

def get_room_info(db: Session) -> str:
    rooms = db.query(Room).all()
    if not rooms:
        return "Hiện chưa có phòng nào."
    return "\n".join([
        f"- {r.name}: {r.price:,.0f}đ/đêm, sức chứa {r.capacity} người, "
        f"{'còn phòng' if r.is_available else 'hết phòng'}. "
        f"Mô tả: {r.description or 'Không có mô tả'}"
        for r in rooms
    ])

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    room_info = get_room_info(db)
    history = [
        {"role": msg.role, "content": msg.content}
        for msg in request.history
    ]
    reply = get_chat_response(request.message, history, room_info)
    return {"reply": reply}

@router.post("/authenticated", response_model=ChatResponse)
def chat_authenticated(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    room_info = get_room_info(db)
    history = [
        {"role": msg.role, "content": msg.content}
        for msg in request.history
    ]
    message_with_name = f"[Khách hàng: {current_user.full_name}] {request.message}"
    reply = get_chat_response(message_with_name, history, room_info)
    return {"reply": reply}