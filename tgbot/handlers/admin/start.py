from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.constants.commands import UserCommands
from tgbot.keyboards.reply import ADMIN_START_KEYBOARD


async def start_admin(message: Message, state: FSMContext) -> None:
    await state.finish()
    await message.answer(
        'Приветствую, админ!',
        reply_markup=ADMIN_START_KEYBOARD
    )


def register_admin_start_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_admin, state='*', is_admin=True,
        commands=[UserCommands.start.name], commands_prefix='!/'
    )
