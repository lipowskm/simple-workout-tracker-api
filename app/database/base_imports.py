# Import all the models, so that Base has them before being
# imported by Alembic
from app.database.base import Base  # noqa
from app.models.user import User  # noqa
