import os
from dataclasses import dataclass
from pathlib import Path

from environs import Env

from tgbot.services.payment.service import Currency, UzSumCurrency


@dataclass(frozen=True)
class DbConfig:
    host: str
    port: int
    database: str

    @property
    def sync_url(self) -> str:
        raise NotImplementedError

    @property
    def async_url(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class PostgresDbConfig(DbConfig):
    password: str
    user: str

    @property
    def sync_url(self) -> str:
        return (
            f'postgresql+psycopg2://{self.user}:{self.password}'
            f'@{self.host}:{self.port}/{self.database}'
        )

    @property
    def async_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.user}:{self.password}'
            f'@{self.host}:{self.port}/{self.database}'
        )


@dataclass(frozen=True)
class RedisDbConfig(DbConfig):
    database: int | str = 1

    @property
    def sync_url(self) -> str:
        return f'redis://{self.host}:{self.port}/{self.database}'

    @property
    def async_url(self) -> str:
        return self.sync_url


@dataclass(frozen=True)
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool
    payment_token: str
    payment_currency: Currency
    referred_user_bonus: int


@dataclass(frozen=True)
class Misc:
    ADMINS_PAGINATE_PER_COUNT: int = 12
    PRODUCTS_PAGINATE_PER_COUNT: int = 1
    MEDIA_DIR: Path = Path(__file__).parent.parent / 'media'
    PHOTOS_DIR: Path = MEDIA_DIR / 'photos'
    PRODUCT_PHOTOS_DIR: Path = PHOTOS_DIR / 'product'
    QR_CODES_DIR: Path = PHOTOS_DIR / 'qr_codes'


@dataclass(frozen=True)
class Config:
    tg_bot: TgBot
    main_db: PostgresDbConfig
    cache_db: RedisDbConfig
    misc: Misc


def make_dirs_if_not_exist(path: Path | str) -> Path | str:
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def make_misc_dirs(misc: Misc) -> Misc:
    for attr_name, attr_value in misc.__dict__.items():
        if isinstance(attr_value, Path):
            make_dirs_if_not_exist(attr_value)
    return misc


def load_config(path: str | None = None):
    env = Env()
    if path:
        env.read_env(path)
    misc = Misc()
    make_misc_dirs(misc)
    return Config(
        tg_bot=TgBot(
            token=env.str('BOT_TOKEN'),
            admin_ids=[int(id_) for id_ in env.list('ADMINS')],
            use_redis=env.bool('USE_REDIS'),
            payment_token=env.str('PAYMENT_TOKEN'),
            payment_currency=UzSumCurrency(
                env.str('PAYMENT_CURRENCY_NAME'),
                env.str('PAYMENT_CURRENCY_CODE'),
                env.int('PAYMENT_CURRENCY_MIN_PRICE'),
                env.int('PAYMENT_CURRENCY_MAX_PRICE'),
            ),
            referred_user_bonus=env.int('REFERRED_USER_BONUS'),
        ),
        main_db=PostgresDbConfig(
            host=env.str('DB_HOST'),
            port=env.int('DB_PORT'),
            database=env.str('DB_NAME'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER')
        ),
        misc=misc,
        cache_db=RedisDbConfig(
            host=env.str('REDIS_HOST'),
            port=env.int('REDIS_PORT'),
            database=env.int('REDIS_DB'),
        )
    )
