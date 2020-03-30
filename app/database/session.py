import databases
from app.core import config
database = databases.Database(url=config.DATABASE_URL, ssl='allow')
