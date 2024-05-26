import os.path

from aiogram import Dispatcher
from aiogram.types import Message, InputFile

from tgbot.config import Config
from tgbot.constants.commands import UserReplyKeyboardCommands
from tgbot.utils.qr_code import make_user_qr_code, get_qr_code_path


async def get_user_qr_code(message: Message):
    config: Config = message.bot['config']
    qr_path = get_qr_code_path(config.misc.QR_CODES_DIR, message.from_user.id)
    if not os.path.exists(qr_path):
        qr_path = make_user_qr_code(
            config, await message.bot.get_me(), message.from_user.id
        )
    await message.bot.send_photo(
        message.from_user.id,
        InputFile(qr_path),
        caption='Ваш QR код'
    )


def register_qr_code_handlers(dp: Dispatcher):
    dp.register_message_handler(
        get_user_qr_code,
        text=UserReplyKeyboardCommands.referrer_link_qr_code.value,
        is_admin=False
    )
