from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String, nullable=False)
    description  = Column(String)
    price        = Column(Float, nullable=False)
    capacity     = Column(Integer, default=2)
    image_url    = Column(String, default="")
    is_available = Column(Boolean, default=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())