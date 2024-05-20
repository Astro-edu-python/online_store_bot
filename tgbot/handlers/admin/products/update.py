from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.misc.states import ChangeProductState
from tgbot.models.products import Product


async def update_product_field_callback(
    callback: CallbackQuery, state: FSMContext
):
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    attrs = callback.data.split('__')
    if len(attrs) == 2:
        await state.update_data(choose_field=attrs)
        await ChangeProductState.value.set()
        await callback.bot.send_message(
            callback.from_user.id,
            'Отправьте новое значение'
        )
    else:
        await callback.bot.send_message(
            callback.from_user.id,
            'Внутренняя ошибка, не знаю что именно поменять'
        )
        return


async def update_product(message: Message, state: FSMContext):
    async with state.proxy() as data:
        attrs = data['choose_field']
    await state.finish()
    product_id, attr_name = int(attrs[0]), attrs[-1]
    product = await Product.get(product_id)
    if not product:
        await message.answer('Продукт не найден')
        return
    try:
        attr_type: type = Product.__table__.columns[attr_name].type.python_type
        await Product.update.where(Product.id == product_id).values(
            {attr_name: attr_type(message.text)}
        ).gino.status()
    except Exception as e:
        await message.answer(f'Неизвестная ошибка при обновлении товара: {e}')
        return
    await message.answer('Успешно обновил продукт')


def register_update_product_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        update_product_field_callback, state=ChangeProductState.choose_field
    )
    dp.register_message_handler(
        update_product, state=ChangeProductState.value
    )
