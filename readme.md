# transfer-system

Project is example of usage Sanic framework with Databases package uses async SQLAlchemy core (not orm). 

Alembic is used for migrations.

PostgreSQL in Docker is configured for two databases, one is used for tests.

pytest-sanic and pytest-mock is used for tests.

Autorisation works with cookies.

Redis is used for cache.

## Usage

To run in Docker:
```shell
docker-compose build
docker-compose up
```

You can use backend with `http://0.0.0.0/api/`

## Migrations

To make and run migrations:
```shell
docker exec -it transfer-system_backend_1 alembic revision --autogenerate -m "name"

docker exec -it transfer-system_backend_1 alembic upgrade head
docker exec -it transfer-system_backend_1 alembic current
```
You can specify database url with flag:
```shell
alembic -x dburl=postgres://user:password@postgresql/db2 upgrade head
```

## Tests

To run tests:
```shell
docker exec -it transfer-system_backend_1 pytest tests.py
```

## Commands

Command for update currencies exchange rate:
```shell
docker exec -it transfer-system_backend_1 python update_currencies.py
```
