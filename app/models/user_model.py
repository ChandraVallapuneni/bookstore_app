from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String, nullable = False)
    email: Mapped[str] = mapped_column(String, nullable = False, unique = True, index = True)
    password: Mapped[str] = mapped_column(String, nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default = datetime.utcnow)

    orders = relationship("Order", back_populates = "user")
    reviews = relationship("Review", back_populates = "user")

