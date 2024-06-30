from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.models import Base


class PagePaginator:

    def __init__(
        self, page_per_count: int,  model: Base, page_num: int = 1,
        condition: Any | None = None, id_field: str = 'id'
    ):
        self.__page_per_count: int = page_per_count
        self.__model: Base = model
        self.__page_num = page_num
        self.__condition: Any | None = condition
        self.id_field = id_field

    @property
    def page_num(self):
        return self.__page_num

    @property
    def condition(self):
        return self.__condition

    @property
    def page_per_count(self) -> int:
        return self.__page_per_count

    async def pages_count(self) -> int:
        if self.condition is not None:
            count = await Base.select([Base.func.count(
                getattr(self.__model, self.id_field)
            )]).where(self.condition).gino.scalar()
        else:
            count = await Base.select([
                getattr(self.__model, self.id_field)
            ]).gino.scalar()
        pages_count = count // self.__page_per_count or 1
        return pages_count

    async def has_next_page(self) -> bool:
        return 1 <= self.__page_num + 1 <= await self.pages_count()

    async def has_prev_page(self) -> bool:
        return 1 <= self.__page_num - 1 <= await self.pages_count()

    async def paginate(self) -> list[Base.Model]:
        if self.__page_num == 1:
            offset = 0
        else:
            offset = self.__page_per_count * self.__page_num - 1
        async with Base.transaction():
            cursor = await (
                self.__condition_parse()
                .order_by(self.id_field).gino.iterate()
            )
            if offset:
                await cursor.forward(offset)
            result = await cursor.many(self.__page_per_count)
        return result

    def __condition_parse(self):
        if self.condition is not None:
            return (
                self.__model
                .query.where(self.condition)
            )
        return (
            self.__model.query
        )


class BotPagePaginator(PagePaginator):

    def __init__(
        self, page_per_count: int, model: Base, page_num: int = 1,
        condition: Any | None = None, id_field: str = 'id'
    ):
        super().__init__(page_per_count, model, page_num, condition, id_field)

    def has_next_page_inline_btn(
        self, callback_data: str
    ) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            '➡️', callback_data=f'{callback_data}{str(self.page_num + 1)}'
        )

    def has_prev_page_inline_btn(
        self, callback_data: str
    ) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            '⬅️', callback_data=f'{callback_data}{str(self.page_num - 1)}'
        )

    async def add_navigate_keyboard_if_exists(
        self, keyboard: InlineKeyboardMarkup,
        extra_callback_data: str = 'page_'
    ) -> InlineKeyboardMarkup:
        has_next = await self.has_next_page()
        has_prev = await self.has_prev_page()
        if has_next:
            if keyboard.inline_keyboard:
                keyboard.inline_keyboard[-1].append(
                    self.has_next_page_inline_btn(extra_callback_data)
                )
            else:
                keyboard.add(
                    self.has_next_page_inline_btn(extra_callback_data)
                )
        if has_prev:
            if keyboard.inline_keyboard:
                keyboard.inline_keyboard[0].insert(
                    0, self.has_prev_page_inline_btn(extra_callback_data)
                )
            else:
                keyboard.add(
                    self.has_prev_page_inline_btn(extra_callback_data)
                )
        return keyboard
