#!/usr/bin/env python3

from datetime import timedelta
from logging.config import dictConfig

import settings
from sanic import Sanic
from sanic_auth import Auth

dictConfig(settings.LOGGER_SETTINGS)

app = Sanic(__name__)

if not settings.SECRET_KEY:
    raise Exception('ERROR: SECRET_KEY is None')

app.config['SECRET_KEY'] = settings.SECRET_KEY

auth = Auth(app)
app.config['AUTH_LOGIN_ENDPOINT'] = 'login'


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
