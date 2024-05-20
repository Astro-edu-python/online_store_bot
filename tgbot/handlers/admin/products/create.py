from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InputFile, ContentType

from tgbot.buttons.inline import RESUME_WITHOUT_INNER_CATEGORY
from tgbot.config import Config
from tgbot.constants.commands import AdminsReplyKeyboardCommands
from tgbot.keyboards.inline import make_inline_kb_from_obj_list
from tgbot.misc.states import AddProductState
from tgbot.models.products import Category, Product
from tgbot.utils.text import product_info_text


async def add_product_command(message: Message):
    parent_categories = await Category.query.where(
        Category.parent == None
    ).gino.all()
    if not parent_categories:
        await message.answer('У вас нет категорий чтобы привязать продукт')
        return
    keyboard = make_inline_kb_from_obj_list(parent_categories, 'name', 'name')
    await AddProductState.choose_categories.set()
    await message.answer('Отлично! Выберите категорию', reply_markup=keyboard)


async def choose_product_category_callback(
    callback: CallbackQuery, state: FSMContext
):
    try:
        if callback.data == RESUME_WITHOUT_INNER_CATEGORY.callback_data:
            await callback.bot.send_message(
                callback.from_user.id,
                f'Отлично! Введите названия продукта'
            )
            await AddProductState.name.set()
            return
        async with state.proxy() as data:
            categories_list: list[int] = data.get('choose_categories', [])
        category_name = callback.data
        categories_list.append(category_name)
        await state.update_data(choose_categories=categories_list)
        child_categories = await Category.query.where(
            Category.parent == category_name
        ).gino.all()
        if not child_categories:
            await callback.bot.send_message(
                callback.from_user.id,
                f'Отлично! Введите названия продукта'
            )
            await AddProductState.name.set()
            return
        keyboard = make_inline_kb_from_obj_list(
            child_categories, 'name', 'name'
        )
        keyboard.add(RESUME_WITHOUT_INNER_CATEGORY)
        await callback.bot.send_message(
            callback.from_user.id,
            'Выберите дочерний категорий, или продолжайте дальше',
            reply_markup=keyboard
        )
    finally:
        await callback.bot.delete_message(
            callback.from_user.id, callback.message.message_id
        )


async def get_product_name(message: Message, state: FSMContext):
    product_exists = await Product.query.where(
        Product.name == message.text
    ).gino.first()
    if product_exists:
        await message.answer(
            'Продукт уже существует, попробуйте другое название'
        )
        return
    await state.update_data(name=message.text)
    await AddProductState.description.set()
    await message.answer('Введите описание продукта')


async def get_product_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await AddProductState.price.set()
    await message.answer('Введите цену продукта')


async def get_product_price(message: Message, state: FSMContext):
    if not message.text.isdecimal():
        await message.answer('Введите правильную сумму(только целое число)')
        return
    await state.update_data(price=int(message.text))
    await AddProductState.stock.set()
    await message.answer('Введите кол-во продуктов в наличии')


async def get_product_stock(message: Message, state: FSMContext):
    if not message.text.isdecimal():
        await message.answer('Введите правильное число(только целое число)')
        return
    await state.update_data(stock=int(message.text))
    await AddProductState.photo.set()
    await message.answer('Отправьте фото продукта')


async def upload_product_photo_and_save(message: Message, state: FSMContext):
    config: Config = message.bot['config']
    async with state.proxy() as data:
        data: dict = dict(data)
    photo = message.photo[-1]
    file_info = await message.bot.get_file(photo.file_id)
    photo_format = file_info.file_path.split('.')[-1]
    photo_save_path = str(
        config.misc.PRODUCT_PHOTOS_DIR / (data['name'] + '.' + photo_format)
    )
    await message.bot.download_file_by_id(
        photo.file_id, destination=photo_save_path
    )
    categories = data.pop('choose_categories')
    data['category'] = categories[-1]
    data['photo'] = photo_save_path
    product = await Product.create(**data)
    await state.finish()
    await message.answer('Успешно создал товар')
    text = product_info_text(product)
    await message.bot.send_photo(
        message.from_user.id,
        InputFile(product.photo),
        caption='\n'.join(text)
    )


def create_products_handlers(dp: Dispatcher):
    dp.register_message_handler(
        add_product_command,
        text=AdminsReplyKeyboardCommands.add_product.value, is_admin=True
    )
    dp.register_callback_query_handler(
        choose_product_category_callback,
        state=AddProductState.choose_categories,
    )
    dp.register_message_handler(
        get_product_name, state=AddProductState.name
    )
    dp.register_message_handler(
        get_product_description, state=AddProductState.description
    )
    dp.register_message_handler(
        get_product_price, state=AddProductState.price
    )
    dp.register_message_handler(
        get_product_stock, state=AddProductState.stock
    )
    dp.register_message_handler(
        upload_product_photo_and_save, state=AddProductState.photo,
        content_types=[ContentType.PHOTO]
    )
