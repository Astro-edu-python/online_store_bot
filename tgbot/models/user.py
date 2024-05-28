from sqlalchemy import Column, BigInteger, Boolean, ForeignKey

from tgbot.models import Base


class User(Base.Model):

    __tablename__ = 'tg_users'

    id = Column(BigInteger(), primary_key=True)
    phone_number = Column(BigInteger())
    is_admin = Column(
        Boolean(), default=False, nullable=False, server_default='f'
    )
    referrer_user_id = Column(
        BigInteger, ForeignKey(f'{__tablename__}.id', ondelete='CASCADE'),
        nullable=True
    )
    balance = Column(
        BigInteger(), default=0, nullable=False, server_default='0'
    )

    def __str__(self) -> str:
        return f'{self.id}'

    def __repr__(self):
        return f'Tg user: {self.id}'
