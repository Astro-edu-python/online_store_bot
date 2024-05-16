from aiogram.types import ReplyKeyboardMarkup

import tgbot.buttons.reply as rkb


ADMIN_START_KEYBOARD = ReplyKeyboardMarkup([
    [rkb.ADMIN_ADD_PRODUCT]
], resize_keyboard=True)
SUPERUSER_START_KEYBOARD = ReplyKeyboardMarkup([
    [rkb.SUPERUSER_ADD_ADMIN, rkb.SUPERUSER_DELETE_ADMIN],
] + ADMIN_START_KEYBOARD.keyboard, resize_keyboard=True)
