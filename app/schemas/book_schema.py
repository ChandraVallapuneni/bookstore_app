from pydantic import BaseModel, EmailStr
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str
    price: float
    pages: int
    description: str | None = None              #Also, can write as -->description: Optional[str] (and we need to import Optional)

class BookCreate(BookBase):
    pass 

class BookResponse(BookBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
