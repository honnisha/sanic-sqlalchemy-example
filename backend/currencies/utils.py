import json

import aiohttp
from currencies.models import CurrenciesEnum, currencies
from sqlalchemy.sql import bindparam, select

# UPDATE_URL = 'https://api.exchangeratesapi.io/latest?symbols={}'
KEY = '6f2c32c1c903969dcfc7554bde8236be'
UPDATE_URL = 'http://data.fixer.io/api/latest?access_key={key}&symbols={symbols}'


async def get_from_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            return json.loads(text)['rates']


async def update_currencies(database):
    currency_choices = list(map(lambda c: c.value, CurrenciesEnum))
    currency_choices[currency_choices.index('GPB')] = 'GBP'

    url = UPDATE_URL.format(symbols=','.join(currency_choices), key=KEY)
    data = await get_from_url(url)

    if not data:
        raise Exception(f'No data from {url}')

    # Update rate
    for currency, rate in data.items():
        query = currencies.update().where(currencies.c.currency == currency).values(rate=rate)
        updated = await database.execute(query, {'rate': rate, 'currency': currency})
