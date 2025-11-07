from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Alembic Config object
config = context.config

# Set up logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------
# Import your SQLAlchemy Base
# ---------------------------
from app.db import Base 
target_metadata = Base.metadata

# ---------------------------
# Use DATABASE_URL from .env
# ---------------------------
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise Exception("DATABASE_URL environment variable is missing")

# Override alembic.ini URL
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# ---------------------------
# Offline migrations
# ---------------------------
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------
# Online migrations
# ---------------------------
def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------
# Run appropriate mode
# ---------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
