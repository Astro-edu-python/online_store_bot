from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.constants.commands import UserCommands
from tgbot.keyboards.reply import SUPERUSER_START_KEYBOARD


async def start_superuser(message: Message):
    await message.answer(
        'Приветствую, суперпользователь!',
        reply_markup=SUPERUSER_START_KEYBOARD
    )


def register_superuser_start_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_superuser, state='*', is_superuser=True,
        commands=[UserCommands.start.name], commands_prefix='!/'
    )
