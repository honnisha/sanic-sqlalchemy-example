import re
from decimal import Decimal

from sanic import Blueprint, response
from sanic_validation import validate_json
from transfers.json_validators import transfer_schema
from users.auth import login_required
from users.utils import get_user, transfer_money

transfers_blueprint = Blueprint('transfers_blueprint', url_prefix='/api')


@transfers_blueprint.route('/transfer', methods=['POST'])
@login_required(insert_user=True)
@validate_json(transfer_schema)
async def transfer(request, user):

    value = Decimal(request.json.get('value'))
    email = request.json.get('email')

    if user['email'] == email:
        return response.json(
            {'error': {'message': "You can't transfer money to yourself"}},
            status=400
        )

    balance = Decimal(user['_balance'])
    if value > balance:
        return response.json(
            {'error': {'message': "You don't have enough money on balance"}},
            status=400
        )

    database = request.app.config['database']

    target_user = await get_user(database, email=email)

    if not target_user:
        return response.json(
            {'error': {'message': "User with specified email not found"}},
            status=400
        )

    redis_pool = request.app.config['redis_pool']
    await transfer_money(database, redis_pool, user, target_user, value)

    return response.json({'message': 'Transfered'})
