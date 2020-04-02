# Import all the models, so that Base has them before being
# imported by Alembic
from app.database.base import Base
from app.models.user import User
from app.models.exercise import Exercise
