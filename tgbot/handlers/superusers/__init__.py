from aiogram import Dispatcher

from .admins import register_superuser_admin_crud_handlers
from .start import register_superuser_start_handlers


def register_all_superusers_handlers(dp: Dispatcher):
    register_superuser_start_handlers(dp)
    register_superuser_admin_crud_handlers(dp)
