from logging.config import fileConfig
from urllib.parse import quote_plus
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models import Base
from app.config import settings

# Alembic Config object
config = context.config

# 1. URL-encode password ('@' becomes '%40')
encoded_pass = quote_plus(settings.database_password)

# 2. Escape '%' for configparser ('%40' becomes '%%40')
escaped_pass_for_ini = encoded_pass.replace("%", "%%")

# 3. Build connection string safely
db_url = f"postgresql+psycopg2://{settings.database_username}:{escaped_pass_for_ini}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# 4. Set the main option
config.set_main_option("sqlalchemy.url", db_url)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Model metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()