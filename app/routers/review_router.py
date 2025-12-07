from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.review_model import Review
from app.models.user_model import User
from app.models.book_model import Book
from app.schemas.review_schema import ReviewCreate, ReviewResponse
from app.routers.auth_router import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):

    # 1. Check user exists
    user_result = await db.execute(select(User).where(User.id == review.user_id))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 2. Check book exists
    book_result = await db.execute(select(Book).where(Book.id == review.book_id))
    book = book_result.scalar_one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # 3. Create new review
    new_review = Review(
        user_id=review.user_id,
        book_id=review.book_id,
        rating=review.rating,
        comment=review.comment
    )

    # 4. Save
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)

    return new_review

@router.get("/", response_model=list[ReviewResponse])
async def get_all_reviews(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review))
    reviews = result.scalars().all()
    return reviews

@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review_by_id(review_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    return review

@router.get("/book/{book_id}", response_model=list[ReviewResponse])
async def get_reviews_by_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).where(Review.book_id == book_id))
    reviews = result.scalars().all()
    return reviews

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_id: int, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    await db.delete(review)
    await db.commit()

    return
