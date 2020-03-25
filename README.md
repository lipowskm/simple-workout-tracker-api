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
