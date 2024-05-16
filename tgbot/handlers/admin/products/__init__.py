from aiogram import Dispatcher

from .create import create_products_handlers


def register_all_products_handler(dp: Dispatcher):
    create_products_handlers(dp)
