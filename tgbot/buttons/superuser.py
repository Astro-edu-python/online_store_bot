from aiogram.types import KeyboardButton

from tgbot.constants.commands import SuperuserReplyKeyboardCommands

SUPERUSER_ADD_ADMIN = KeyboardButton(
    SuperuserReplyKeyboardCommands.add_admin.value
)
SUPERUSER_DELETE_ADMIN = KeyboardButton(
    SuperuserReplyKeyboardCommands.delete_admin.value
)
