from typing import Optional

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery

from tgbot.config import Config
from tgbot.models.user import User


class IsAuthenticated(BoundFilter):
    key = 'is_authenticated'

    def __init__(self, is_authenticated: Optional[bool] = None):
        self.is_authenticated = is_authenticated

    async def check(self, obj: Message | CallbackQuery):
        config: Config = obj.bot['config']
        if self.is_authenticated is None:
            return False
        user = await User.query.where(
            User.id == obj.from_user.id,
        ).gino.first()
        return bool(user) == self.is_authenticated
