from tgbot.models.products import Product


def user_mention_text_html(chat_id: int, display_text: str) -> str:
    return f'<a href="tg://user?id={chat_id}">{display_text}</a>'


def get_referrer_link(bot_username: str, user_id: int) -> str:
    return f'https://t.me/{bot_username}?start=referrer{user_id}'


def product_info_text(product: Product) -> str:
    text = (
        f'Продукт: {product.name}',
        f'Категория: {product.category}',
        f'Описание: {product.description}',
        f'Цена: {product.price}',
        f'Кол-во в наличии: {product.stock}',
    )
    return '\n'.join(text)
