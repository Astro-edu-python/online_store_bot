from aiogram.types import ReplyKeyboardMarkup

import tgbot.buttons.reply as rkb


ADMIN_START_KEYBOARD = ReplyKeyboardMarkup([
    [rkb.ADMIN_ADD_PRODUCT, rkb.PRODUCTS_LIST_COMMAND],
    [rkb.ADMIN_MODERATE_REVIEWS_COMMAND]
], resize_keyboard=True)
SUPERUSER_START_KEYBOARD = ReplyKeyboardMarkup([
    [rkb.SUPERUSER_ADD_ADMIN, rkb.SUPERUSER_DELETE_ADMIN],
] + ADMIN_START_KEYBOARD.keyboard, resize_keyboard=True)
USER_REGISTER_KEYBOARD = ReplyKeyboardMarkup(
    [[rkb.SEND_CONTACT_BUTTON]], resize_keyboard=True
)
USER_START_KEYBOARD = ReplyKeyboardMarkup([
    [rkb.USER_REFERRER_LINK, rkb.USER_QR_CODE],
    [rkb.ADD_BALANCE_BUTTON, rkb.MY_BALANCE_BUTTON],
    [rkb.PRODUCTS_LIST_USER_COMMAND, rkb.MY_BASKET_BUTTON],
    [rkb.ORDERS_HISTORY_BUTTON, rkb.MY_REVIEWS_BUTTON]
], resize_keyboard=True)
USER_GET_LOCATION_KEYBOARD = ReplyKeyboardMarkup(
    [[rkb.SEND_LOCATION_BUTTON]], resize_keyboard=True
)
