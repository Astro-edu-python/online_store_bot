from enum import EnumType

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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


def make_inline_kb_from_obj_attrs_list(
    attrs_model: EnumType, callback_attr_prefix: str = '',
    send_callback: bool = True, attr_name_as_prefix: bool = False
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for attr_name, attr_value in attrs_model.__members__.items():
        if not callback_attr_prefix and not send_callback:
            keyboard.add(InlineKeyboardButton(attr_value.value.name))
        else:
            if attr_name_as_prefix:
                keyboard.add(InlineKeyboardButton(
                    attr_value.value.name,
                    callback_data=f'{callback_attr_prefix}__'
                                  f'{attr_value.value.obj_attr_name}'
                ))
            else:
                keyboard.add(InlineKeyboardButton(
                    attr_value.value.name,
                    callback_data=callback_attr_prefix
                ))
    return keyboard
