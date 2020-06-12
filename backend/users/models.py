from decimal import Decimal

import sqlalchemy as sa

from currencies.models import CurrenciesEnum
from main import Base
from users.utils import generate_password_hash, verify_password


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.types.Integer, primary_key=True, unique=True, autoincrement=True)
    _balance = sa.Column(sa.types.Float(precision=28))
    currency = sa.Column(sa.types.Enum(CurrenciesEnum), primary_key=True)
    email = sa.Column(sa.types.String, unique=True)
    password_hash = sa.Column(sa.types.String)

    @property
    def balance(self):
        return Decimal(self._balance)

    @balance.setter
    def balance(self, new_balance):
        self._balance = float(new_balance)

# self.password_hash = generate_password_hash(password)
