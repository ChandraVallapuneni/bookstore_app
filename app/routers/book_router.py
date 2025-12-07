from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.book_model import Book
from app.schemas.book_schema import BookCreate, BookResponse
from app.routers.auth_router import get_current_user


router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):

    # 1. Check if book with same title exists
    result = await db.execute(select(Book).where(Book.title == book.title))
    existing_book = result.scalar_one_or_none()

    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this title already exists"
        )

    # 2. Create new book object
    new_book = Book(
        title=book.title,
        author=book.author,
        price=book.price,
        pages=book.pages,
        description=book.description
    )

    # 3. Save to DB
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)

    return new_book

@router.get("/", response_model=list[BookResponse])
async def get_all_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    books = result.scalars().all()
    return books

@router.get("/{book_id}", response_model=BookResponse)
async def get_book_by_id(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    return book

@router.put("/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, updated_book: BookCreate, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):

    # 1. Find existing book
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # 2. Update fields
    book.title = updated_book.title
    book.author = updated_book.author
    book.price = updated_book.price
    book.pages = updated_book.pages
    book.description = updated_book.description

    # 3. Commit
    await db.commit()
    await db.refresh(book)

    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):

    # 1. Find book
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # 2. Delete
    await db.delete(book)
    await db.commit()

    return
