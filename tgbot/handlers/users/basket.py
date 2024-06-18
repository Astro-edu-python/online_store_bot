from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton, InputFile,
    CallbackQuery
)
from redis.asyncio import Redis

from tgbot.buttons.inline import make_buy_inline_kb, make_delete_inline_kb
from tgbot.constants.commands import UserReplyKeyboardCommands
from tgbot.misc.states import BasketShowState, OrderState
from tgbot.models.products import Product
from tgbot.models.user import User
from tgbot.services.basket.types import UserProfile
from tgbot.utils.text import product_info_text


async def basket_products_command(message: Message):
    redis: Redis = message.bot['cache_db']
    user = await UserProfile.load(redis, message.from_user.id)
    if not user or not user.basket.products_ids:
        await message.answer('Ваша корзина пуста')
        return
    product: Product | None = None
    while user.basket.products_ids:
        product_id: int = user.basket.products_ids[0]
        product = await Product.query.where(
            Product.id == product_id
        ).gino.first()
        if product:
            break
        user.basket.products_ids.pop(0)
    else:
        await message.answer('Продуктов в корзине нет')
        return
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            make_buy_inline_kb(product.id),
            make_delete_inline_kb(f'delete_{product.id}')
        ]]
    )
    if len(user.basket.products_ids) > 1:
        keyboard.inline_keyboard[0].append(InlineKeyboardButton(
            '➡️', callback_data=f'page_2'
        ))
    await BasketShowState.choose_product.set()
    await message.bot.send_photo(
        message.from_user.id,
        InputFile(product.photo),
        product_info_text(product),
        reply_markup=keyboard
    )


async def choose_product_callback(callback: CallbackQuery, state: FSMContext):
    product_id: int = int(callback.data.split('_')[-1])
    if 'delete' in callback.data:
        redis: Redis = callback.bot['cache_db']
        user = await UserProfile.load(redis, callback.from_user.id)
        user.basket.remove_product(product_id)
        await user.insert_to_db(redis)
        await state.finish()
        await callback.bot.delete_message(
            callback.from_user.id, callback.message.message_id
        )
        await callback.bot.send_message(
            callback.from_user.id, 'Успешно удалил продукт'
        )
    else:
        product = await Product.query.where(
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
            return
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
        callback.from_user.id, callback.message.message_id
    )


def register_basket_products_handlers(dp: Dispatcher):
    dp.register_message_handler(
        basket_products_command,
        text=UserReplyKeyboardCommands.my_basket.value, is_admin=False,
        is_authenticated=True
    )
    dp.register_callback_query_handler(
        choose_product_callback, state=BasketShowState.choose_product
    )
