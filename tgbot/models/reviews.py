from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint

from tgbot.models import Base
from tgbot.models.products import Product
from tgbot.models.user import User
from tgbot.utils.exceptions import BotException


class Review(Base.Model):
    __tablename__ = 'reviews'
    __table_args__ = UniqueConstraint(
        'user_id', 'product_id', name='ut_reviews_user_id_product_id'
    ),

    review = Column(String(150))
    user_id = Column(
        Integer, ForeignKey(f'{User.__tablename__}.id', ondelete='CASCADE')
    )
    product_id = Column(Integer, ForeignKey(
        f'{Product.__tablename__}.id', ondelete='CASCADE'
    ))
    rate = Column(Integer)

    @classmethod
    def validate(
        cls, review: str | None = None, rate: int | None = None,
        raise_exception: bool = False
    ) -> bool:
        valid_fields = []
        if review is not None:
            column_: Column = getattr(cls, 'review')
            len_review_valid = column_.expression.type.length > len(review)
            if not len_review_valid and raise_exception:
                raise BotException(
                    f'Отзыв слишком длинный(допускается до '
                    f'{column_.expression.type.length} символов)'
                )
            valid_fields.append(len_review_valid)
        if rate is not None:
            rate_valid = 0 < rate <= 5
            if not rate_valid and raise_exception:
                raise BotException('Оценка должна быть от 1 до 5')
            valid_fields.append(rate_valid)
        return all(valid_fields)

    def __str__(self):
        return f'{self.user_id}: {self.rate}'

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.id}'
