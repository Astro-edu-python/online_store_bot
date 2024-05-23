from typing import Optional

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery

from tgbot.config import Config


class IsSuperuser(BoundFilter):
    key = 'is_superuser'

    def __init__(self, is_superuser: Optional[bool] = None):
        self.is_superuser = is_superuser

    async def check(self, obj: Message | CallbackQuery):
        if self.is_superuser is None:
            return False
        config: Config = obj.bot.get('config')
        return (
            obj.from_user.id in config.tg_bot.admin_ids
        ) == self.is_superuser
