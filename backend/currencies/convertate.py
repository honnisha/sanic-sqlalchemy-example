from decimal import Decimal, getcontext

from redis import ConnectionPool

from currencies.models import CurrenciesEnum, base
from currencies.utils import get_currencies
from databases import Database


async def convert(
        value: Decimal, source_currency: str, target_currency: str,
        database: Database, redis_pool: ConnectionPool=None
) -> Decimal:
    getcontext().prec = 5

    if source_currency == target_currency:
        return value

    currencies_data = await get_currencies(database, redis_pool)
    currencies = {curr: data['rate'] for curr, data in currencies_data.items()}

    value_in_base = value / Decimal(currencies[source_currency])
    return value_in_base * Decimal(currencies[target_currency])
