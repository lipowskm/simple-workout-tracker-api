from fastapi import APIRouter

from app.api import user, login, test

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(test.router, prefix="/tests", tags=["tests"])
