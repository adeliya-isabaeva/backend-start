from fastapi import FastAPI, HTTPException
from repository import get_all_items, get_item_by_id, create_item
from schemas import ItemCreate, ItemOut
from typing import List  # Добавлен для совместимости со старыми версиями Python

app = FastAPI(title="Shop API", version="1.0.0")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Сервер работает"}

@app.get("/items", response_model=List[ItemOut])
def read_items():
    return get_all_items()

@app.get("/items/{item_id}", response_model=ItemOut)
def read_item(item_id: int):
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return item

@app.post("/items", response_model=ItemOut)
def add_item(item: ItemCreate):
    return create_item(
        name=item.name,
        price=item.price,
        stock_quantity=item.stock_quantity,
        description=item.description,
    )
