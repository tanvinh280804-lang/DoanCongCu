from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id     = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    check_in    = Column(String, nullable=False)
    check_out   = Column(String, nullable=False)
    total_price = Column(Float)
    status      = Column(String, default="pending")
    guest_name  = Column(String)
    guest_phone = Column(String)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    room = relationship("Room")