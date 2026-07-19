from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from typing import List

app = FastAPI()

class ItemOut(BaseModel):
    id: int
    name: str
    price: float

class Item(BaseModel):
    name: str
    price: float = Field(gt=0)


items_db = [
    {"id": 1, "name": "Кофе", "price": 200.5},
    {"id": 2, "name": "Чай", "price": 150.0},
    {"id": 3, "name": "Булочка", "price": 80.25},
]

next_id = len(items_db) + 1  # Считаем, сколько товаров уже есть, и берём следующий номер

# 1. Этот маршрут отвечает за ГЛАВНУЮ страницу (/)
@app.get("/")
def read_root():
    return {"message": "Я сама это поменяла, и сервер это отдал!"}

# 2. Этот маршрут отвечает за страницу с именем (/hello/{name})
@app.get("/hello/{name}")
def read_hello(name: str):
    return {"message": f"Привет, {name}!"}

@app.get("/math/sum/{a}/{b}")
def math_sum(a: int, b: int):
    result = a + b
    return {"a": a, "b": b, "sum": result}


@app.get("/items", response_model=List[ItemOut])
def get_items(min_price: Optional[float] = None):
    result = items_db
    if min_price is not None:
        result = [item for item in result if item["price"] >= min_price]

    # FastAPI сам возьмет наши словари из items_db
    # и превратит их в объекты ItemOut. Нам ничего делать не надо!
    return result


@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item

    # Если ничего не нашли — выбрасываем красивую ошибку
    raise HTTPException(
        status_code=404,
        detail="Товар с таким ID не найден"
    )

@app.post("/items/", response_model=ItemOut)
def create_item(item: Item):
    global next_id, items_db

    new_item = {
        "id": next_id,
        "name": item.name,
        "price": item.price
    }

    items_db.append(new_item)
    next_id += 1

    return ItemOut(**new_item)

# Блок запуска (работает только если ты запускаешь файл напрямую)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

