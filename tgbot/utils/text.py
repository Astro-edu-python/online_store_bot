def user_mention_text_html(chat_id: int, display_text: str):
    return f'<a href="tg://user?id={chat_id}">{display_text}</a>'
