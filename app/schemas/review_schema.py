from pydantic import BaseModel
from datetime import datetime

class ReviewBase(BaseModel):
    rating: int
    comment: str | None = None

class ReviewCreate(ReviewBase):
    user_id: int
    book_id: int

class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    book_id: int
    created_at: datetime

    class Config:
        orm_mode = True
