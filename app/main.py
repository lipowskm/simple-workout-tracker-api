import os

import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from app.api.api import api_router

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()
app.include_router(api_router, prefix="/api")
app.add_middleware(DBSessionMiddleware, db_url=os.getenv("DATABASE_URL"))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
