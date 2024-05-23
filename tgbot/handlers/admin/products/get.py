from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message, InlineKeyboardMarkup, InputFile, CallbackQuery
)

from tgbot.buttons.inline import make_delete_inline_kb, make_change_inline_kb
from tgbot.config import Config
from tgbot.constants.commands import AdminsReplyKeyboardCommands
from tgbot.keyboards.inline import make_inline_kb_from_obj_attrs_list
from tgbot.misc.states import ManageProductState, ChangeProductState
from tgbot.models.products import Product
from tgbot.serializers.product import ProductFields
from tgbot.utils.paginator import BotPagePaginator
from tgbot.utils.text import product_info_text


async def get_products_command(message: Message):
    config: Config = message.bot['config']
    paginator = BotPagePaginator(
        config.misc.PRODUCTS_PAGINATE_PER_COUNT, Product
    )
    product: list[Product] = await paginator.paginate()
    if not product:
        await message.answer('У вас нет продуктов')
        return
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        make_delete_inline_kb(f'delete_{product[0].id}'),
        make_change_inline_kb(f'change_{product[0].id}')
    )
    await paginator.add_navigate_keyboard_if_exists(keyboard)
    await ManageProductState.choose_product_callback.set()
    await message.bot.send_photo(
        message.from_user.id,
        InputFile(product[0].photo),
        product_info_text(product[0]),
        reply_markup=keyboard
    )


async def choose_product_callback(callback: CallbackQuery, state: FSMContext):
    if 'page' in callback.data:
        config: Config = callback.bot['config']
        page_num = int(callback.data.split('_')[-1])
        paginator = BotPagePaginator(
            config.misc.PRODUCTS_PAGINATE_PER_COUNT, Product, page_num
        )
        product: list[Product] = await paginator.paginate()
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            make_delete_inline_kb(f'delete_{product[0].id}'),
            make_change_inline_kb(f'change_{product[0].id}')
        )
        await paginator.add_navigate_keyboard_if_exists(keyboard)
        await callback.bot.send_photo(
            callback.from_user.id,
            InputFile(product[0].photo),
            product_info_text(product[0]),
            reply_markup=keyboard
        )
    elif 'delete' in callback.data:
        product_id = int(callback.data.split('_')[-1])
        await Product.delete.where(Product.id == product_id).gino.status()
        await callback.bot.send_message(
            callback.from_user.id,
            'Успешно удалил товар'
        )
        await state.finish()
    else:
        await state.finish()
        product_id = int(callback.data.split('_')[-1])
        product: Product | None = await Product.get(product_id)
        if not product:
            await callback.bot.send_message(
                callback.from_user.id,
                'Товар не найден'
            )
            return
        await ChangeProductState.choose_field.set()
        keyboard = make_inline_kb_from_obj_attrs_list(
            ProductFields, f'{product_id}', attr_name_as_prefix=True
        )
        await callback.bot.send_message(
            callback.from_user.id,
            'Отлично! Выбирайте что обновить',
            reply_markup=keyboard
        )
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )


def register_product_get_handlers(dp: Dispatcher):
    dp.register_message_handler(
        get_products_command, is_admin=True,
        text=AdminsReplyKeyboardCommands.products_list.value
    )
    dp.register_callback_query_handler(
        choose_product_callback,
        state=ManageProductState.choose_product_callback
    )
