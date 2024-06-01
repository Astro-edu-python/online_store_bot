from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message, CallbackQuery, InputFile, InlineKeyboardMarkup
)

from tgbot.buttons.inline import SHOW_CATEGORY_PRODUCTS
from tgbot.config import Config
from tgbot.constants.commands import UserReplyKeyboardCommands
from tgbot.keyboards.inline import make_inline_kb_from_obj_list
from tgbot.misc.states import ShowProductsState
from tgbot.models.products import Category, Product
from tgbot.utils.paginator import BotPagePaginator
from tgbot.utils.text import product_info_text


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
            await paginator.add_navigate_keyboard_if_exists(keyboard)
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


async def choose_products_callback(callback: CallbackQuery):
    if 'page' in callback.data:
        config: Config = callback.bot['config']
        page_num = int(callback.data.split('_')[-1])
        paginator = BotPagePaginator(
            config.misc.PRODUCTS_PAGINATE_PER_COUNT, Product, page_num
        )
        product: list[Product] = await paginator.paginate()
        keyboard = InlineKeyboardMarkup()
        await paginator.add_navigate_keyboard_if_exists(keyboard)
        await callback.bot.send_photo(
            callback.from_user.id,
            InputFile(product[0].photo),
            product_info_text(product[0]),
            reply_markup=keyboard
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
