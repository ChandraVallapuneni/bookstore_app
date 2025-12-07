from fastapi import FastAPI
from app.database import init_db
from app.routers.user_router import router as users_router
from app.routers.book_router import router as books_router
from app.routers.order_router import router as orders_router
from app.routers.review_router import router as reviews_router
from app.routers.auth_router import router as auth_router

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()  # <-- THIS CREATES ALL TABLES

app.include_router(users_router)
app.include_router(books_router)
app.include_router(orders_router)
app.include_router(reviews_router)
app.include_router(auth_router)
