from aiogram import Dispatcher

from .superuser import IsSuperuser


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(IsSuperuser)
