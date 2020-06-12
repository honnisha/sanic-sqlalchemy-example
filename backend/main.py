#!/usr/bin/env python3

from datetime import timedelta
from logging.config import dictConfig

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

import settings
from databases import Database
from sanic import Sanic
from sanic_session import InMemorySessionInterface, Session

dictConfig(settings.LOGGER_SETTINGS)

app = Sanic(__name__)

session = Session(app, interface=InMemorySessionInterface())

if not settings.SECRET_KEY:
    raise Exception('ERROR: SECRET_KEY is None')

app.config['SECRET_KEY'] = settings.SECRET_KEY

mainmetatadata = MetaData()
Base = declarative_base(metadata=mainmetatadata)


@app.listener('before_server_start')
async def register_db(app, loop):
    app.config['database'] = Database(settings.connection)
    await app.config['database'].connect()

@app.listener('before_server_stop')
async def register_db(app, loop):
    await app.config['database'].disconnect()

    
if __name__ == '__main__':
    from transfers.views import transfers_blueprint
    from users.views import users_blueprint
    app.register_blueprint(users_blueprint)
    app.register_blueprint(transfers_blueprint)

    app.run(
        settings.HOST_IP, int(settings.HOST_PORT),
        debug=bool(settings.DEBUG),
        auto_reload=bool(settings.DEBUG)
    )
