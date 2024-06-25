from aiogram import Dispatcher

from .create import register_create_reviews_handlers
from .list import register_reviews_list_handlers


def register_reviews_handlers(dp: Dispatcher):
    register_create_reviews_handlers(dp)
    register_reviews_list_handlers(dp)
