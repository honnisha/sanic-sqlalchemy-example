import sqlalchemy as sa

from main import Base


class Transaction(Base):
    __tablename__ = 'transaction'

    id = sa.Column(sa.types.Integer, primary_key=True, unique=True, autoincrement=True)

    sender_id = sa.Column(sa.types.Integer, sa.ForeignKey('user.id'))
    sender = sa.orm.relationship("User", backref="target_user")
    sender_new_balance = sa.Column(sa.types.Float(precision=5), nullable=False)

    target_id = sa.Column(sa.types.Integer, sa.ForeignKey('user.id'))
    target = sa.orm.relationship("User", backref="sender_user")
    target_new_balance = sa.Column(sa.types.Float(precision=5), nullable=False)

    user = sa.orm.relationship("user")

    currency_id = sa.Column(sa.types.Integer, sa.ForeignKey('currency.id'))
    currency = sa.orm.relationship("Currency", backref="transaction")

transactions = Transaction.__table__
