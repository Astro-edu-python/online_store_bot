from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.config import Config
from tgbot.constants.commands import SuperuserReplyKeyboardCommands
from tgbot.misc.states import AddAdminState, DeleteAdminState
from tgbot.models.user import User
from tgbot.utils.handlers.users import make_users_info_callback_keyboard
from tgbot.utils.paginator import BotPagePaginator
from tgbot.utils.text import user_mention_text_html


async def add_admin_command(message: Message):
    config: Config = message.bot['config']
    paginator = BotPagePaginator(
        config.misc.PAGINATE_PER_COUNT, User,
        condition=User.is_admin == False
    )
    users: list[User] = await paginator.paginate()
    if not users:
        await message.reply('Кандидатов на админа нет')
        return
    keyboard, users_info_text = await make_users_info_callback_keyboard(
        users, message.bot
    )
    await paginator.add_navigate_keyboard_if_exists(keyboard)
    await AddAdminState.choose_admin_callback.set()
    await message.answer(
        f'Отлично! Выбирайте пользователя\n' +
        '\n'.join(users_info_text),
        reply_markup=keyboard
    )


async def add_admin_callback(callback: CallbackQuery, state: FSMContext):
    if 'page' in callback.data:
        config: Config = callback.bot['config']
        page_num = int(callback.data.split('_')[-1])
        paginator = BotPagePaginator(
            config.misc.PAGINATE_PER_COUNT, User, page_num,
            condition=User.is_admin == False
        )
        users: list[User] = await paginator.paginate()
        keyboard, users_info_text = await make_users_info_callback_keyboard(
            users, callback.bot
        )
        await paginator.add_navigate_keyboard_if_exists(keyboard)
        await callback.bot.edit_message_text(
            'Выбирайте пользователя\n' + '\n'.join(users_info_text),
            callback.from_user.id, callback.message.message_id,
            reply_markup=keyboard
        )
    else:
        user_id = int(callback.data)
        await callback.bot.delete_message(
            callback.from_user.id,
            callback.message.message_id
        )
        await state.finish()
        await User.update.where(
            User.id == user_id
        ).values(is_admin=True).gino.status()
        user_info = await callback.bot.get_chat(user_id)
        await callback.bot.send_message(
            callback.from_user.id,
            f'Успешно назначил админом пользователя '
            f'{user_mention_text_html(user_info.id, user_info.full_name)}'
        )


async def delete_admin_command(message: Message):
    users: list[User] = await User.query.where(
        User.is_admin == True
    ).gino.all()
    if not users:
        await message.reply('Админов нет')
        return
    keyboard, users_info_text = await make_users_info_callback_keyboard(
        users, message.bot
    )
    await DeleteAdminState.choose_admin_callback.set()
    await message.answer(
        f'Отлично! Выбирайте админа\n' +
        '\n'.join(users_info_text),
        reply_markup=keyboard
    )


async def delete_admin_callback(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data)
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    await state.finish()
    await User.update.where(
        User.id == user_id
    ).values(is_admin=False).gino.status()
    user_info = await callback.bot.get_chat(user_id)
    await callback.bot.send_message(
        callback.from_user.id,
        f'Успешно убрал пользователя '
        f'{user_mention_text_html(user_info.id, user_info.full_name)} из '
        f'админов'
    )


def register_superuser_admin_crud_handlers(dp: Dispatcher):
    dp.register_message_handler(
        add_admin_command, text=SuperuserReplyKeyboardCommands.add_admin.value,
        is_superuser=True
    )
    dp.register_callback_query_handler(
        add_admin_callback, is_superuser=True,
        state=AddAdminState.choose_admin_callback
    )
    dp.register_message_handler(
        delete_admin_command, is_superuser=True,
        text=SuperuserReplyKeyboardCommands.delete_admin.value
    )
    dp.register_callback_query_handler(
        delete_admin_callback, is_superuser=True,
        state=DeleteAdminState.choose_admin_callback
    )
