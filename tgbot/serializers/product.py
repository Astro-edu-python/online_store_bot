from dataclasses import dataclass
from enum import Enum


@dataclass
class DisplayField:
    name: str
    obj_attr_name: str


class ProductFields(Enum):
    name: DisplayField = DisplayField('Название', 'name')
    description: DisplayField = DisplayField('Описание', 'description')
    price: DisplayField = DisplayField('Цена', 'price')
    stock: DisplayField = DisplayField('Кол-во в наличии', 'stock')
