import enum

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CurrenciesEnum(enum.Enum):
    EUR = "EUR"
    USD = "USD"
    GPB = "GPB"
    RUB = "RUB"
    BTC = "BTC"


class Currency(Base):
    __tablename__ = 'currencies'

    currency = sa.Column(sa.types.Enum(CurrenciesEnum), primary_key=True)
    rate = sa.Column(sa.types.Float)
