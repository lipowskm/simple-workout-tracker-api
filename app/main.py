import time
from urllib.request import Request

import uvicorn
from fastapi import FastAPI

from app import init_data
from app.api.api import api_router
from app.core import config
from app.database.session import database


app = FastAPI(title='Simple Workout Tracker API')
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup():
    await database.connect()
    await init_data.init()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host=config.SERVER_HOST, port=config.SERVER_PORT)
