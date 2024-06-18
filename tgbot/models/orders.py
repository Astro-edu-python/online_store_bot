from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

from tgbot.models import Base
from tgbot.models.products import Product
from tgbot.models.user import User


class Order(Base.Model):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    product = Column(
        Integer,
        ForeignKey(f'{Product.__tablename__}.id', ondelete='CASCADE'),
        nullable=False
    )
    user = Column(
        Integer,
        ForeignKey(f'{User.__tablename__}.id', ondelete='CASCADE'),
        nullable=False
    )
    count = Column(Integer, nullable=False)
    address = Column(String(255), nullable=False)
    comment = Column(String, nullable=False)
    order_sum = Column(Integer, nullable=False)
    created_date = Column(DateTime, nullable=False)

    def __str__(self):
        return self.address

    def __repr__(self):
        return f'{self.id}: {self.address}'
