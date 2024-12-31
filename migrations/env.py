# alembic/env.py
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context
from logging.config import fileConfig


# Add the root directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import app.models
# Import Base from app.models.base (doesn't need to import individual models)
from app.models.base import Base  # This imports Base, and all models inherit from it

# Load environment variables from .env file
load_dotenv()

# Set the target_metadata to Base.metadata for Alembic to detect models
target_metadata = Base.metadata

# Get the database URL from environment variables
url = os.getenv("DATABASE_URL", "postgresql://root:root@localhost:5432/myapp_db")

# Set the sqlalchemy.url in Alembic config
config = context.config
if url:
    config.set_main_option("sqlalchemy.url", url)

# This part configures the logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Migration functions
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
