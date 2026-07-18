from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from typing import List

app = FastAPI()

class ItemOut(BaseModel):
    id: int
    name: str
    price: float

items_db = [
    {"id": 1, "name": "Кофе", "price": 200.5},
    {"id": 2, "name": "Чай", "price": 150.0},
    {"id": 3, "name": "Булочка", "price": 80.25},
]

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

# Блок запуска (работает только если ты запускаешь файл напрямую)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

