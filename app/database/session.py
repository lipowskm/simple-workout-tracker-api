import os

import databases
from dotenv import load_dotenv

from app.core import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))

database = databases.Database(url=config.DATABASE_URL, ssl='allow')
