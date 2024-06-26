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


class OrderState(StatesGroup):
    product_id = State()
    count = State()
    choose_address_type = State()
    address = State()
    comment = State()
    confirm = State()


class OrdersHistoryState(StatesGroup):
    show_history = State()


class CreateReviewState(StatesGroup):
    choose_product = State()
    review = State()
    rate = State()


class ReviewHistoryState(StatesGroup):
    show_history = State()


class ProductReviewsState(StatesGroup):
    reviews = State()


class ModerateReviewsState(StatesGroup):
    show_history = State()
