import os

import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from app.models.user import User
from app.schemas.user import UserBase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.getenv("DATABASE_URL"))


@app.post("/user", response_model=UserBase)
async def create_user(user: UserBase):
    db_user = User(
        first_name=user.first_name, last_name=user.last_name, email=user.email,
        is_active=user.is_active, is_superuser=user.is_superuser
    )
    db.session.add(db_user)
    db.session.commit()
    return db_user

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
