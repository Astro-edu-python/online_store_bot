from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ContentTypes

from tgbot.constants.commands import UserCommands
from tgbot.keyboards.reply import USER_REGISTER_KEYBOARD
from tgbot.misc.states import RegisterUserState
from tgbot.models.user import User


async def user_start(message: Message):
    await message.reply(
        'Приветствую пользователь!',
        reply_markup=ReplyKeyboardRemove()
    )
    user: User | None = await User.get(message.from_user.id)
    if not user:
        await RegisterUserState.send_number.set()
        await message.answer(
            'Вы не зарегистрированы! '
            'Чтобы зарегистрироваться отправьте свой номер',
            reply_markup=USER_REGISTER_KEYBOARD
        )
        return
    await message.answer('Выберите команду')


async def register_user(message: Message, state: FSMContext):
    phone_number = int(message.contact.phone_number)
    await User.create(id=message.from_user.id, phone_number=phone_number)
    await state.finish()
    await message.answer('Вы успешно зарегистрировались!')
    await message.answer('Выберите команду')


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(
        user_start, commands=[UserCommands.start.name], state='*'
    )
    dp.register_message_handler(
        register_user, state=RegisterUserState.send_number,
        content_types=ContentTypes.CONTACT
    )
