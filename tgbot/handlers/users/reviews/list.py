from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message, InlineKeyboardMarkup, InputFile, CallbackQuery
)

from tgbot.buttons.inline import make_cancel_inline_kb
from tgbot.config import Config
from tgbot.constants.commands import UserReplyKeyboardCommands
from tgbot.misc.states import ReviewHistoryState
from tgbot.models.products import Product
from tgbot.models.reviews import Review
from tgbot.utils.paginator import BotPagePaginator
from tgbot.utils.text import product_info_text, review_display_text


async def my_reviews_command(message: Message):
    config: Config = message.bot['config']
    paginator = BotPagePaginator(
        config.misc.PRODUCTS_PAGINATE_PER_COUNT, Review,
        condition=Review.user_id == message.from_user.id, id_field='user_id'
    )
    reviews: list[Review] = await paginator.paginate()
    if not reviews:
        await message.answer('У вас нет отзывов')
        return
    review = reviews[0]
    product = await Product.get(review.product_id)
    await ReviewHistoryState.show_history.set()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(make_cancel_inline_kb())
    await paginator.add_navigate_keyboard_if_exists(keyboard)
    await message.bot.send_photo(
        message.from_user.id,
        InputFile(product.photo),
        caption=(
            'Товар\n' + product_info_text(product) + '\n\nОтзыв\n' +
            review_display_text(review)
        ),
        reply_markup=keyboard
    )


async def reviews_callback(callback: CallbackQuery, state: FSMContext):
    if 'page' in callback.data:
        config: Config = callback.bot['config']
        page_num = int(callback.data.split('_')[-1])
        paginator = BotPagePaginator(
            config.misc.PRODUCTS_PAGINATE_PER_COUNT, Review, page_num,
            Review.user_id == callback.from_user.id, 'user_id'
        )
        reviews: list[Review] = await paginator.paginate()
        review = reviews[0]
        product: Product = await Product.get(review.product_id)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(make_cancel_inline_kb())
        await paginator.add_navigate_keyboard_if_exists(keyboard)
        await callback.bot.send_photo(
            callback.from_user.id,
            InputFile(product.photo),
            caption=(
                'Товар\n' + product_info_text(product) + '\n\nОтзыв\n' +
                review_display_text(review)
            ),
            reply_markup=keyboard
        )
    else:
        await state.finish()
        await callback.bot.send_message(
            callback.from_user.id,
            'Отменил действие'
        )
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )


def register_reviews_list_handlers(dp: Dispatcher):
    dp.register_message_handler(
        my_reviews_command,
        text=UserReplyKeyboardCommands.reviews_history.value,
        is_admin=False, is_authenticated=True
    )
    dp.register_callback_query_handler(
        reviews_callback, state=ReviewHistoryState.show_history
    )
