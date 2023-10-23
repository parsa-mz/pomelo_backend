# Pomelo 

### Introduction

The project is consisted of two apps `users` and `transactions`. The `users` app is responsible for user authentication and the transactions app is responsible for creating and listing transactions. 

The project uses [FastAPI](https://fastapi.tiangolo.com/) as the web framework and [SQLAlchemy](https://www.sqlalchemy.org/) as the ORM.


## Installation

For this you need to have Python 3.8 or higher installed. [Click here](https://www.python.org/downloads/) to download
Python.

Create a virtual environment:

```bash
# create a virtual environment
python -m venv venv

# activate the virtual environment
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

For the database, you need to have [PostgreSQL](https://www.postgresql.org/) installed. [Click here](https://www.postgresql.org/download/) to download PostgreSQL. But I also added a cloud database for testing purposes.

## Usage

To run the application:

```bash
uvicorn main:app --reload
```

## API Documentation

To view the API documentation, go to `http://localhost:8000/docs` in your browser after running the application.



## Project Structure
- Each app has a separate logic than others and contains its own models, endpoints, and services.
```
/app
├── models.py
├── schemas.py
├── routes.py
└── services.py
```

## Testing

This project uses [pytest](https://docs.pytest.org/en/stable/) for testing. To run the tests:

```bash
pytest
```

## Notes and how to use 
1. Create a user by just giving a `name`. After creating a user, you will get a `token` which you can use to authenticate yourself in the next steps. 
2. Past the JWT token on the top right corner of the page and click on `Authorize` button. (or use it in Postman)
3. Since the project is designed for event-driven architecture, you can create a list transactions (1 or many) by sending a POST request to `/transactions` endpoint.
4. The system loads transactions and then writes back in the end to minimize the number of database queries.
5. In the end user `credit` and `payable` is also updated + any transaction with their `user_id`.
6. App is dockerized and is fully ready to be deployed on any cloud provider.


## Author:

Parsa Mazaheri, Oct 2023

