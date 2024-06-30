from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message, CallbackQuery, InputFile, InlineKeyboardMarkup
)
from redis.asyncio import Redis
from sqlalchemy import and_

from tgbot.buttons.inline import (
    SHOW_CATEGORY_PRODUCTS, make_cart_inline_kb, make_buy_inline_kb,
    make_show_reviews_inline_kb, make_cancel_inline_kb
)
from tgbot.config import Config
from tgbot.constants.commands import UserReplyKeyboardCommands
from tgbot.keyboards.inline import make_inline_kb_from_obj_list
from tgbot.misc.states import (
    ShowProductsState, OrderState, ProductReviewsState
)
from tgbot.models.products import Category, Product
from tgbot.models.reviews import Review, ReviewsStatusChoices
from tgbot.models.user import User
from tgbot.services.basket.types import UserProfile, UserBasket
from tgbot.utils.paginator import BotPagePaginator
from tgbot.utils.text import product_info_text, review_display_text


async def get_products_command(message: Message):
    categories = await Category.query.where(
        Category.parent == None
    ).gino.all()
    if not categories:
        await message.answer('Товаров нет')
        return
    await ShowProductsState.choose_category.set()
    keyboard = make_inline_kb_from_obj_list(categories, 'name', 'name')
    await message.answer('Отлично! Выберите категорию', reply_markup=keyboard)


async def choose_product_category_callback(
    callback: CallbackQuery, state: FSMContext
):
    try:
        if callback.data == 'show_category_products':
            async with state.proxy() as data:
                category_name = data['choose_category']
            config: Config = callback.bot['config']
            paginator = BotPagePaginator(
                config.misc.PRODUCTS_PAGINATE_PER_COUNT, Product,
                condition=Product.category == category_name
            )
            products: list[Product] = await paginator.paginate()
            if not products:
                await callback.bot.send_message(
                    callback.from_user.id,
                    'Товаров по данному категорию нет'
                )
                await state.finish()
                return
            await ShowProductsState.choose_product.set()
            keyboard = InlineKeyboardMarkup()
            keyboard.add(make_cart_inline_kb(products[0].id))
            keyboard.inline_keyboard[0].append(make_buy_inline_kb(products[0].id))
            await paginator.add_navigate_keyboard_if_exists(keyboard)
            keyboard.add(make_show_reviews_inline_kb(products[0].id))
            await callback.bot.send_photo(
                callback.from_user.id,
                InputFile(products[0].photo),
                product_info_text(products[0]),
                reply_markup=keyboard
            )
            return
        await state.update_data(choose_category=callback.data)
        child_categories = await Category.query.where(
            Category.parent == callback.data
        ).gino.all()
        keyboard = make_inline_kb_from_obj_list(
            child_categories, 'name', 'name'
        )
        keyboard.add(SHOW_CATEGORY_PRODUCTS)
        await callback.bot.send_message(
            callback.from_user.id,
            'Выберите следующую категорию либо '
            'нажмите показать товары этой категории',
            reply_markup=keyboard
        )
    finally:
        await callback.bot.delete_message(
            callback.from_user.id, callback.message.message_id
        )


