Project is example of usage Sanic framework with Postgresql async SQLAlchemy core (not orm). Alembic is used for migrations.

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

To run tests:
```shell
docker exec -it transfer-system_backend_1 python -m unittest discover
```

Command for update currencies exchange rate:
```shell
docker exec -it transfer-system_backend_1 python update_currencies.py
```
