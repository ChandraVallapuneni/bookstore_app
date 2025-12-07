from pydantic import BaseModel
from datetime import datetime

class OrderBase(BaseModel):
    quantity: int

class OrderCreate(OrderBase):
    user_id: int
    book_id: int

class OrderResponse(OrderBase):
    id: int
    user_id: int
    book_id: int
    total_price: float
    created_at: datetime

    class Config:
        orm_mode = True
