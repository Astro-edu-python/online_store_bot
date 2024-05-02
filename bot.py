import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters import register_all_filters
from tgbot.handlers import register_all_handlers
from tgbot.models import Base
from tgbot.utils.bot import install_bot_commands, notify_admins_message

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=(
            u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - '
            u'%(name)s - %(message)s'
        )
    )
    logger.info('Starting bot')
    config = load_config('.env')

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config
    register_all_filters(dp)
    register_all_handlers(dp)
    await install_bot_commands(bot)
    await Base.set_bind(config.main_db.async_url)

    try:
        await dp.reset_webhook(True)
        await dp.skip_updates()
        logger.info('UPDATES WERE SKIPPED')
        await dp.start_polling()
    except Exception as error:
        message = f'UNEXPECTED ERROR {error}. Error args: {error.args}'
        logger.warning(message)
        await notify_admins_message(
            config.tg_bot.admin_ids, bot, message
        )
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()
        await Base.pop_bind().close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
