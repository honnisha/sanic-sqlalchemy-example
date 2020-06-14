import pytest
from currencies.models import currencies
from currencies.utils import update_currencies
from sqlalchemy.sql import select

MOCK_CURRENCIES = {'EUR': 1, 'USD': 1.12554, 'GBP': 0.897238, 'RUB': 78.49708, 'BTC': 0.000119}


async def test_update_currencies(test_cli, database, mocker):
    get_from_mock = mocker.patch('currencies.utils.get_from_url')
    async def mock_get_from_mock():
        return MOCK_CURRENCIES
    get_from_mock.return_value = mock_get_from_mock()

    resp = await update_currencies(database)

    query = select([currencies]).where(currencies.c.currency == 'USD')
    currency = await database.fetch_one(query)
    print(dict(currency))
    assert currency['rate'] == MOCK_CURRENCIES['USD'], currency['rate']
