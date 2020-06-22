import sys
import os
sys.path.insert(0, os.getcwd())

from main import create_app, app
import pytest
import logging
import settings
import alembic.config

from users.tests.test_api import *
from currencies.tests.test_utils import *
from currencies.tests.tests_converate import *
from transfers.tests.test_transfer import *


@pytest.yield_fixture(scope="session")
def sanic_app():
    logging.getLogger('databases').setLevel(logging.ERROR)

    # Apply migrate to test db
    db_url_arg = f'dburl={settings.test_connection}'
    alembic.config.main(argv=['-x', db_url_arg, 'upgrade', 'head'])

    # Rollback after each connect_db from before_server_start
    create_app(
        settings.test_connection, run=False,
        force_rollback=True, redis_use=False
    )
    yield app

    # Rollback db
    alembic.config.main(argv=['-x', db_url_arg, 'downgrade', 'base'])


@pytest.fixture
def test_cli(loop, sanic_app, sanic_client):
    return loop.run_until_complete(sanic_client(app))


@pytest.fixture
def database(loop, sanic_app, sanic_client):
    return sanic_app.config['database']
