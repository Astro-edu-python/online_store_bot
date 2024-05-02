from sqlalchemy import Column, Integer, BigInteger, Boolean

from tgbot.models import Base


class User(Base.Model):

    __tablename__ = 'tg_users'

    id = Column(BigInteger(), primary_key=True)
    phone_number = Column(BigInteger())
    is_admin = Column(
        Boolean(), default=False, nullable=False, server_default='f'
    )

    def __str__(self) -> str:
        return f'{self.id}'

    def __repr__(self):
        return f'Tg user: {self.id}'
