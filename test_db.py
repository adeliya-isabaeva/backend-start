from database import get_connection

import pytest


@pytest.fixture
def db_cursor():
    """Эта штука сама откроет и закроет базу для теста"""
    conn = get_connection()
    cursor = conn.cursor()
    yield cursor
    conn.close()


def test_check_items_in_db(db_cursor):
    """Тест: проверяем, что база подключена и товары есть"""

    # --- Твой блок с PRAGMA (проверка пути) ---
    row = db_cursor.execute("PRAGMA database_list;").fetchone()
    file_path = row
    # Вместо print используем assert: если пути нет — тест упадёт
    assert file_path is not None, f"Не удалось найти путь к БД! Получено: {row}"

    # --- Твой блок с SELECT (проверка товаров) ---
    db_cursor.execute("SELECT * FROM items")
    rows = db_cursor.fetchall()

    # Вместо красивого вывода в цикле используем assert
    assert len(rows) > 0, "Таблица items пуста! Ожидались товары."

    # Если хочешь проверить конкретный товар (как в твоём выводе), раскомментируй строку ниже:
    # assert rows == "Пирожок с вишней", "Первый товар не тот, что ожидался."
