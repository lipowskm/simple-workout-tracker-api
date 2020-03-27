import uvicorn
from fastapi import FastAPI

from app import init_data
from app.api.api import api_router
from app.core import config

init_data.init()
app = FastAPI()
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app, host=config.SERVER_HOST, port=config.SERVER_PORT)
