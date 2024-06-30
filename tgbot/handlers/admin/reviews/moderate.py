from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message, InlineKeyboardMarkup, InputFile, CallbackQuery
)
from sqlalchemy import and_

from tgbot.buttons.inline import (
    make_cancel_inline_kb, make_confirm_order_inline_kb, ban_reviews_inline_kb
)
from tgbot.config import Config
from tgbot.constants.commands import AdminsReplyKeyboardCommands
from tgbot.misc.states import ModerateReviewsState
from tgbot.models.products import Product
from tgbot.models.reviews import Review, ReviewsStatusChoices
from tgbot.utils.paginator import BotPagePaginator
from tgbot.utils.text import product_info_text, review_display_text


async def moderate_reviews_command(message: Message):
    config: Config = message.bot['config']
    paginator = BotPagePaginator(
        config.misc.PRODUCTS_PAGINATE_PER_COUNT, Review,
        condition=Review.status == ReviewsStatusChoices.MODERATE,
        id_field='user_id'
    )
    reviews: list[Review] = await paginator.paginate()
    if not reviews:
        await message.answer('Нет подходящих отзывов')
        return
    review = reviews[0]
    product = await Product.get(review.product_id)
    await ModerateReviewsState.show_history.set()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        make_confirm_order_inline_kb(f'{review.user_id}__{review.product_id}'),
        ban_reviews_inline_kb(f'{review.user_id}__{review.product_id}'),
    )
    await paginator.add_navigate_keyboard_if_exists(keyboard)
    keyboard.add(make_cancel_inline_kb())
    await message.bot.send_photo(
        message.from_user.id,
        InputFile(product.photo),
        caption=(
                'Товар\n' + product_info_text(product) + '\n\nОтзыв\n' +
                review_display_text(review)
        ),
        reply_markup=keyboard
    )


async def moderate_reviews_callback(
    callback: CallbackQuery, state: FSMContext
):
    if 'page' in callback.data:
        config: Config = callback.bot['config']
        page = int(callback.data.split('_')[-1])
        paginator = BotPagePaginator(
            config.misc.PRODUCTS_PAGINATE_PER_COUNT, Review, page,
            condition=Review.status == ReviewsStatusChoices.MODERATE,
            id_field='user_id'
        )
        reviews: list[Review] = await paginator.paginate()
        if not reviews:
            await callback.answer('Нет подходящих отзывов')
            await state.finish()
            return
        review = reviews[0]
        product = await Product.get(review.product_id)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            make_confirm_order_inline_kb(
                f'{review.user_id}__{review.product_id}'),
            ban_reviews_inline_kb(f'{review.user_id}__{review.product_id}'),
        )
        await paginator.add_navigate_keyboard_if_exists(keyboard)
        keyboard.add(make_cancel_inline_kb())
        await callback.bot.send_photo(
            callback.from_user.id,
            InputFile(product.photo),
            caption=(
                    'Товар\n' + product_info_text(product) + '\n\nОтзыв\n' +
                    review_display_text(review)
            ),
            reply_markup=keyboard
        )
    elif 'confirm' in callback.data:
        user_id, product_id = [
            int(i.split('_')[-1]) for i in callback.data.split('__')
        ]
        await Review.update.where(and_(
            Review.user_id == user_id,
            Review.product_id == product_id
        )).values({'status': ReviewsStatusChoices.PUBLISHED}).gino.status()
        await state.finish()
        await callback.bot.send_message(
            callback.from_user.id,
            'Подтвердил комментарий'
        )
    elif 'reject' in callback.data:
        user_id, product_id = [
            int(i.split('_')[-1]) for i in callback.data.split('__')
        ]
        await Review.update.where(and_(
            Review.user_id == user_id,
            Review.product_id == product_id
        )).values({'status': ReviewsStatusChoices.REJECTED}).gino.status()
        await state.finish()
        await callback.bot.send_message(
            callback.from_user.id,
            'Отклонил комментарий'
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


def register_reviews_moderate_handlers(dp: Dispatcher):
    dp.register_message_handler(
        moderate_reviews_command,
        text=AdminsReplyKeyboardCommands.moderate_reviews.value,
        is_admin=True
    )
    dp.register_callback_query_handler(
        moderate_reviews_callback, state=ModerateReviewsState.show_history
    )
