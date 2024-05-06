from aiogram.types import ReplyKeyboardMarkup

from tgbot.buttons.reply import SUPERUSER_ADD_ADMIN, SUPERUSER_DELETE_ADMIN

SUPERUSER_START_KEYBOARD = ReplyKeyboardMarkup([
    [SUPERUSER_ADD_ADMIN, SUPERUSER_DELETE_ADMIN]
], resize_keyboard=True)
