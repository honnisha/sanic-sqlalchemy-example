import json

import redis
from redis import ConnectionPool

import aiohttp
from currencies.models import CurrenciesEnum, currencies
from databases import Database
from sqlalchemy.sql import bindparam, select

# UPDATE_URL = 'https://api.exchangeratesapi.io/latest?symbols={}'
KEY = '6f2c32c1c903969dcfc7554bde8236be'
UPDATE_URL = 'http://data.fixer.io/api/latest?access_key={key}&symbols={symbols}'


class RurrenciesZeroError(Exception):
    pass


async def get_from_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            return json.loads(text)['rates']


async def update_currencies(database, redis_pool=None):
    currency_choices = list(map(lambda c: c.value, CurrenciesEnum))
    currency_choices[currency_choices.index('GPB')] = 'GBP'

    url = UPDATE_URL.format(symbols=','.join(currency_choices), key=KEY)
    data = await get_from_url(url)

    if not data:
        raise Exception(f'No data from {url}')

    # Update rate
    for currency, rate in data.items():
        if currency == 'GBP':
            currency = 'GPB'

        query = currencies.update().where(currencies.c.currency == currency).values(rate=rate)
        updated = await database.execute(query, {'rate': rate, 'currency': currency})

    if redis_pool:
        conn = redis.Redis(connection_pool=redis_pool)
        conn.delete('currencies')


async def get_currencies(database: Database, redis_pool: ConnectionPool=None) -> dict:
    if redis_pool:
        conn = redis.Redis(connection_pool=redis_pool)

        currencies_data = conn.get('currencies')
        if currencies_data:
            return json.loads(currencies_data)

    query = select([currencies])
    result = await database.fetch_all(query)
    currencies_data = {c['currency']: {'rate': c['rate'], 'id': c['id'] } for c in result}

    zero_currencies = [
        curr for curr, data in currencies_data.items() if not data['rate']
    ]
    if zero_currencies:
        raise RurrenciesZeroError(f'Found currencies with 0 rate: {zero_currencies}. Call currencies.utils.update_currencies for update rates.')

    if redis_pool:
        return conn.set("currencies", json.dumps(currencies_data))

    return currencies_data
