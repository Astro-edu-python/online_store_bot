from sqlalchemy import Column, Integer, String, ForeignKey

from tgbot.models import Base


class Category(Base.Model):
    __tablename__ = 'categories'

    name = Column(String, primary_key=True, nullable=False)
    parent = Column(
        String, ForeignKey(f'{__tablename__}.name', ondelete='CASCADE'),
        nullable=True
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Product(Base.Model):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    category = Column(
        String,
        ForeignKey(f'{Category.__tablename__}.name', ondelete='CASCADE'),
        nullable=False
    )
    name = Column(String(75), unique=True, nullable=False)
    description = Column(String(255))
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    photo = Column(String, nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.id}: {self.name}'
