# FastAPI Auth & Items API Demo

Учебный бэкенд-сервис на FastAPI: CRUD для товаров, авторизация (OAuth2), защита API‑ключом. Проект демонстрирует понимание базовых паттернов разработки и безопасности.

> ⚠️ **ВАЖНО: учебный проект**  
> - Учётные данные (`admin` / `password`) и токены — тестовые, только для локальной проверки.  
> - Логика авторизации намеренно упрощена для наглядности.  
> **Не использовать в продакшен-системах.**

## Стек технологий

- Python 3.10+
- FastAPI + Uvicorn
- SQLite (SQLAlchemy)
- OAuth2 Password Flow
- API Key защита
- Swagger UI, ReDoc

## Установка и запуск

1. Установи зависимости:
   ```bash
   pip install -r requirements.txt

2. Создай (или проверь) файл `.env` в папке проекта. В нём должна быть строка:
    
    ```text
    API_KEY=super_secret_key_123

3. Запусти сервер:

    ```bash
    uvicorn main:app --reload

4. Открой документацию:

    Swagger UI (с кнопками «Try it out»): http://127.0.0.1:8000/docs
    ReDoc (аккуратная справка): http://127.0.0.1:8000/redoc

## Эндпоинты

### Публичные (без авторизации)

- `GET /` — проверка работы сервера.
- `GET /items` — список товаров.
- `GET /items/{item_id}` — получение товара по ID.
- `GET /stats` — статистика.

---

### Авторизация (OAuth2 Password Flow)

- `POST /token` — получить токен.  
  Входные данные: `username=admin`, `password=password`.  

  **Пример ответа:**

[  ```json
  {
    "access_token": "test_token_12345_just_for_swagger",
    "token_type": "bearer"
  }
  
    `GET /protected` — защищённый ресурс.]()
  
Требуется заголовок: `Authorization: Bearer <access_token>`.

## CRUD (создание товаров)

    `POST /items/` — создать товар.

    Тело запроса (JSON):

    ```json
    {
      "name": "Новый товар",
      "price": 1200,
      "description": "Описание товара"
    }

## Пример типичного запроса и ответа

Этот пример показывает, как клиент взаимодействует с эндпоинтом создания товара.

Запрос (curl):

    ```bash
    curl -X 'POST' 'http://127.0.0.1:8000/items/' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
        "name": "strawberry",
        "price": 400,
        "description": "sweet"
      }'

Ответ (JSON):

    ```json
    {
      "id": 6,
      "name": "strawberry",
      "price": 400,
      "description": "sweet"
    }

## Безопасность и .gitignore

Файл `.env` и служебные данные категорически запрещено коммитить в Git.

Убедись, что в твоём файле `.gitignore` (в корне проекта) есть следующие строки:

    ```text
    .env
    venv/
    __pycache__/
    *.pyc
    shop.db
    .DS_Store
    app.log
    screenshots/

Важно: если файл `.env` уже был добавлен в историю коммитов, простого добавления в `.gitignore` недостаточно. Выполни:

    ```bash
    git rm --cached .env
    git commit -m "Remove .env from tracking"

## Скриншоты работы API

### Интерфейс Swagger (эндпоинт создания товара)
![Swagger UI с полями запроса](screenshots/swagger-post-expanded.png)

### Ответ сервера (реальный JSON с id: 6)
![JSON ответ после POST-запроса](screenshots/swagger-response.png)




