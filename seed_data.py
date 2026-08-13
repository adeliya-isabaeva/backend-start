import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Подтягиваем переменные из .env (как в твоём проекте)
DB_USER = os.getenv("POSTGRES_USER", "shop_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret_password")
DB_HOST = os.getenv("DB_HOST", "localhost")  # Если запускаешь из контейнера, будет имя сервиса
DB_NAME = os.getenv("POSTGRES_DB", "shop_db")

# ВАЖНО: если ты запускаешь этот скрипт из хоста (не из контейнера),
# используй host=db (если внутри compose) или host=localhost (если база отдельно).
# Для Docker Compose лучше запускать скрипт как часть контейнера или через docker exec.
# Самый простой вариант для начала: запустить через docker exec в контейнере БД.

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"
# Если будешь запускать локально вне Docker, замени @db на @localhost

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed():
    session = SessionLocal()
    try:
        # Сначала удаляем старые тестовые товары, чтобы не дублировались
        session.execute(text("DELETE FROM items WHERE name LIKE 'Test item%'"))
        session.commit()

        items = [
            ("Test item 1", 100.0, "Описание первого товара"),
            ("Test item 2", 250.5, "Описание второго товара"),
            ("Test item 3", 99.99, "Описание третьего товара"),
            ("Test item 4", 450.0, "Описание четвёртого товара"),
            ("Test item 5", 79.9, "Описание пятого товара"),
            ("Test item 6", 199.0, "Описание шестого товара"),
            ("Test item 7", 320.25, "Описание седьмого товара"),
            ("Test item 8", 89.99, "Описание восьмого товара"),
            ("Test item 9", 550.0, "Описание девятого товара"),
            ("Test item 10", 129.99, "Описание десятого товара"),
        ]

        for name, price, description in items:
            session.execute(
                text("INSERT INTO items (name, price, description) VALUES (:name, :price, :description)"),
                {"name": name, "price": price, "description": description}
            )
        session.commit()
        print("✅ Seed data inserted successfully!")
    except Exception as e:
        session.rollback()
        print(f"❌ Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed()
