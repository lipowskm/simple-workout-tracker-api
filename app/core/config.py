import os
from dotenv import load_dotenv


def get_env_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
load_dotenv(os.path.join(BASE_DIR, ".env"))

DATABASE_URL=os.getenv("DATABASE_URL")
SERVER_HOST=os.getenv("SERVER_HOST")
SERVER_PORT=int(os.getenv("SERVER_PORT"))