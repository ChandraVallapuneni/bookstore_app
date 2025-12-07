📚 FastAPI Bookstore API

A complete backend API built with FastAPI, PostgreSQL, SQLAlchemy Async, and JWT Authentication.

🚀 Features
🔐 Authentication

User Registration

User Login with JWT

Protected Routes using Bearer Token

👤 Users

Create user

Get all users

Get user by ID

📘 Books

Create Book (auth required)

Get all books (public)

Get book by ID (public)

Update Book (auth required)

Delete Book (auth required)

🛒 Orders

Create Order (auth required)

Get all Orders (auth required)

Get Order by ID (auth required)

⭐ Reviews

Create Review (auth required)

Get all Reviews (public)

Get Review by ID (public)

🗃 Database

PostgreSQL

SQLAlchemy Async ORM

Automatic table creation on startup

🏗 Project Structure
bookstore_app/
│── app/
│   ├── main.py
│   ├── database.py
│   ├── config/
│   │     └── settings.py
│   ├── models/
│   │     ├── user_model.py
│   │     ├── book_model.py
│   │     ├── order_model.py
│   │     └── review_model.py
│   ├── routers/
│   │     ├── user_router.py
│   │     ├── book_router.py
│   │     ├── order_router.py
│   │     ├── review_router.py
│   │     └── auth_router.py
│   ├── schemas/
│   │     ├── user_schema.py
│   │     ├── book_schema.py
│   │     ├── order_schema.py
│   │     ├── review_schema.py
│   │     └── auth_schema.py
│   └── utils/
│         ├── hashing.py
│         └── token.py
│
├── requirements.txt
├── README.md
└── .env

🧪 Tech Stack

FastAPI

PostgreSQL

SQLAlchemy Async (asyncpg)

Pydantic v2

JWT Authentication

Uvicorn

🔧 Setup Instructions
1️⃣ Clone Repo
git clone https://github.com/ChandraVallapuneni/bookstore_app.git
cd bookstore_app

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Create .env file
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/bookstoredb
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256

5️⃣ Run Server
python -m uvicorn app.main:app --reload

🔐 Authentication Flow
1. Register User

POST /users/

2. Login

POST /auth/login

Response:

{
  "access_token": "your-jwt-token"
}

3. Use Token for Protected Routes

Click Authorize → paste token → now you can:

Create books

Update books

Create orders

Add reviews

🧠 Learning Highlights

This project includes:

Async DB operations

HTTPBearer JWT authentication

Relationships (User → Orders → Books → Reviews)

Proper schema separation

Clean folder structure

Error handling & validations
