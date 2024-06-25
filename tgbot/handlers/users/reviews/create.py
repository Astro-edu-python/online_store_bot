from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.states import CreateReviewState
from tgbot.models.reviews import Review
from tgbot.utils.exceptions import BotException
from tgbot.utils.text import review_display_text


async def review_text_handler(message: Message, state: FSMContext):
    try:
        Review.validate(message.text, raise_exception=True)
    except BotException as error:
        await message.answer(error.message)
        return
    await state.update_data(review=message.text)
    await message.answer('Отправьте оценку на товар(от 1 до 5)')
    await CreateReviewState.rate.set()


async def review_rate_handler(message: Message, state: FSMContext):
    try:
        if not message.text.isdecimal():
            await message.answer('Вы отправили не число')
            return
        rate = int(message.text)
        Review.validate(rate=rate, raise_exception=True)
    except BotException as error:
        await message.answer(error.message)
        return
    async with state.proxy() as data:
        product_id = data['choose_product']
        review = data['review']
    review = await Review.create(
        review=review, user_id=message.from_user.id, product_id=product_id,
        rate=rate
    )
    await message.answer(
        'Ваш отзыв добавлен успешно\n' + review_display_text(review)
    )


def register_create_reviews_handlers(dp: Dispatcher):
    dp.register_message_handler(
        review_text_handler, state=CreateReviewState.review,
        is_admin=False, is_authenticated=True
    )
    dp.register_message_handler(
        review_rate_handler, state=CreateReviewState.rate
    )
