import logging
import re

from asyncpg import UniqueViolationError
from currencies.models import CurrenciesEnum
from sanic import Blueprint, response
from sqlalchemy.sql import select
from users.models import users
from users.utils import (
    create_user, generate_password_hash, login_required, verify_password)

logger = logging.getLogger('users')

users_blueprint = Blueprint('users_blueprint', url_prefix='/api')

LOGIN_DATA_ERROR = "Provide email, password for login"
AUTH_ERROR_MESSAGE = "An account could not be found for the provided username and password"
NO_DATA_ERROR = "No data provided"
ALREADY_EXSITS_ERROR = "User with this email already exsits"


@users_blueprint.route('/register', methods=['POST'])
async def register(request):
    if not request.json:
        return response.text(NO_DATA_ERROR, status=400)

    email = request.json.get('email')
    if not email or not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return response.text("Not valid email", status=400)

    password = request.json.get('password')
    if not password or 6 > len(password) or len(password) > 64:
        return response.text("Not valid password, must be between 6 and 64 symbols", status=400)

    currency_choices = list(map(lambda c: c.value, CurrenciesEnum))
    currency = request.json.get('currency')
    if not currency or currency.upper() not in currency_choices:
        return response.text(f"Not valid, must be in {currency_choices}", status=400)
    currency = currency.upper()

    database = request.app.config['database']
    try:

        user_id = await create_user(
            database, email, 0.0, currency, password
        )

        # Save in session
        request.ctx.session['user_id'] = user_id

    except UniqueViolationError:
        return response.text(ALREADY_EXSITS_ERROR, status=400)

    return response.text("Registered")


@users_blueprint.route('/login', methods=['POST'])
async def login(request):
    if not request.json:
        return response.text(NO_DATA_ERROR, status=401)

    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return response.text(LOGIN_DATA_ERROR, status=401)

    database = request.app.config['database']
    query = select([users]).where(users.c.email == email)
    user = await database.fetch_one(query=query)

    if user and verify_password(dict(user)['password_hash'], password):

        # Save in session
        request.ctx.session['user_id'] = dict(user)['id']
        return response.text("Logged in successfully")

    return response.text(AUTH_ERROR_MESSAGE, status=401)


@users_blueprint.route('/logout')
@login_required()
async def logout(request):

    # Remove from session
    del request.ctx.session['user_id']
    return response.text("Logged out successfully")
