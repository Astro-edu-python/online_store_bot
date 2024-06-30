from tgbot.models.orders import Order
from tgbot.models.products import Product
from tgbot.models.reviews import Review


def user_mention_text_html(chat_id: int, display_text: str) -> str:
    return f'<a href="tg://user?id={chat_id}">{display_text}</a>'


def get_referrer_link(bot_username: str, user_id: int) -> str:
    return f'https://t.me/{bot_username}?start=referrer{user_id}'


def product_info_text(product: Product) -> str:
    text = (
        f'Продукт: #{product.id} {product.name}',
        f'Категория: {product.category}',
        f'Описание: {product.description}',
        f'Цена: {product.price}',
        f'Кол-во в наличии: {product.stock}',
    )
    return '\n'.join(text)


def order_confirm_info(
    product: Product, count: int, address: str, comment: str, order_sum: int
) -> str:
    product_info = product_info_text(product)
    product_info += (
        f'\nКол-во товаров в заказе: {count}\n'
        f'Адрес доставки: {address}\nКомментарий к заказу: {comment}\n'
        f'Сумма заказа: {order_sum}'
    )
    return product_info


def order_notify_text(
    order: Order, product: Product, phone_number: str
) -> str:
    return (
        f'Заказ #{order.id}\n'
        f'Адрес доставки: {order.address}\n'
        f'Кол-во товаров в заказе: {order.count}\n'
        f'Сумма заказа: {order.order_sum}\n'
        f'Комментарий к заказу: {order.comment}\n'
        f'Дата создания заказа: {order.created_date}\n\n'
        f'Товар\n'
        f'ID: {product.id}\n'
        f'Название: {product.name}\n'
        f'Цена: {product.price}\n'
        f'Заказчик: +{user_mention_text_html(order.user, phone_number)}'
    )


def review_display_text(review: Review) -> str:
    return (
        f'⭐: {review.rate * "⭐"}\n'
        f'✒️: {review.review}\n'
        f'Статус: {review.status.get_choice_value(review.status)}'
    )
