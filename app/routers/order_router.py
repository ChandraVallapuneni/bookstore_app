from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.order_model import Order
from app.models.user_model import User
from app.models.book_model import Book
from app.schemas.order_schema import OrderCreate, OrderResponse
from app.routers.auth_router import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):

    # 1. Check if user exists
    user_result = await db.execute(select(User).where(User.id == order.user_id))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 2. Check if book exists
    book_result = await db.execute(select(Book).where(Book.id == order.book_id))
    book = book_result.scalar_one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # 3. Calculate total price
    total_price = order.quantity * book.price

    # 4. Create new order
    new_order = Order(
        user_id=order.user_id,
        book_id=order.book_id,
        quantity=order.quantity,
        total_price=total_price
    )

    # 5. Save to DB
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    return new_order

@router.get("/", response_model=list[OrderResponse])
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order))
    orders = result.scalars().all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_by_id(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return order

@router.get("/user/{user_id}", response_model=list[OrderResponse])
async def get_orders_by_user(user_id: int, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    result = await db.execute(select(Order).where(Order.user_id == user_id))
    orders = result.scalars().all()
    return orders

@router.get("/book/{book_id}", response_model=list[OrderResponse])
async def get_orders_by_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.book_id == book_id))
    orders = result.scalars().all()
    return orders

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):

    # 1. Find the order
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # 2. Delete the order
    await db.delete(order)
    await db.commit()

    return
