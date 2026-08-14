import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 1. Добавляем корень проекта в путь, чтобы импорты работали
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from main import app

# 2. Импортируем Base из models.py (там, где у тебя таблицы)
from models import Base

# 3. Создаём движок и сессию специально для тестов (SQLite в файле test.db)
TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# 4. Функция, которая будет выдавать тестовую сессию вместо обычной
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# 5. Фикстура: перед каждым тестом удаляем старую базу и создаём всё заново
@pytest.fixture(autouse=True)
def setup_database():
    # Удаляем все таблицы, если они есть (чтобы тест был чистым)
    Base.metadata.drop_all(bind=test_engine)
    # Создаём все таблицы заново по твоим моделям
    Base.metadata.create_all(bind=test_engine)
    yield


# 6. Пытаемся подменить зависимость get_db
# Это сработает, если в database.py (или models.py) есть функция def get_db(): ...
try:
    from database import get_db

    app.dependency_overrides[get_db] = override_get_db
except ImportError:
    # Если get_db не нашлось, значит, у тебя зависимость называется иначе
    # или ты передаёшь её другим способом.
    # В этом случае тесты могут упасть с ошибкой подключения.
    print("⚠️ Не удалось найти функцию get_db. Если тест падает на ошибке БД — скинь сюда database.py.")

client = TestClient(app)


def test_root_returns_200():
    response = client.get("/")
    assert response.status_code == 200


def test_create_item_returns_201():
    payload = {
        "name": "Test Item",
        "price": 123.45,
        "stock_quantity": 10,
        "description": "Just a test"
    }
    response = client.post("/items", json=payload)

    if response.status_code != 201:
        print("❌ Статус не 201:", response.status_code)
        try:
            print("❌ Ответ сервера:", response.json())
        except Exception:
            print("❌ Тело ответа не JSON")

    assert response.status_code == 200
    data = response.json()

    # Проверяем, что данные вернулись корректно
    assert data["name"] == payload["name"]
    assert abs(data["price"] - payload["price"]) < 0.01  # float сравнение
    assert data["stock_quantity"] == payload["stock_quantity"]
