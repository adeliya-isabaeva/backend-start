from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from database import get_connection, get_stats
import sqlite3
from database import init_db
init_db()

app = FastAPI()

class ItemOut(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None

class Item(BaseModel):
    name: str
    price: float = Field(gt=0)
    description: Optional[str] = None


# УДАЛИ эти строки (старый список и счетчик), они больше не нужны для чтения из БД:
# items_db = [...]
# next_id = ...

@app.get("/")
def read_root():
    return {"message": "Сервер работает, данные берем из SQLite"}


@app.get("/hello/{name}")
def read_hello(name: str):
    return {"message": f"Привет, {name}!"}


@app.get("/math/sum/{a}/{b}")
def math_sum(a: int, b: int):
    return {"a": a, "b": b, "sum": a + b}


# ЭТА ФУНКЦИЯ (СПИСОК ТОВАРОВ) ОСТАЕТСЯ БЕЗ ИЗМЕНЕНИЙ - ОНА ПРАВИЛЬНАЯ
@app.get("/items", response_model=List[ItemOut])
def get_items(min_price: Optional[float] = None):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, name, price FROM items"
    params = []

    if min_price is not None:
        query += " WHERE price >= ?"
        params.append(min_price)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    result=[]

    for row in rows:
        # ПРАВИЛЬНО: превращаем строку в словарь
        result.append({"id": row["id"], "name": row["name"], "price": row["price"]})

    return result

# ЭТА ФУНКЦИЯ (ОДИН ТОВАР ПО ID) НУЖДАЕТСЯ В ЗАМЕНЕ:
# Она должна искать в БД, а не в списке items_db
@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    conn = get_connection()
    conn.row_factory = sqlite3.Row  # Чтобы удобно брать данные по имени колонки
    cursor = conn.cursor()

    # Ищем товар с конкретным ID
    cursor.execute("SELECT id, name, price FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Товар с таким ID не найден в базе данных"
        )

    # Возвращаем как словарь, Pydantic сам превратит в ItemOut
    return {"id": row["id"], "name": row["name"], "price": row["price"]}


@app.get("/stats")
def get_stats_endpoint():
    stats = get_stats()  # <-- «Эй, кухня, дай статистику!»
    return stats  # <-- «И сразу отдаю её гостю»


# ВАЖНО: Функция create_item тоже должна писать в БД, а не в список.
# Пока мы её закомментируем или оставим как есть, если план не требует записи.
# Если нужно сделать запись в БД - скажи, я дам код.
@app.post("/items/", response_model=ItemOut)
def create_item(item: Item):
    conn = get_connection()          # ты это уже написала — отлично
    cursor = conn.cursor()           # обязательно нужен курсор для SQL

    try:
        cursor.execute(
            "INSERT INTO items (name, price, description) VALUES (?, ?, ?)",
            (item.name, item.price, item.description)
        )
        conn.commit()                 # без этого INSERT не сохранится!

        new_id = cursor.lastrowid     # вот тут база сама отдаёт ID, который создала

        return ItemOut(
            id=new_id,
            name=item.name,
            price=item.price,
            description=item.description
        )

    except Exception as e:
        conn.rollback()               # если ошибка — отменяем всё, что начали
        raise HTTPException(status_code=500, detail=f"Ошибка при создании: {e}")

    finally:
        conn.close()                  # вот это обязательно: закрываем соединение всегда


if __name__ == "__main__":
    import uvicorn
    init_db()
    seed_data()
    uvicorn.run(app, host="127.0.0.1", port=8000)
