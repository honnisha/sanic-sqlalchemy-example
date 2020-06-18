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

users = User.__table__
