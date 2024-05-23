from aiogram import Dispatcher

from .qr_code import register_qr_code_handlers
from .user import register_user_handlers


def register_all_user_handlers(dp: Dispatcher):
    register_qr_code_handlers(dp)
    register_user_handlers(dp)
