from pydantic import BaseModel, Field
from typing import Optional, List
from database import get_connection, init_db, get_stats
from models import Item, ItemOut  # <-- Важно: импортируем модели
from starlette.exceptions import HTTPException as StarletteHTTPException
import sqlite3
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# 1. Загружаем ключ
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError(" API_KEY не найден! Проверь файл .env")

print(f"Ключ загружен: {API_KEY[:5]}...")

app = FastAPI()
security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Эта функция может быть обычной (не async), потому что она просто проверяет данные
def get_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None or credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key"
        )
    return credentials.credentials

@app.on_event("startup")
def startup():
    """Инициализация базы данных при старте сервера"""
    logging.info(" Server starting, initializing DB...")
    init_db()
    logging.info(" Database initialized")



@app.get("/")
def read_root():
    logging.info("GET / called")
    return {"message": "Сервер работает, данные берем из SQLite"}


@app.get("/items", response_model=List[ItemOut])
def get_items(min_price: Optional[float] = None):
    logging.info("GET /items called")
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
    logging.info(f"GET /items/{item_id} called")
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
    logging.info("GET /stats called")
    stats = get_stats()
    # get_stats возвращает кортеж (count, total_price), превратим в словарь для красоты
    count, total_price = stats
    return {"total_items": count, "total_price": total_price}


@app.post("/items/", response_model=ItemOut)
def create_item(item: Item):
    logging.info("POST /items/ called")
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO items (name, price, description) VALUES (?, ?, ?)",
            (item.name, item.price, item.description)
        )
        conn.commit()
        new_id = cursor.lastrowid

        logging.info(f" Создан товар id={new_id}, name={item.name}")
        return ItemOut(
            id=new_id,
            name=item.name,
            price=item.price,
            description=item.description
        )
    except Exception as e:
        conn.rollback()
        logging.exception(" Ошибка при создании товара")  # .exception пишет и сообщение, и стек-трейс
        raise HTTPException(status_code=500, detail=f"Ошибка при создании: {e}")
    finally:
        conn.close()

# 1. Функция проверки (синхронная)
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Твоя простая логика проверки токена
    if token != "test_token_12345_just_for_swagger":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": "admin"}

# 2. Защищённый эндпоинт (синхронный)
@app.get("/protected")
def get_protected_data(current_user: dict = Depends(get_current_user)):
    return {"message": "Success!", "user": current_user}

# 3. Эндпоинт выдачи токена (синхронный)
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "admin" and form_data.password == "password":
        return {"access_token": "test_token_12345_just_for_swagger", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Bad credentials")


# Блок для ручного запуска (python main.py)
if __name__ == "__main__":
    import uvicorn

    # Здесь можно временно раскомментировать seed_data(), если нужно быстро наполнить базу
    # from database import seed_data
    # seed_data()

    uvicorn.run(app, host="127.0.0.1", port=8000)
