from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentCreate(BaseModel):
    booking_id: int
    method: str = "cash"  # cash / bank_transfer / momo

class PaymentUpdate(BaseModel):
    status: str              # pending / completed / failed / refunded
    transaction_code: Optional[str] = None

class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    amount: float
    method: str
    status: str
    transaction_code: Optional[str]
    paid_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True