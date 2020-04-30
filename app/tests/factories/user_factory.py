from datetime import datetime

import factory

from app.models.user import User
from app.schemas.user import UserCreate


class UserFactory(factory.Factory):
    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    hashed_password = factory.Faker('sha256')
    date_created = factory.LazyFunction(datetime.utcnow)
    is_active = True
    is_email_verified = True
    is_superuser = False

    class Meta:
        model = User


class UserCreateFactory(factory.Factory):
    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
    is_active = True
    is_email_verified = True
    is_superuser = False

    class Meta:
        model = UserCreate
