from aiogram.dispatcher.filters.state import StatesGroup, State


class AddAdminState(StatesGroup):
    choose_admin_callback = State()


class DeleteAdminState(StatesGroup):
    choose_admin_callback = State()


class AddProductState(StatesGroup):
    choose_categories = State()
    name = State()
    description = State()
    price = State()
    stock = State()
    photo = State()
