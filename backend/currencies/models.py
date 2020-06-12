import enum

import sqlalchemy as sa

from main import Base


class CurrenciesEnum(enum.Enum):
    EUR = "EUR"
    USD = "USD"
    GPB = "GPB"
    RUB = "RUB"
    BTC = "BTC"


class Currency(Base):
    __tablename__ = 'currency'

    currency = sa.Column(sa.types.Enum(CurrenciesEnum), primary_key=True)
    rate = sa.Column(sa.types.Float)

currencies = Currency.__table__
