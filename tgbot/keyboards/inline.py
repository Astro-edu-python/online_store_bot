from aiogram.types import InlineKeyboardMarkup

from tgbot.buttons.inline import make_inline_kb_button_from_obj


def make_inline_kb_from_obj_list(
    obj_list: list[object], attr_name: str, callback_attr_name: str
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for obj in obj_list:
        keyboard.add(make_inline_kb_button_from_obj(
            obj, attr_name, callback_attr_name
        ))
    return keyboard
