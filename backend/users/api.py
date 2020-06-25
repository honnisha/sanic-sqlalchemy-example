import logging

from asyncpg import UniqueViolationError
from sanic import Blueprint, response
from sanic_validation import validate_json
from users.auth import login_required, user_auth_method
from users.utils import create_user, get_user, verify_hash
from users.json_validators import register_schema, login_schema

logger = logging.getLogger('users')

users_blueprint = Blueprint('users_blueprint', url_prefix='/api')


@users_blueprint.route('/register', methods=['POST'])
@validate_json(register_schema)
async def register(request):
    password = request.json.get('password')
    currency = request.json.get('currency')
    email = request.json.get('email')

    try:
        user_id = await create_user(
            request.app.config['database'], email, 100.0,
            currency.upper(), password
        )

        token = await user_auth_method().user_authorize(request, user_id, email)
        return response.json({
            'message': 'Registered successfully',
            'token': token
        })

    except UniqueViolationError:
        return response.json(
            {'error': {'message': 'User with this email already exsits'}},
            status=400
        )


@users_blueprint.route('/login', methods=['POST'])
@validate_json(login_schema)
async def login(request):

    email = request.json.get('email')
    password = request.json.get('password')

    database = request.app.config['database']
    user = await get_user(database, email=email)

    if user and verify_hash(dict(user)['password_hash'], password):

        token = await user_auth_method().user_authorize(request, dict(user)['id'], email)
        return response.json({
            'message': "Logged in successfully",
            'token': token
        })

    return response.json({'error': {'message': 'Login error'}}, status=401)


@users_blueprint.route('/logout')
@login_required()
async def logout(request):

    await user_auth_method().user_unauthorize(request)
    return response.json({'message': 'Logged out successfully'})
