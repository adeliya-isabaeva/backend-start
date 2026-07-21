from database import get_connection

conn = get_connection()
cursor = conn.cursor()

# Делаем запрос
row = conn.execute("PRAGMA database_list;").fetchone()

# row — это как коробочка с 3 вещами: [0]=seq, [1]=name, [2]=file_path
# Нам нужен именно третий элемент — [2]
file_path = row[2]

print("База данных подключена! Файл:", file_path)

# --- ДОБАВЛЯЕМ ЭТОТ БЛОК ---
print("\n--- Смотрим товары из таблицы items ---")

# Делаем обычный SELECT запрос
cursor.execute("SELECT * FROM items")
rows = cursor.fetchall()

# Красиво выводим каждый товар
for row in rows:
    # row — это кортеж: (id, name, price)
    item_id, name, price = row
    print(f"ID: {item_id} | Товар: {name} | Цена: {price} руб.")

conn.close()
