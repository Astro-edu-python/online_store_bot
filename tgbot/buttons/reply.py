from aiogram.types import KeyboardButton

from tgbot.constants.commands import (
    SuperuserReplyKeyboardCommands, AdminsReplyKeyboardCommands
)

SUPERUSER_ADD_ADMIN = KeyboardButton(
    SuperuserReplyKeyboardCommands.add_admin.value
)
SUPERUSER_DELETE_ADMIN = KeyboardButton(
    SuperuserReplyKeyboardCommands.delete_admin.value
)
ADMIN_ADD_PRODUCT = KeyboardButton(
    AdminsReplyKeyboardCommands.add_product.value
)
PRODUCTS_LIST_COMMAND = KeyboardButton(
    AdminsReplyKeyboardCommands.products_list.value
)
