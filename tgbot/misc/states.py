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


class ManageProductState(StatesGroup):
    choose_product_callback = State()


class ChangeProductState(StatesGroup):
    choose_field = State()
    value = State()


class RegisterUserState(StatesGroup):
    send_number = State()


class AddPaymentState(StatesGroup):
    get_sum = State()
    pre_checkout = State()
    success = State()


class ShowProductsState(StatesGroup):
    choose_category = State()
    choose_product = State()


class BasketShowState(StatesGroup):
    choose_product = State()
