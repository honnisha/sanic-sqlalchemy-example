from decimal import Decimal

import sqlalchemy as sa

from main import Base


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.types.Integer, primary_key=True, unique=True, autoincrement=True)

    _balance = sa.Column(sa.types.Float(precision=5), nullable=False)
    email = sa.Column(sa.types.String, unique=True, nullable=False)
    password_hash = sa.Column(sa.types.String, nullable=False)

    currency_id = sa.Column(sa.types.Integer, sa.ForeignKey('currency.id'), nullable=False)
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
