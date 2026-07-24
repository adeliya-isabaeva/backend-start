from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from database import get_connection, init_db, get_stats
from models import Item, ItemOut  # <-- Важно: импортируем модели
import sqlite3

app = FastAPI()


@app.on_event("startup")
def startup():
    """Инициализация базы данных при старте сервера"""
    init_db()
    # seed_data() здесь НЕ вызываем! Иначе при каждой перезагрузке (--reload)
    # в базу будут добавляться новые копии товаров.


@app.get("/")
def read_root():
    return {"message": "Сервер работает, данные берем из SQLite"}


@app.get("/items", response_model=List[ItemOut])
def get_items(min_price: Optional[float] = None):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT id, name, price, description FROM items"
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
        result.append({"id": row["id"], "name": row["name"], "price": row["price"], "description": row["description"]})

    return result


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    conn = get_connection()
    conn.row_factory = sqlite3.Row  # Теперь можно обращаться по именам колонок
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, price, description FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Товар с таким ID не найден в базе данных"
        )

    return {
        "id": row["id"],
        "name": row["name"],
        "price": row["price"],
        "description": row["description"]
    }


@app.get("/stats")
def get_stats_endpoint():
    stats = get_stats()
    # get_stats возвращает кортеж (count, total_price), превратим в словарь для красоты
    count, total_price = stats
    return {"total_items": count, "total_price": total_price}


@app.post("/items/", response_model=ItemOut)
def create_item(item: Item):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO items (name, price, description) VALUES (?, ?, ?)",
            (item.name, item.price, item.description)
        )
        conn.commit()
        new_id = cursor.lastrowid

        return ItemOut(
            id=new_id,
            name=item.name,
            price=item.price,
            description=item.description
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при создании: {e}")
    finally:
        conn.close()


# Блок для ручного запуска (python main.py)
if __name__ == "__main__":
    import uvicorn

    # Здесь можно временно раскомментировать seed_data(), если нужно быстро наполнить базу
    # from database import seed_data
    # seed_data()

    uvicorn.run(app, host="127.0.0.1", port=8000)
