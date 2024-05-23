from aiogram import Dispatcher

from .products import register_all_products_handler
from .start import register_admin_start_handlers


def register_admin_handlers(dp: Dispatcher):
    register_admin_start_handlers(dp)
    register_all_products_handler(dp)
