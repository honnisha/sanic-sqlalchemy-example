import sqlalchemy as sa

from currencies.models import CurrenciesEnum
from main import Base
from users.models import User


class Transaction(Base):
    __tablename__ = 'transaction'

    id = sa.Column(sa.types.Integer, primary_key=True)

    sender_id = sa.Column(sa.types.Integer, sa.ForeignKey('user.id'))
    sender = sa.orm.relationship("User", backref="target_user")
    sender_new_balance = sa.Column(sa.types.Float(precision=28), nullable=False)
    
    target_id = sa.Column(sa.types.Integer, sa.ForeignKey('user.id'))
    target = sa.orm.relationship("User", backref="sender_user")
    target_new_balance = sa.Column(sa.types.Float(precision=28), nullable=False)

    user = sa.orm.relationship("user")

    currency = sa.Column(sa.types.Enum(CurrenciesEnum), primary_key=True)

transactions = Transaction.__table__
