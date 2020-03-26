# Simple workout tracker API
API for workout tracker application.
Created with FastAPI and PostgreSQL database.

## Installation
Clone repo.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies from requirements file.

```bash
pip install -r requirements.txt
```

## Run server
Either run main.py, or run the following command:

```bash
uvicorn main:app
```

To make the server reload after making changes, add the parameter:

```bash
uvicorn main:app --reload
```

## Database migration
After any changes or additions in database structure, new [alembic](https://pypi.org/project/alembic/) revision has to be created using the following command:

```bash
alembic revision --autogenerate -m "example message"
```

And then to upgrade the database to the newest revision:

```bash
alembic upgrade head"
```
