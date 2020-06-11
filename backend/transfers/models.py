import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'

    id = sa.Column(sa.types.Integer, primary_key=True)

    sender_id = Column(Integer, ForeignKey('user.id'))
    sender_new_balance = sa.Column(sa.types.Float(precision=28))
    
    target_id = Column(Integer, ForeignKey('user.id'))
    target_new_balance = sa.Column(sa.types.Float(precision=28))

    user = relationship("User")

    currency = sa.Column(Enum(CurrenciesEnum), primary_key=True)
