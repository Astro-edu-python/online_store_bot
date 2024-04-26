from dataclasses import dataclass

from environs import Env


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


@dataclass(frozen=True)
class Config:
    tg_bot: TgBot
    main_db: PostgresDbConfig


def load_config(path: str | None = None):
    env = Env()
    if path:
        env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str('BOT_TOKEN'),
            admin_ids=env.list('ADMINS'),
            use_redis=env.bool('USE_REDIS'),
        ),
        main_db=PostgresDbConfig(
            host=env.str('DB_HOST'),
            port=env.int('DB_PORT'),
            database=env.str('DB_NAME'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER')
        )
    )
