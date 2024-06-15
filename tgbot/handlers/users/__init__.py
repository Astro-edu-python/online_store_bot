from aiogram import Dispatcher

from .balance import register_balance_handlers
from .products import register_products_handlers
from .basket import register_basket_products_handlers
from .qr_code import register_qr_code_handlers
from .user import register_user_handlers


def register_all_user_handlers(dp: Dispatcher):
    register_qr_code_handlers(dp)
    register_user_handlers(dp)
    register_balance_handlers(dp)
    register_products_handlers(dp)
    register_basket_products_handlers(dp)
