from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint

from tgbot.models import Base
from tgbot.models.products import Product
from tgbot.models.user import User


class Review(Base.Model):
    __tablename__ = 'reviews'
    __table_args__ = UniqueConstraint(
        'user_id', 'product_id', name='ut_reviews_user_id_product_id'
    ),

    id = Column(Integer, primary_key=True)
    review = Column(String(150))
    user_id = Column(Integer, ForeignKey(f'{User.__tablename__}.id'))
    product_id = Column(Integer, ForeignKey(f'{Product.__tablename__}.id'))
    rate = Column(Integer)

    def __str__(self):
        return f'{self.user_id}: {self.rate}'

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.id}'
