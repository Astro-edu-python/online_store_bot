from tgbot.models.products import Product


def user_mention_text_html(chat_id: int, display_text: str):
    return f'<a href="tg://user?id={chat_id}">{display_text}</a>'


def product_info_text(product: Product) -> str:
    text = (
        f'Продукт: {product.name}',
        f'Категория: {product.category}',
        f'Описание: {product.description}',
        f'Цена: {product.price}',
        f'Кол-во в наличии: {product.stock}',
    )
    return '\n'.join(text)
