from database import init_db, seed_data, get_connection

# 1. Готовим базу (если нет таблицы — создаст, если есть — ничего не сделает)
init_db()

# 2. Добавляем тестовые товары, если база пустая
seed_data()

# 3. Подключаемся и делаем SELECT
conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM items")
rows = cursor.fetchall()

print("\n--- Список товаров из БД ---")
items_list = []

for row in rows:
    item_id, name, price = row
    # Превращаем кортеж в словарь — это и есть "вернуть как список"
    item = {
        "id": item_id,
        "name": name,
        "price": price
    }
    items_list.append(item)
    print(f"ID: {item_id} | Товар: {name} | Цена: {price} руб.")

print("\nИтоговый список (для передачи в API):")
print(items_list)

conn.close()
