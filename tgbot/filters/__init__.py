from aiogram import Dispatcher

from .admin import AdminFilter
from .authenticate import IsAuthenticated
from .superuser import IsSuperuser


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(IsSuperuser)
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsAuthenticated)
