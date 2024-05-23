from aiogram import Dispatcher

from .create import create_products_handlers
from .get import register_product_get_handlers
from .update import register_update_product_handlers


def register_all_products_handler(dp: Dispatcher):
    create_products_handlers(dp)
    register_product_get_handlers(dp)
    register_update_product_handlers(dp)
