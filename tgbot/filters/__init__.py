from aiogram import Dispatcher

from .admin import AdminFilter
from .superuser import IsSuperuser


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(IsSuperuser)
    dp.filters_factory.bind(AdminFilter)
