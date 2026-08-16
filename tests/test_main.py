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


def test_create_item_returns_201():  # <-- переименуем функцию
    payload = {
        "name": "Test Item",
        "price": 123.45,
        "stock_quantity": 10,
        "description": "Just a test"
    }
    response = client.post("/items", json=payload)

    assert response.status_code == 201  # <-- теперь это будет правдой
    data = response.json()

    assert data["name"] == payload["name"]
    assert abs(data["price"] - payload["price"]) < 0.01
    assert data["stock_quantity"] == payload["stock_quantity"]

def test_create_item_returns_422():  # <-- переименуем функцию
    payload = {
        "name": "Bad Item",
        "price": -10.0,
        "stock_quantity": 5,
        "description": "Should fail"
    }
    response = client.post("/items", json=payload)

    assert response.status_code == 422  # <-- теперь это будет правдой
    data = response.json()

 # 2. Проверяем, что в ответе есть список ошибок (стандартная структура FastAPI + Pydantic)
    assert "detail" in data, "В ответе на 422 должно быть поле detail"
    assert isinstance(data["detail"], list), "detail должен быть списком ошибок"
    assert len(data["detail"]) > 0, "Должна быть хотя бы одна ошибка валидации"

    # 3. (Опционально) Проверяем, что ошибка касается именно price
    first_error = data["detail"][0]
    # В loc путь к полю: ["body", "price"]
    assert "price" in first_error.get("loc", []), "Ошибка должна относиться к полю price"

def test_items_returns_200():  # Переименовали функцию, чтобы не путаться
    response = client.get("/items")
    assert response.status_code == 200  # Было 404, стало 200
    data = response.json()
    # Можно проверить, что это список (даже если он пустой)
    assert isinstance(data, list)

def test_get_item_by_nonexistent_id_returns_404():
    # 1. Создаём товар, чтобы база не была пустой
    payload = {"name": "Existing Item", "price": 99.99, "stock_quantity": 5}
    create_resp = client.post("/items", json=payload)
    assert create_resp.status_code == 201
    real_id = create_resp.json()["id"]

    # 2. Пробуем получить несуществующий ID
    nonexistent_id = real_id + 1000
    response = client.get(f"/items/{nonexistent_id}")

    # 3. Проверяем статус
    assert response.status_code == 404

    data = response.json()

    # 4. Проверяем текст ошибки.
    # Так как у тебя "Товар не найден", ищем эти слова.
    error_text = str(data).lower()
    assert "товар" in error_text and "не найден" in error_text, "Ошибка должна говорить, что товар не найден"
