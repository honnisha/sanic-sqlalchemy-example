from decimal import Decimal, getcontext

from currencies.convertate import convert
from currencies.models import CurrenciesEnum
from currencies.tests.test_utils import MOCK_CURRENCIES
from currencies.utils import update_currencies


async def test_convert(test_cli, database, mocker):
    # Tested on https://cash.rbc.ru/converter.html

    context = getcontext()
    context.prec = 5

    get_from_mock = mocker.patch('currencies.utils.get_from_url')
    get_from_mock.return_value = MOCK_CURRENCIES
    await update_currencies(database)

    result = await convert(Decimal(0.00187), CurrenciesEnum.EUR.value, CurrenciesEnum.USD.value, database)
    target = context.create_decimal_from_float(0.0021191)
    assert result == target, f'EUR>USD {result} != {target}'

    result = await convert(Decimal(25.04134), CurrenciesEnum.USD.value, CurrenciesEnum.RUB.value, database)
    target = context.create_decimal_from_float(1746.6941)
    assert result == target, f'USD>RUB {result} != {target}'

    result = await convert(Decimal(35.25432), CurrenciesEnum.RUB.value, CurrenciesEnum.USD.value, database)
    target = context.create_decimal_from_float(0.50542)
    assert result == target, f'RUB>USD {result} != {target}'

    result = await convert(Decimal(55.26213), CurrenciesEnum.GPB.value, CurrenciesEnum.USD.value, database)
    target = context.create_decimal_from_float(69.7684)
    assert result == target, f'GBP>USD {result} != {target}'
