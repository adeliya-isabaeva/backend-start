import pytest
from fastapi.testclient import TestClient
from main import app  # импортируем приложение из main.py

client = TestClient(app)

def test_root_returns_200():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_items_filter_by_min_price():
    # Задаем цену, выше которой хотим получить товары
    min_price = 50
    response = client.get("/items", params={"min_price": min_price})

    # 1. Проверяем, что сервер ответил успешно
    assert response.status_code == 200

    data = response.json()

    # 2. (Опционально) Проверяем, что это список
    assert isinstance(data, list)

    # 3. ГЛАВНАЯ ПРОВЕРКА: каждый товар в ответе должен стоить >= min_price
    for item in data:
        # Предполагаем, что в словаре товара есть ключ 'price'.
        # Если у тебя ключ называется иначе (например, 'cost'), замени 'price' на нужное.
        assert item.get("price", 0) >= min_price
