from decimal import Decimal

import sqlalchemy as sa

from currencies.models import CurrenciesEnum
from main import Base
from users.utils import generate_password_hash, verify_password


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.types.Integer, primary_key=True, unique=True, autoincrement=True)

    _balance = sa.Column(sa.types.Float(precision=28))
    email = sa.Column(sa.types.String, unique=True)
    password_hash = sa.Column(sa.types.String)

    currency_id = sa.Column(sa.types.Integer, sa.ForeignKey('currency.id'))
    currency = sa.orm.relationship("Currency", backref="transaction")

    @property
    def balance(self):
        return Decimal(self._balance)

    @property
    def name(self):
        return f'#{id} {self.email}'

    @balance.setter
    def balance(self, new_balance):
        self._balance = float(new_balance)

users = User.__table__
