import os

import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI

from app.api.api import api_router

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))


app = FastAPI()
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    print(os.getenv("SERVER_HOST"))
    uvicorn.run(app, host=os.getenv("SERVER_HOST"), port=int(os.getenv("SERVER_PORT")))