async def choose_products_callback(callback: CallbackQuery, state: FSMContext):
    if 'page' in callback.data:
        config: Config = callback.bot['config']
        page_num = int(callback.data.split('_')[-1])
        async with state.proxy() as data:
            category_name = data['choose_category']
        paginator = BotPagePaginator(
            config.misc.PRODUCTS_PAGINATE_PER_COUNT, Product, page_num,
            condition=Product.category == category_name
        )
        product: list[Product] = await paginator.paginate()
        keyboard = InlineKeyboardMarkup()
        keyboard.add(make_cart_inline_kb(product[0].id))
        keyboard.inline_keyboard[0].append(make_buy_inline_kb(product[0].id))
        await paginator.add_navigate_keyboard_if_exists(keyboard)
        keyboard.add(make_show_reviews_inline_kb(product[0].id))
        await callback.bot.send_photo(
            callback.from_user.id,
            InputFile(product[0].photo),
            product_info_text(product[0]),
            reply_markup=keyboard
        )
    elif 'basket_' in callback.data:
        product_id = int(callback.data.split('basket_')[-1])
        redis: Redis = callback.bot['cache_db']
        user = await UserProfile.load(redis, callback.from_user.id)
        if not user:
            user = UserProfile(callback.from_user.id, UserBasket([product_id]))
        else:
            user.basket.add_product(product_id)
        await user.insert_to_db(redis)
        await callback.bot.send_message(
            callback.from_user.id,
            'Успешно добавил в корзину'
        )
        await state.finish()
    elif 'reviews' in callback.data:
        config: Config = callback.bot['config']
        product_id = int(callback.data.split('reviews_')[-1])
        paginator = BotPagePaginator(
            config.misc.PRODUCTS_PAGINATE_PER_COUNT, Review,
            condition=and_(
                Review.product_id == product_id,
                Review.status == ReviewsStatusChoices.PUBLISHED
            ), id_field='product_id'
        )
        reviews: list[Review] = await paginator.paginate()
        if not reviews:
            await callback.answer('У этого товара нет отзывов')
            return
        review = reviews[0]
        product: Product = await Product.get(review.product_id)
        await ProductReviewsState.reviews.set()
        keyboard = InlineKeyboardMarkup()
        keyboard.add(make_cancel_inline_kb())
        await paginator.add_navigate_keyboard_if_exists(
            keyboard, f'page_{product_id}_'
        )
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
        product_id: int = int(callback.data.split('_')[-1])
        product: Product = await Product.query.where(
            Product.id == product_id
        ).gino.first()
        if not product.stock:
            await callback.bot.send_message(
                callback.from_user.id,
                'Товара нет в наличии'
            )
            await state.finish()
            return
        user = await User.query.where(
            User.id == callback.from_user.id
        ).gino.first()
        if user.balance < product.price:
            await callback.bot.send_message(
                callback.from_user.id,
                'Недостаточно средств на балансе'
            )
            await state.finish()
        else:
            available_count = int(user.balance // product.price)
            await OrderState.count.set()
            await state.update_data(product_id=product_id)
            await callback.bot.send_message(
                callback.from_user.id,
                f'Отправьте кол-во товаров для покупки\n'
                f'Исходя из вашего баланса вы можете купить {available_count} '
                f'шт.\nМаксимальное кол-во доступных товаров: {product.stock} шт.'
            )
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )


async def reviews_list_callback(callback: CallbackQuery, state: FSMContext):
    if 'page' in callback.data:
        config: Config = callback.bot['config']
        page_num = int(callback.data.split('_')[-1])
        product_id = int(callback.data.split('_')[-2])
        paginator = BotPagePaginator(
            config.misc.PRODUCTS_PAGINATE_PER_COUNT, Review, page_num,
            condition=and_(
                Review.status == ReviewsStatusChoices.PUBLISHED,
                Review.product_id == product_id
            ), id_field='product_id'
        )
        reviews: list[Review] = await paginator.paginate()
        review = reviews[0]
        product: Product = await Product.get(review.product_id)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(make_cancel_inline_kb())
        await paginator.add_navigate_keyboard_if_exists(
            keyboard, f'page_{product_id}_'
        )
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


def register_products_handlers(dp: Dispatcher):
    dp.register_message_handler(
        get_products_command, text=UserReplyKeyboardCommands.products.value,
        is_admin=False, is_authenticated=True
    )
    dp.register_callback_query_handler(
        choose_product_category_callback,
        state=ShowProductsState.choose_category
    )
    dp.register_callback_query_handler(
        choose_products_callback, state=ShowProductsState.choose_product
    )
    dp.register_callback_query_handler(
        reviews_list_callback, state=ProductReviewsState.reviews
    )
