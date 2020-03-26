# Simple workout tracker API
API for workout tracker application.
Created with FastAPI and PostgreSQL database.

## Installation
Clone repo.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies from requirements file.

```bash
pip install -r requirements.txt
```

## Environmental variables
Before running the server, `.env` file with input variables needs to be created in project root directory, like so:

```text
VAR1_NAME=VAR1_VALUE
VAR2_NAME=VAR2_VALUE
...
```

Variables list:

* `DATABASE_URL`: URL of PostgreSQL database. Syntax:
```text
postgres://username:password:@server_address/database_name
```

Include this only if running server by executing `main.py`:

* `SERVER_HOST`: Server address. Use `0.0.0.0` to make application available on local network.
* `SERVER_PORT`: Server port number, e.g. `8000`

## Run server
Either run `main.py`, or run the following command from root directory:

```bash
uvicorn app.main:app
```

To make the server reload after making changes, add the parameter:

```bash
uvicorn app.main:app --reload
```

## API documentation

After running the server, API documentation is available under:

```
http://SERVER_HOST:SERVER:PORT/docs
```

## Database migration
After any changes or additions in database structure, new [alembic](https://pypi.org/project/alembic/) revision has to be created using the following command:

```bash
alembic revision --autogenerate -m "example message"
```

And then to upgrade the database to the newest revision:

```bash
alembic upgrade head
```
