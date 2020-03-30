import logging

from app.database.init_database import init_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init():
    logger.info("Creating initial data")
    await init_database()
    logger.info("Initial data created")
