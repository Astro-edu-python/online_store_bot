from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message, LabeledPrice, PreCheckoutQuery, ContentType, ChatType
)

from tgbot.config import Config
from tgbot.constants.commands import UserReplyKeyboardCommands
from tgbot.misc.states import AddPaymentState
from tgbot.models.user import User
from tgbot.services.payment.service import UzPaymentService


async def get_balance(message: Message):
    config: Config = message.bot['config']
    user = await User.get(message.from_user.id)
    await message.answer(
        f'Ваш баланс: {user.balance} {config.tg_bot.payment_currency.name}'
    )


async def add_balance_command(message: Message):
    await AddPaymentState.get_sum.set()
    config: Config = message.bot['config']
    await message.answer(
        f'Введите сумму пополнения(в {config.tg_bot.payment_currency.code})\n'
        f'Минимальная сумма: {config.tg_bot.payment_currency.min_price} '
        f'{config.tg_bot.payment_currency.name}\n'
        f'Максимальная сумма: {config.tg_bot.payment_currency.max_price} '
        f'{config.tg_bot.payment_currency.name}'
    )


async def add_balance_invoice(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        config: Config = message.bot['config']
        if any([
            amount > config.tg_bot.payment_currency.max_price,
            amount < config.tg_bot.payment_currency.min_price,
        ]):
            raise ValueError
    except ValueError:
        await message.answer('Вы ввели неправильную сумму, введите ещё раз')
        return
    service = UzPaymentService(amount, message.from_user.id)
    msg = await message.bot.send_invoice(
        message.from_user.id, 'Пополнение баланса',
        'Человек хочет пополнить свой баланс', service.payload,
        config.tg_bot.payment_token, config.tg_bot.payment_currency.code,
        [LabeledPrice('Пополнение баланса', service.parse_amount())]
    )
    await AddPaymentState.pre_checkout.set()
    await state.update_data(pre_checkout=msg.message_id)


async def pre_checkout_balance_query(
    query: PreCheckoutQuery, state: FSMContext
):
    async with state.proxy() as data:
        checkout_msg_id = data['pre_checkout']
    user_id, amount = UzPaymentService.parse_payload(query.invoice_payload)
    await query.bot.delete_message(query.from_user.id, checkout_msg_id)
    if user_id != query.from_user.id:
        await query.bot.send_message(
            query.from_user.id,
            'Попробуйте заново'
        )
        await state.finish()
        await query.bot.answer_pre_checkout_query(query.id, False)
        return
    await query.bot.answer_pre_checkout_query(query.id, True)
    await AddPaymentState.success.set()


async def success_balance_payment(message: Message, state: FSMContext):
    config: Config = message.bot['config']
    service = UzPaymentService(
        message.successful_payment.total_amount, message.from_user.id
    )
    amount = service.resolve_amount()
    user = await User.get(message.from_user.id)
    await user.update(balance=user.balance + amount).apply()
    await message.answer(
        f'Вам начислено {amount} {config.tg_bot.payment_currency.name}'
        f' на баланс!\nВаш текущий баланс: {user.balance} '
        f'{config.tg_bot.payment_currency.name}'
    )
    await state.finish()


def register_balance_handlers(dp: Dispatcher):
    dp.register_message_handler(
        get_balance, text=UserReplyKeyboardCommands.my_balance.value,
        is_admin=False, is_authenticated=True
    )
    dp.register_message_handler(
        add_balance_command, text=UserReplyKeyboardCommands.add_balance.value,
        is_admin=False, chat_type=ChatType.PRIVATE, is_authenticated=True
    )
    dp.register_message_handler(
        add_balance_invoice, state=AddPaymentState.get_sum
    )
    dp.register_pre_checkout_query_handler(
        pre_checkout_balance_query, state=AddPaymentState.pre_checkout,
    )
    dp.register_message_handler(
        success_balance_payment, state=AddPaymentState.success,
        content_types=ContentType.SUCCESSFUL_PAYMENT
    )
