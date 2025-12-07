from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserResponse
from app.utils.hashing import get_password_hash   # FIXED: hashing, not hasing
from app.routers.auth_router import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):

    # 1. Check if user already exists
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()    # FIXED: add parentheses

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # 2. Hash password
    hashed_password = get_password_hash(user.password)

    # 3. Create user object
    new_user = User(
        name=user.name,          # FIXED commas
        email=user.email,
        password=hashed_password
    )

    # 4. Commit to DB
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@router.get("/", response_model= list[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users 

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )
    
    return user 