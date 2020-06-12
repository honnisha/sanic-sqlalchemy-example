import logging
import re

from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import select

from currencies.models import CurrenciesEnum
from sanic import Blueprint, response
from users.models import users, User
from users.utils import generate_password_hash, verify_password, login_required
from asyncpg import UniqueViolationError

logger = logging.getLogger('users')

users_blueprint = Blueprint('users_blueprint', url_prefix='/api')

LOGIN_DATA_ERROR = "Provide email, password for login"
AUTH_ERROR_MESSAGE = "An account could not be found for the provided username and password"


@users_blueprint.route('/register', methods=['POST'])
async def register(request):
    email = request.json.get('email')
    if not email or not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return response.text("Not valid email", status=400)

    password = request.json.get('password')
    if not password or 6 > len(password) or len(password) > 64:
        return response.text("Not valid password, must be between 6 and 64 symbols", status=400)

    currency_choices = list(map(lambda c: c.value, CurrenciesEnum))
    currency = request.json.get('currency')
    if not currency or currency not in currency_choices:
        return response.text(f"Not valid, must be in {currency_choices}", status=400)

    database = request.app.config['database']
    try:
        user_id = await database.execute(
            query=users.insert(),
            values={
                "email": email,
                "_balance": 0.0,
                "currency": currency,
                "password_hash": generate_password_hash(password),
            }
        )

        # Save in session
        request.ctx.session['user_id'] = user_id

    except UniqueViolationError:
        return response.text("User with this email already exsits", status=400)

    return response.text("Registered")
    
@users_blueprint.route('/login', methods=['POST'])
async def login(request):
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return response.text(LOGIN_DATA_ERROR)

    database = request.app.config['database']
    query = select([users]).where(users.c.email == email)
    user_id = await database.fetch_one(query=query)

    if user and verify_password(user.password_hash, password):

        # Save in session
        request.ctx.session['user_id'] = user_id
        return response.text("Logged in successfully")

    return response.text(AUTH_ERROR_MESSAGE)


@users_blueprint.route('/logout')
@login_required()
async def logout(request):

    # Remove from session
    del request.ctx.session['user_id']
    return response.text("Logged out successfully")
