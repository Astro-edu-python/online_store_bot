from aiogram import Dispatcher

from .moderate import register_reviews_moderate_handlers


def register_all_reviews_handler(dp: Dispatcher):
    register_reviews_moderate_handlers(dp)
