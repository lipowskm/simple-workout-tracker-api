import logging

from app.database.init_database import init_database
from app.database.session import db_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init():
    logger.info("Creating initial data")
    init_database(db_session)
    logger.info("Initial data created")
