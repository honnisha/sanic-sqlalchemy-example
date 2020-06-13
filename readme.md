Project is example of usage Sanic framework with Postgresql async SQLAlchemy core (not orm). 
Alembic is used for migrations.
PostgreSQL in Docker is configured for two databases, one is used for tests.


To run in Docker:
```shell
sudo docker-compose build
sudo docker-compose up
```

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

To run tests:
```shell
sudo docker exec -it transfer-system_backend_1 pytest tests.py
```

Command for update currencies exchange rate:
```shell
docker exec -it transfer-system_backend_1 python update_currencies.py
```
