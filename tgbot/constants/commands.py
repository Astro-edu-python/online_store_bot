from enum import Enum


class UserCommands(Enum):
    start = 'Старт бота'


class SuperuserReplyKeyboardCommands(Enum):
    add_admin = 'Назначить админа 🤴'
    delete_admin = 'Убрать админа 🤴💀'


class AdminsReplyKeyboardCommands(Enum):
    add_product = 'Добавить продукт 🏺'
    products_list = 'Продукты 🥡'
