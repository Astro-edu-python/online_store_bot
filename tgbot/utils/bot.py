from aiogram import Bot
from aiogram.types import BotCommand

from tgbot.constants.commands import UserCommands


def get_bot_commands() -> list[BotCommand]:
    bot_commands: list[BotCommand] = []
    for command, description in UserCommands.__members__.items():
        bot_commands.append(
            BotCommand(command, description.value)
        )
    return bot_commands


async def install_bot_commands(bot: Bot):
    await bot.set_my_commands(get_bot_commands())


async def notify_admins_message(
    admins_ids: list[int], bot: Bot, message: str,
    parse_mode: str = "HTML"
):
    for admin in admins_ids:
        await bot.send_message(admin, message, parse_mode=parse_mode)
