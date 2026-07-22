import sqlite3
from pathlib import Path

# Путь к файлу базы данных (он появится рядом с файлами проекта)
DB_PATH = Path("shop.db")

def get_connection():
    """Возвращает соединение с базой данных SQLite"""
    conn = sqlite3.connect(DB_PATH)
    # Эта строчка — маленькая хитрость: она позволяет обращаться к данным по именам колонок
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Создаёт таблицу items, если её нет"""
    conn = get_connection()
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL
    );
    """

    cursor.execute(create_table_sql)
    conn.commit()  # Важно: сохраняем изменения в базе
    conn.close()


def seed_data():
    """Добавляет тестовые товары, если таблица пустая"""
    conn = get_connection()
    cursor = conn.cursor()

    # Сначала проверим, есть ли уже товары
    cursor.execute("SELECT count(*) FROM items")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_items = [
            ("Пирожок с вишней", 120.5),
            ("Булочка с корицей", 95.0),
            ("Круассан", 150.0)
        ]
        cursor.executemany(
            "INSERT INTO items (name, price) VALUES (?, ?)",
            sample_items
        )
        conn.commit()
        print("Тестовые товары добавлены в базу!")
    else:
         print("В базе уже есть товары, seed не нужен.")

    conn.close()


def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    # Магия SQL: база сама всё посчитает и вернёт одну строчку
    cursor.execute("SELECT COUNT(*) AS count, SUM(price) AS total_price FROM items")

    # fetchone() достаёт только одну строку результата
    row = cursor.fetchone()

    conn.close()
    return row
