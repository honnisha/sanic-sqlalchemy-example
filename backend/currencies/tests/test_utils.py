import pytest
from currencies.utils import (RurrenciesZeroError, get_currencies,
                              update_currencies)

MOCK_CURRENCIES = {'EUR': 1, 'USD': 1.1332, 'GBP': 0.8976, 'RUB': 79.0434, 'BTC': 0.00012}


async def test_update_currencies(test_cli, database, mocker):

    # Test that get_currencies will fail if currensies not set
    with pytest.raises(RurrenciesZeroError) as error:
        await get_currencies(database)
        assert 'get_currencies must failed with RurrenciesZeroError'

    get_from_mock = mocker.patch('currencies.utils.get_from_url')
    get_from_mock.return_value = MOCK_CURRENCIES
    await update_currencies(database)

    currencies = await get_currencies(database)
    assert currencies['USD']['rate'] == MOCK_CURRENCIES['USD'], currencies['USD']
