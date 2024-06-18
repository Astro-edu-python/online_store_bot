from aiogram.types import KeyboardButton

from tgbot.constants.commands import (
    SuperuserReplyKeyboardCommands, AdminsReplyKeyboardCommands,
    UserReplyKeyboardCommands
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
SEND_CONTACT_BUTTON = KeyboardButton(
    UserReplyKeyboardCommands.share_number.value, request_contact=True
)
USER_REFERRER_LINK = KeyboardButton(
    UserReplyKeyboardCommands.referrer_link.value
)
USER_QR_CODE = KeyboardButton(
    UserReplyKeyboardCommands.referrer_link_qr_code.value
)
ADD_BALANCE_BUTTON = KeyboardButton(
    UserReplyKeyboardCommands.add_balance.value
)
MY_BALANCE_BUTTON = KeyboardButton(
    UserReplyKeyboardCommands.my_balance.value
)
PRODUCTS_LIST_USER_COMMAND = KeyboardButton(
    UserReplyKeyboardCommands.products.value
)
MY_BASKET_BUTTON = KeyboardButton(
    UserReplyKeyboardCommands.my_basket.value
)
SEND_LOCATION_BUTTON = KeyboardButton(
    UserReplyKeyboardCommands.send_location.value, request_location=True
)
ORDERS_HISTORY_BUTTON = KeyboardButton(
    UserReplyKeyboardCommands.orders_history.value
)
