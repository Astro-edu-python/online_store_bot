from aiogram.types import InlineKeyboardButton

RESUME_WITHOUT_INNER_CATEGORY = InlineKeyboardButton(
    'Продолжить без вложенных категорий ➡️', callback_data='resume'
)
SHOW_CATEGORY_PRODUCTS = InlineKeyboardButton(
    'Показать товары этой категории', callback_data='show_category_products'
)


def make_inline_kb_button(
    name: str, callback_data: str | int | float | bool | None = None,
) -> InlineKeyboardButton:
    if callback_data is not None:
        return InlineKeyboardButton(
            name, callback_data=str(callback_data)
        )
    else:
        return InlineKeyboardButton(name)


def make_delete_inline_kb(
    callback_data: str | int | float | bool | None = None
) -> InlineKeyboardButton:
    return make_inline_kb_button('Удалить 🗑️', callback_data)


def make_change_inline_kb(
    callback_data: str | int | float | bool = ''
) -> InlineKeyboardButton:
    return make_inline_kb_button('Изменить 📃', callback_data)


def make_cart_inline_kb(
    callback_data: str | int | float | bool = ''
) -> InlineKeyboardButton:
    return make_inline_kb_button(
        'В корзину 🧺', f'basket_{callback_data}'
    )


def make_buy_inline_kb(
    callback_data: str | int | float | bool = ''
) -> InlineKeyboardButton:
    return make_inline_kb_button(
        'Купить 💲', f'buy_{callback_data}'
    )


def make_deliver_by_location_inline_kb(
    callback_data: str | int | float | bool = ''
):
    return make_inline_kb_button(
        'Отправить свою локацию 📍', f'location_{callback_data}'
    )


def make_deliver_by_custom_location_inline_kb(
    callback_data: str | int | float | bool = ''
):
    return make_inline_kb_button(
        'Отправить другой адрес 🗺️', f'manual_location_{callback_data}'
    )


def make_confirm_order_inline_kb(
    callback_data: str | int | float | bool = ''
):
    return make_inline_kb_button(
        'Подтвердить ✅', f'confirm_{callback_data}'
    )


def make_cancel_inline_kb(
    callback_data: str | int | float | bool = ''
):
    return make_inline_kb_button(
        'Отменить ❌', f'cancel_{callback_data}'
    )


def make_review_inline_kb(
    callback_data: str | int | float | bool = ''
):
    return make_inline_kb_button(
        'Оставить отзыв ✒️', f'review_{callback_data}'
    )


def make_inline_kb_button_from_obj(
    obj: object, attr_name: str, callback_attr_name: str | None = None
) -> InlineKeyboardButton:
    if callback_attr_name is None:
        return InlineKeyboardButton(
            getattr(obj, attr_name)
        )
    return InlineKeyboardButton(
        getattr(obj, attr_name),
        callback_data=str(getattr(obj, callback_attr_name))
    )
