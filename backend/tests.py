import sys
import os
sys.path.insert(0, os.getcwd())

from main import create_app, app, Base
import pytest
import logging
import settings
import alembic.config

from users.tests.test import *


@pytest.yield_fixture
def sanic_app():
    logging.getLogger("databases").setLevel(logging.ERROR)

    # Apply migrate to test db
    db_url_arg = f'dburl={settings.test_connection}'
    alembic.config.main(argv=['-x', db_url_arg, 'upgrade', 'head'])

    create_app(settings.test_connection, run=False)

    # Rollback db
    alembic.config.main(argv=['-x', db_url_arg, 'downgrade', 'base'])
    
    yield app

@pytest.fixture
def test_cli(loop, sanic_app, sanic_client):
    return loop.run_until_complete(sanic_client(app))
