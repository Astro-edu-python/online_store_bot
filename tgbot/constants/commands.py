from enum import Enum


class UserCommands(Enum):
    start = 'Старт бота'


class UserReplyKeyboardCommands(Enum):
    share_number = 'Поделиться номером 📞'
    referrer_link = 'Моя реферальная ссылка 🔗'
    referrer_link_qr_code = 'Мой QR код 🖼️'


class SuperuserReplyKeyboardCommands(Enum):
    add_admin = 'Назначить админа 🤴'
    delete_admin = 'Убрать админа 🤴💀'


class AdminsReplyKeyboardCommands(Enum):
    add_product = 'Добавить продукт 🏺'
    products_list = 'Продукты 🥡'
