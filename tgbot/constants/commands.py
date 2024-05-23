from enum import Enum


class UserCommands(Enum):
    start = 'Старт бота'
    share_number = 'Поделиться номером 📞'


class SuperuserReplyKeyboardCommands(Enum):
    add_admin = 'Назначить админа 🤴'
    delete_admin = 'Убрать админа 🤴💀'


class AdminsReplyKeyboardCommands(Enum):
    add_product = 'Добавить продукт 🏺'
    products_list = 'Продукты 🥡'
