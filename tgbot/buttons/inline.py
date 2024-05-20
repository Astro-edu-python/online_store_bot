from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

RESUME_WITHOUT_INNER_CATEGORY = InlineKeyboardButton(
    'Продолжить без вложенных категорий ➡️', callback_data='resume'
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
    callback_data: str | int | float | bool | None = None
) -> InlineKeyboardButton:
    return make_inline_kb_button('Изменить 📃', callback_data)


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
