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

    id = sa.Column(sa.types.Integer, primary_key=True, unique=True, autoincrement=True)

    currency = sa.Column(sa.types.Enum(CurrenciesEnum), unique=True)
    rate = sa.Column(sa.types.Float)

currencies = Currency.__table__
