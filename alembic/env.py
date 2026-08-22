from logging.config import fileConfig
import os
from dotenv import load_dotenv

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 1. Сначала пробуем загрузить .env (для локальной разработки)
# Если файла нет (как в CI), эта функция просто ничего не сделает и не вызовет ошибку
load_dotenv()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Подключаем модели
from models import Base
target_metadata = Base.metadata

# 2. Получаем URL. Приоритет: Переменная окружения (CI) > .env файл (локально)
# os.getenv вернет значение из env vars (которое мы задали в workflow.yml)
# Если его нет, возьмет то, что загрузилось из .env
database_url = os.getenv("DATABASE_URL")

# 3. ВАЖНОЕ ИЗМЕНЕНИЕ:
# Убираем жесткий raise ValueError. В CI .env файла нет, и это нормально.
# Если URL все равно не нашелся ниоткуда, тогда уже ругаемся.
if not database_url:
    # Для CI можно вывести более понятное сообщение, если что-то пошло не так
    raise ValueError(
        "Переменная окружения DATABASE_URL не найдена! "
        "Проверь .env файл (локально) или настройки GitHub Actions (CI)."
    )

# Перезаписываем значение в конфиге Alembic
config.set_main_option("sqlalchemy.url", database_url)


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
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
