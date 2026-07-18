from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Простая модель данных
class Item(BaseModel):
    name: str
    price: float

# Эндпоинт, который просто здоровается (чтобы проверить, что сервер жив)
@app.get("/")
def read_root():
    return {"message": "Привет! Бэкенд работает!"}

# Эндпоинт, который принимает данные (аналог твоего задания с обработкой)
@app.post("/items")
def create_item(item: Item):
    return {"message": "Товар создан", "data": item}

# Блок запуска (работает только если ты запускаешь файл напрямую)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

