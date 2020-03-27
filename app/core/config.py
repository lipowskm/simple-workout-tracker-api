import os

from dotenv import load_dotenv, find_dotenv


def get_env_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


load_dotenv(find_dotenv())


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
SUPERUSER = os.getenv("SUPERUSER")
SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD")
SUPERUSER_EMAIL = "admin@admin.com"
