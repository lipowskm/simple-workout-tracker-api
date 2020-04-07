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
EMAIL_RESET_TOKEN_EXPIRE_MINUTES = 15
EMAIL_NEW_ACCOUNT_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = os.getenv("DATABASE_URL")
EMAILS_ENABLED = get_env_boolean("EMAILS_ENABLED", True)
EMAIL_TEMPLATES_DIR = "./app/email-templates"
PROJECT_NAME = os.getenv("PROJECT_NAME")
EMAILS_FROM_EMAIL = os.getenv("EMAILS_FROM_EMAIL")
EMAILS_FROM_NAME = PROJECT_NAME
SECRET_KEY = os.getenv("SECRET_KEY")
SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS")
SMTP_TLS = get_env_boolean("SMTP_TLS", True)
SMTP_PORT = None
_SMTP_PORT = os.getenv("SMTP_PORT")
if _SMTP_PORT is not None:
    SMTP_PORT = int(_SMTP_PORT)
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SUPERUSER = os.getenv("SUPERUSER")
SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD")
