from pathlib import Path

from aiogram.types import User
from qrcode import make

from tgbot.config import Config
from tgbot.utils.text import get_referrer_link


def get_qr_code_path(qr_codes_dir: Path | str, user_id: int) -> Path:
    if isinstance(qr_codes_dir, Path):
        qr_path = str(
            qr_codes_dir / str(user_id)
        ) + '.png'
    else:
        qr_path = str(
            qr_codes_dir + '/' + str(user_id)
        ) + '.png'
    return Path(qr_path)


def make_user_qr_code(config: Config, bot: User, user_id: int) -> Path:
    qr_code_path = get_qr_code_path(config.misc.QR_CODES_DIR, user_id)
    qr_code = make(get_referrer_link(
        bot.username, user_id
    ))
    qr_code.save(qr_code_path)
    return qr_code_path
