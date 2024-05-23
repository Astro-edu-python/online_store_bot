from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy import and_

from tgbot.config import Config
from tgbot.models.user import User


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: bool | None = None):
        self.is_admin = is_admin

    async def check(self, message: Message | CallbackQuery) -> bool:
        config: Config = message.bot['config']
        if self.is_admin is None:
            return False
        user = await User.query.where(and_(
            User.is_admin == self.is_admin,
            User.id == message.from_user.id,
        )).gino.first()
        return bool(user) or message.from_user.id in config.tg_bot.admin_ids
