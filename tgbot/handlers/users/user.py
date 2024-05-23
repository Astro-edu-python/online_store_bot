from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ContentTypes

from tgbot.constants.commands import UserCommands, UserReplyKeyboardCommands
from tgbot.keyboards.reply import USER_REGISTER_KEYBOARD, USER_START_KEYBOARD
from tgbot.misc.states import RegisterUserState
from tgbot.models.user import User
from tgbot.utils.text import get_referrer_link_html


async def user_start(message: Message, state: FSMContext):
    await message.reply(
        'Приветствую пользователь!',
        reply_markup=ReplyKeyboardRemove()
    )
    user: User | None = await User.get(message.from_user.id)
    if not user:
        await RegisterUserState.send_number.set()
        if 'referrer' in message.text:
            referrer_id = int(message.text.split('referrer')[-1])
            referrer: User | None = await User.get(referrer_id)
            if not referrer or referrer_id == message.from_user.id:
                await message.answer(
                    'У вас неправильная пригласительная ссылка'
                )
                return
            await state.update_data(send_number=referrer_id)
        await message.answer(
            'Вы не зарегистрированы! '
            'Чтобы зарегистрироваться отправьте свой номер',
            reply_markup=USER_REGISTER_KEYBOARD
        )
        return
    await message.answer('Выберите команду', reply_markup=USER_START_KEYBOARD)


async def register_user(message: Message, state: FSMContext):
    await state.finish()
    phone_number = int(message.contact.phone_number)
    user: User | None = await User.query.where(
        User.phone_number == phone_number
    ).gino.first()
    if user:
        await message.answer(
            'Пользователь с таким номером телефона существует!'
        )
        return
    async with state.proxy() as data:
        referrer_id = data.get('send_number')
    if referrer_id:
        await User.create(
            id=message.from_user.id, phone_number=phone_number,
            referrer_user_id=referrer_id
        )
    else:
        await User.create(
            id=message.from_user.id, phone_number=phone_number
        )
    await message.answer('Вы успешно зарегистрировались!')
    await message.answer('Выберите команду', reply_markup=USER_START_KEYBOARD)


async def show_user_referrer_link(message: Message):
    bot_info = await message.bot.get_me()
    await message.answer(
        f'Ваша реферальная ссылка: '
        f'{get_referrer_link_html(bot_info.username, message.from_user.id)}'
    )


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(
        user_start, commands=[UserCommands.start.name], state='*'
    )
    dp.register_message_handler(
        register_user, state=RegisterUserState.send_number,
        content_types=ContentTypes.CONTACT
    )
    dp.register_message_handler(
        show_user_referrer_link,
        text=UserReplyKeyboardCommands.referrer_link.value
    )
