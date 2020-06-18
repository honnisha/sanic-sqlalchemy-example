import re
from decimal import Decimal

from sanic import Blueprint, response
from sqlalchemy.sql import select
from transfers.models import transactions
from users.models import users
from users.utils import login_required, transfer_money
from users.views import NO_DATA_ERROR

NOT_VALID_EMAIL = "Not valid targer email"
NOT_ENOUGH_MONEY = "You don't have enough money on balance"
USER_EMAIL_NOT_FOUND = "User with specified email not found"

transfers_blueprint = Blueprint('transfers_blueprint', url_prefix='/api')


@transfers_blueprint.route('/transfer', methods=['POST'])
@login_required(insert_user=True)
async def transfer(request, user):
    if not request.json:
        return response.text(NO_DATA_ERROR, status=400)

    value_str = request.json.get('value')
    if not value_str or float(value_str) <= 0:
        return response.text("Not valid value to transfer", status=400)
    value = Decimal(value_str)

    balance = Decimal(user['_balance'])
    if value > balance:
        return response.text(NOT_ENOUGH_MONEY, status=400)

    email = request.json.get('email')
    if not email or not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return response.text(NOT_VALID_EMAIL, status=400)

    database = request.app.config['database']

    user_id = request.ctx.session['user_id']
    query = select([users]).where(users.c.email == email)
    target_user = await database.fetch_one(query=query)

    if not target_user:
        return response.text(USER_EMAIL_NOT_FOUND, status=400)

    redis_pool = request.app.config['redis_pool']
    await transfer_money(database, redis_pool, user, target_user, value)

    return response.text("Transfered")
