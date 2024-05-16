from aiogram.types import InlineKeyboardButton


RESUME_WITHOUT_INNER_CATEGORY = InlineKeyboardButton(
    'Продолжить без вложенных категорий ➡️', callback_data='resume'
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
