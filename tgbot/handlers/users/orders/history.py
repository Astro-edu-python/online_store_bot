from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message, InlineKeyboardMarkup, InputFile, CallbackQuery
)
from sqlalchemy import and_

from tgbot.buttons.inline import make_cancel_inline_kb, make_review_inline_kb
from tgbot.config import Config
from tgbot.constants.commands import UserReplyKeyboardCommands
from tgbot.misc.states import OrdersHistoryState, CreateReviewState
from tgbot.models.orders import Order
from tgbot.models.products import Product
from tgbot.models.reviews import Review
from tgbot.models.user import User
from tgbot.utils.paginator import BotPagePaginator
from tgbot.utils.text import order_notify_text, review_display_text


async def orders_history_command(message: Message):
    config: Config = message.bot['config']
    paginator = BotPagePaginator(
        config.misc.PRODUCTS_PAGINATE_PER_COUNT, Order,
        condition=Order.user == message.from_user.id
    )
    orders: list[Order] = await paginator.paginate()
    if not orders:
        await message.answer(
            'У вас не было заказов'
        )
        return
    order = orders[0]
    product = await Product.get(order.product)
    user = await User.get(message.from_user.id)
    await OrdersHistoryState.show_history.set()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(make_cancel_inline_kb())
    await paginator.add_navigate_keyboard_if_exists(keyboard)
    keyboard.add(make_review_inline_kb(product.id))
    await message.bot.send_photo(
        message.from_user.id,
        InputFile(product.photo),
        order_notify_text(order, product, user.phone_number),
        reply_markup=keyboard
    )


async def show_history_callback(callback: CallbackQuery, state: FSMContext):
    if 'page' in callback.data:
        config: Config = callback.bot['config']
        page_num = int(callback.data.split('_')[-1])
        paginator = BotPagePaginator(
            config.misc.PRODUCTS_PAGINATE_PER_COUNT, Order, page_num,
            Order.user == callback.from_user.id
        )
        orders: list[Order] = await paginator.paginate()
        order = orders[0]
        user = await User.get(callback.from_user.id)
        product: Product = await Product.get(order.product)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(make_cancel_inline_kb())
        await paginator.add_navigate_keyboard_if_exists(keyboard)
        keyboard.add(make_review_inline_kb(product.id))
        await callback.bot.send_photo(
            callback.from_user.id,
            InputFile(product.photo),
            order_notify_text(order, product, user.phone_number),
            reply_markup=keyboard
        )
    elif 'review' in callback.data:
        product_id = int(callback.data.split('_')[-1])
        review: Review | None = await Review.query.where(and_(
            Review.product_id == product_id,
            Review.user_id == callback.from_user.id
        )).gino.first()
        if review:
            await callback.bot.send_message(
                callback.from_user.id,
                f'У вас уже есть отзыв на этот товар\n'
                f'{review_display_text(review)}'
            )
            return
        await CreateReviewState.review.set()
        await state.update_data(choose_product=product_id)
        await callback.bot.send_message(
            callback.from_user.id,
            'Отлично! Отправьте отзыв'
        )
    else:
        await state.finish()
        await callback.bot.send_message(
            callback.from_user.id,
            'Успешно отменил действие'
        )
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )


def orders_history_register_handler(dp: Dispatcher):
    dp.register_message_handler(
        orders_history_command,
        text=UserReplyKeyboardCommands.orders_history.value,
        is_admin=False, is_authenticated=True
    )
    dp.register_callback_query_handler(
        show_history_callback, state=OrdersHistoryState.show_history
    )
