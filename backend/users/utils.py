import binascii
import hashlib
import os
from decimal import Decimal, getcontext
from functools import wraps

from redis import ConnectionPool

from currencies.convertate import convert
from currencies.models import currencies
from currencies.utils import get_currencies
from databases import Database
from sanic import response
from sqlalchemy.sql import select
from transfers.models import transactions
from users.models import users


async def transfer_money(database: Database, redis_pool: ConnectionPool, user: dict, target_user: dict, value: Decimal) -> int:
    context = getcontext()
    context.prec = 5

    async with database.transaction():
        currencies_data = await get_currencies(database, redis_pool)
        currencies = {data['id']: curr for curr, data in currencies_data.items()}

        currency_form = currencies[user['currency_id']]
        currency_to = currencies[target_user['currency_id']]

        query = users.update().where(users.c.id == user['id'])
        balance = Decimal(user['_balance'])
        sender_new_balance = balance - value
        await database.execute(query, {'_balance': sender_new_balance})
        
        value_in_target_currency = await convert(
            value, currency_form, currency_to, database
        )
        query = users.update().where(users.c.id == target_user['id'])
        target_balance = Decimal(target_user['_balance'])
        target_new_balance = target_balance + value_in_target_currency
        await database.execute(query, {'_balance': target_new_balance})

        transactions.insert().values(
            sender_id=user['id'],
            sender_new_balance=sender_new_balance,

            target_id=target_user['id'],
            target_new_balance=target_new_balance,

            currency_id=user['currency_id']
        )
        return await database.execute(query, {'_balance': target_new_balance})


def generate_password_hash(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512', password.encode('utf-8'), salt, 100000
    )
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512', password.encode('utf-8'), salt.encode('ascii'), 100000
    )
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


async def create_user(database: Database, email: str, balance: float, currency: str, password: str) -> int:
    query = select([currencies]).where(currencies.c.currency == currency)
    currency_id = await database.execute(query=query)

    return await database.execute(
        query=users.insert(),
        values={
            "email": email,
            "_balance": balance,
            "currency_id": currency_id,
            "password_hash": generate_password_hash(password),
        }
    )

def login_required(insert_user=False):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authorized = request.ctx.session.get('user_id')

            if is_authorized:

                if insert_user:
                    database = request.app.config['database']

                    user_id = request.ctx.session['user_id']
                    query = select([users]).where(users.c.id == user_id)
                    user = await database.fetch_one(query=query)
                    return await f(request, user, *args, **kwargs)

                return await f(request, *args, **kwargs)
            else:
                # the user is not authorized.
                return response.text('Not authorized', status=403)
        return decorated_function
    return decorator
