from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user_model import User
from app.schemas.auth_schema import LoginSchema, TokenResponse
from app.utils.hashing import verify_password
from app.utils.token import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# Bearer scheme to read token from the Authorization header
bearer_scheme = HTTPBearer()

# Load JWT settings
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")


# -------------------- LOGIN ENDPOINT --------------------
@router.post("/login", response_model=TokenResponse)
async def login_user(credentials: LoginSchema, db: AsyncSession = Depends(get_db)):

    # 1. Check if user exists
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email or password"
        )

    # 2. Verify password
    if not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 3. Create JWT token
    token = create_access_token({"sub": user.email})

    # 4. Return token
    return TokenResponse(access_token=token)


# -------------------- GET CURRENT USER (JWT DECODE) --------------------
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials  # Extract raw JWT token string

    # 1. Decode and validate JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")

        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    # 2. Fetch user from DB
    result = await db.execute(select(User).where(User.email == user_email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        )

    return user
