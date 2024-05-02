from aiogram import Dispatcher

from tgbot.handlers.admin import register_admin_handlers
from tgbot.handlers.echo import register_echo
from tgbot.handlers.superusers import register_all_superusers_handlers
from tgbot.handlers.users import register_all_user_handlers


def register_all_handlers(dp: Dispatcher):
    register_all_superusers_handlers(dp)
    register_admin_handlers(dp)
    register_all_user_handlers(dp)
    register_echo(dp)
