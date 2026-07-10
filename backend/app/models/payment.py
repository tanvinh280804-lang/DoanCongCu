from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id               = Column(Integer, primary_key=True, index=True)
    booking_id       = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    amount           = Column(Float, nullable=False)
    method           = Column(String, default="cash")       # cash / bank_transfer / momo
    status           = Column(String, default="pending")    # pending / completed / failed / refunded
    transaction_code = Column(String, nullable=True)
    paid_at          = Column(DateTime(timezone=True), nullable=True)
    created_at       = Column(DateTime(timezone=True), server_default=func.now())

    booking = relationship("Booking")