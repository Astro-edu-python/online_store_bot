import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message, InlineKeyboardMarkup, CallbackQuery, InputFile
)

from tgbot.buttons.inline import (
    make_deliver_by_location_inline_kb,
    make_deliver_by_custom_location_inline_kb, make_confirm_order_inline_kb,
    make_cancel_inline_kb
)
from tgbot.config import Config
from tgbot.keyboards.reply import (
    USER_GET_LOCATION_KEYBOARD, USER_START_KEYBOARD
)
from tgbot.misc.states import OrderState
from tgbot.models.orders import Order
from tgbot.models.products import Product
from tgbot.models.user import User
from tgbot.utils.bot import notify_admins_message
from tgbot.utils.text import order_confirm_info, order_notify_text


async def order_product_count(message: Message, state: FSMContext):
    if not message.text.isdecimal():
        await message.answer('Вы ввели не цифру!')
        return
    await state.update_data(count=int(message.text))
    await OrderState.choose_address_type.set()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(make_deliver_by_location_inline_kb())
    keyboard.add(make_deliver_by_custom_location_inline_kb())
    await message.answer(
        'Отлично! Выберите способ доставки', reply_markup=keyboard
    )


async def choose_delivery_type_callback(
    callback: CallbackQuery, state: FSMContext
):
    await state.update_data(choose_address_type=callback.data)
    await OrderState.address.set()
    await callback.bot.send_message(
        callback.from_user.id, 'Отправьте адрес доставки',
        reply_markup=(
            USER_GET_LOCATION_KEYBOARD
            if 'manual' not in callback.data else None
        )
    )
    await callback.bot.delete_message(
        callback.from_user.id, callback.message.message_id
    )


async def get_delivery_address(message: Message, state: FSMContext):
    if message.location:
        await state.update_data(
            address=f"широта: {message.location.latitude}\n"
                    f"долгота: {message.location.longitude}"
        )
    else:
        await state.update_data(address=message.text)
    await OrderState.comment.set()
    await message.answer(
        'Ваш комментарий(или примечания) к заказу',
        reply_markup=USER_START_KEYBOARD
    )


async def get_order_comment_and_confirm(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await OrderState.confirm.set()
    await message.answer('Подтвердите заказ')
    async with state.proxy() as data:
        product_id = data['product_id']
        count = data['count']
        address = data['address']
        comment = data['comment']
    product = await Product.query.where(
        Product.id == product_id
    ).gino.first()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(make_confirm_order_inline_kb())
    keyboard.add(make_cancel_inline_kb())
    await message.answer_photo(
        InputFile(product.photo),
        caption=order_confirm_info(
            product, count, address, comment, product.price * count
        ),
        reply_markup=keyboard
    )


async def confirm_order_callback(callback: CallbackQuery, state: FSMContext):
    await callback.bot.delete_message(
        callback.from_user.id, callback.message.message_id
    )
    if 'confirm' in callback.data:
        async with state.proxy() as data:
            count = int(data['count'])
            address = data['address']
            product_id = data['product_id']
            comment = data['comment']
        product: Product = await Product.query.where(
            Product.id == product_id
        ).gino.first()
        order_sum = product.price * count
        user = await User.query.where(
            User.id == callback.from_user.id
        ).gino.first()
        if not product.stock:
            await state.finish()
            await callback.bot.send_message(
                callback.from_user.id, 'Товара нет в наличии'
            )
            return
        if product.stock - count < 0:
            await state.finish()
            await callback.bot.send_message(
                callback.from_user.id,
                'Вы не можете заказать товар больше чем в наличии'
            )
            return
        if user.balance < order_sum:
            await state.finish()
            await callback.bot.send_message(
                callback.from_user.id, 'У вас нет средств для покупки'
            )
            return
        await user.update(balance=user.balance-order_sum).apply()
        order: Order = await Order.create(
            product=product_id, user=user.id, count=count, address=address,
            comment=comment, order_sum=order_sum,
            created_date=datetime.datetime.now()
        )
        await product.update(stock=product.stock - count).apply()
        await callback.bot.send_message(
            callback.from_user.id,
            f'Ваш заказ создан! Его номер {order.id}\n'
            f'Также вы можете посмотреть информацию о заказе в своих заказах'
        )
        config: Config = callback.bot['config']
        await notify_admins_message(
            config.tg_bot.admin_ids, callback.bot,
            f'Заявка! {order_notify_text(order, product, user.phone_number)}'
        )
    else:
        await state.finish()
        await callback.bot.send_message(
            callback.from_user.id, 'Отменил все действия'
        )


def register_create_orders_handlers(dp: Dispatcher):
    dp.register_message_handler(
        order_product_count, state=OrderState.count, is_admin=False,
        is_authenticated=True
    )
    dp.register_callback_query_handler(
        choose_delivery_type_callback, state=OrderState.choose_address_type
    )
    dp.register_message_handler(
        get_delivery_address, state=OrderState.address,
    )
    dp.register_message_handler(
        get_order_comment_and_confirm, state=OrderState.comment
    )
    dp.register_callback_query_handler(
        confirm_order_callback, state=OrderState.confirm,
    )
