from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.models.user import User
from tgbot.utils.text import user_mention_text_html


async def make_users_info_callback_keyboard(
    users: list[User], bot: Bot
) -> tuple[InlineKeyboardMarkup, list[str]]:
    users_info_text: list[str] = []
    buttons: list[InlineKeyboardButton] = []
    for idx, user in enumerate(users, start=1):
        chat_info = await bot.get_chat(user.id)
        users_info_text.append(f'{idx}: ' + user_mention_text_html(
            chat_info.id, chat_info.full_name
        ))
        buttons.append(InlineKeyboardButton(
            idx, callback_data=f'{user.id}'
        ))
    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard, users_info_text
