from currencies.utils import update_currencies, get_currencies

MOCK_CURRENCIES = {'EUR': 1, 'USD': 1.1332, 'GBP': 0.8976, 'RUB': 79.0434, 'BTC': 0.00012}


async def test_update_currencies(test_cli, database, mocker):
    get_from_mock = mocker.patch('currencies.utils.get_from_url')
    get_from_mock.return_value = MOCK_CURRENCIES

    resp = await update_currencies(database)

    currencies = await get_currencies(database)
    assert currencies['USD']['rate'] == MOCK_CURRENCIES['USD'], currencies['USD']
