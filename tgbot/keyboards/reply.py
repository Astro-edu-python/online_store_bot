from aiogram.types import ReplyKeyboardMarkup

import tgbot.buttons.reply as rkb


ADMIN_START_KEYBOARD = ReplyKeyboardMarkup([
    [rkb.ADMIN_ADD_PRODUCT, rkb.PRODUCTS_LIST_COMMAND]
], resize_keyboard=True)
SUPERUSER_START_KEYBOARD = ReplyKeyboardMarkup([
    [rkb.SUPERUSER_ADD_ADMIN, rkb.SUPERUSER_DELETE_ADMIN],
] + ADMIN_START_KEYBOARD.keyboard, resize_keyboard=True)
USER_REGISTER_KEYBOARD = ReplyKeyboardMarkup(
    [[rkb.SEND_CONTACT_BUTTON]], resize_keyboard=True
)
