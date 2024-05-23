import sys
from logging.config import fileConfig
from pathlib import Path

from environs import Env
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

BASE_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(BASE_DIR))

from tgbot.config import PostgresDbConfig
import tgbot.models.user
import tgbot.models.products
from tgbot.models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base


env = Env()
env.read_env(str(BASE_DIR / '.env'))
db_config = PostgresDbConfig(
    env.str('DB_HOST'), env.int('DB_PORT'), env.str('DB_NAME'),
    env.str('DB_PASS'), env.str('DB_USER')
)
config.set_main_option('sqlalchemy.url', db_config.sync_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        include_schemas=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
