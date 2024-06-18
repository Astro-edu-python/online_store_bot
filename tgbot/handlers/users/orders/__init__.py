from aiogram import Dispatcher

from .create import register_create_orders_handlers
from .history import orders_history_register_handler


def register_orders_handlers(dp: Dispatcher):
    register_create_orders_handlers(dp)
    orders_history_register_handler(dp)
