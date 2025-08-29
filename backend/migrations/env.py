# backend/migrations/env.py
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

import os, sys
from pathlib import Path
from dotenv import load_dotenv

# --- Rutas ---
MIGR_DIR = Path(__file__).resolve().parent          # backend/migrations
BACKEND_DIR = MIGR_DIR.parent                       # backend/
sys.path.insert(0, str(BACKEND_DIR))                # añade backend/ al PYTHONPATH

# --- .env ---
load_dotenv()  # si tu .env está en la raíz, opcional: load_dotenv(BACKEND_DIR.parent / ".env")

# --- Alembic config ---
config = context.config
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# --- Logging ---
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Modelos ---
from db.session import Base      # <<-- AQUÍ el Base correcto en tu proyecto
import db.models                 # registra todos los modelos

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            # render_as_batch=True,  # sólo si usas SQLite
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
