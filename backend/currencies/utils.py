import json

from sqlalchemy.sql import select
from sqlalchemy.sql.expression import bindparam

import aiohttp
from databases import Database
import settings
from currencies.models import CurrenciesEnum, currencies

# UPDATE_URL = 'https://api.exchangeratesapi.io/latest?symbols={}'
KEY = '6f2c32c1c903969dcfc7554bde8236be'
UPDATE_URL = 'http://data.fixer.io/api/latest?access_key={key}&symbols={symbols}'


async def update_currencies():
    currency_choices = list(map(lambda c: c.value, CurrenciesEnum))
    currency_choices[currency_choices.index('GPB')] = 'GBP'

    url = UPDATE_URL.format(symbols=','.join(currency_choices), key=KEY)
    print(url)

    data = {}
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            data = json.loads(text)['rates']

    if data:
        database = Database(settings.connection)
        await database.connect()

        # Get existed currencies
        query = select([currencies])
        currencies_records = [r['currency'] for r in await database.fetch_all(str(query))]

        cs = [
            {'currency': title if title != 'GBP' else 'GPB', 'rate': value}
            for title, value in data.items()
        ]

        # Create if not exist
        await database.execute_many(
            currencies.insert(),
            [c for c in cs if c['currency'] not in currencies_records]
        )
        # Or update rate
        await database.execute_many(
            currencies.update(),
            [{"rate": c["rate"]} for c in cs if c['currency'] in currencies_records]
        )
        database.disconnect()
