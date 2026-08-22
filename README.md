# Shop API (учебный проект)

Учебный REST API для магазина на FastAPI + SQLAlchemy + PostgreSQL. Проект собран как полноценный бэкенд: с миграциями, автотестами и CI, но сделан в учебных целях — чтобы отработать весь стек от подключения БД до покрытия тестами.

## Цели проекта
В рамках обучения отработаны:
- разделение на слои (API / Repository / DB)
- работа с реальной СУБД PostgreSQL (не SQLite)
- миграции Alembic и применение схемы БД
- валидация данных через Pydantic
- автотесты (pytest) и автоматическая проверка в CI (GitHub Actions)

## Функционал

- `GET /` — проверка, что сервер работает
- `GET /items` — список всех товаров
- `GET /items/{item_id}` — товар по ID
- `POST /items` — создание товара

## Стек

- FastAPI
- SQLAlchemy (ORM)
- Pydantic (валидация)
- PostgreSQL (СУБД) + psycopg2 (драйвер)
- Alembic (миграции)
- pytest (тесты)
- GitHub Actions (CI)

## Как запустить локально

1. **Запустите PostgreSQL** (локально или в Docker).  
   Если используете Docker:
 
   ```bash
   docker compose up -d.

2. Создайте виртуальное окружение:

   ```bash
   python -m venv venv

3. Активируйте его (Windows):

   ```bash
   venv\Scripts\activate

4. Установите зависимости:

   ```bash
   pip install -r requirements.txt

5. Настройте переменные окружения: создайте .env на основе .env.example.
Проверьте, что DATABASE_URL указывает на ваш PostgreSQL, например:

   ```python
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/shop_db

6. Примените миграции:

   ```bash
   alembic upgrade head

7. Запустите сервер:

   ```bash
   uvicorn main:app --reload

Сервер будет доступен по адресу: `http://127.0.0.1:8000`.

**Документация и тестирование API**

После запуска сервера откройте:

- Swagger UI (интерактивная документация и тесты эндпоинтов):

    `http://localhost:8000/docs`

- ReDoc (альтернативная документация):

    `http://localhost:8000/redoc`

    Важно: Swagger генерируется самим FastAPI и доступен только когда сервер запущен и успешно подключена база данных.

##Тесты

- Локально:

   ```bash
   pytest

- Автоматически: при каждом push тесты запускаются в CI через

   `.github/workflows/ci.yml`.

## Примеры запросов (curl)

Эти команды позволяют проверить работу API без браузера. Сервер должен быть запущен:
 
   ```bash
   uvicorn main:app --reload
   
Быстрый старт

### Статус сервера

   ```bash
   curl http://localhost:8000/

### Список товаров

   ```bash
   curl http://localhost:8000/items

### Товар по ID

   ```bash
   curl http://localhost:8000/items/1

### Создание товара (POST)

   ```bash
   curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Планшет\",\"price\":45000,\"stock_quantity\":7,\"description\":\"Планшет для учёбы\"}"

## Что будет в ответе (примеры)

### От `GET /`

```json
{
  "status": "ok",
  "message": "Сервер работает"
}

### От POST /items (успех, 201 Created)

```json
{
  "id": 5,
  "name": "Планшет",
  "price": 45000,
  "stock_quantity": 7,
  "description": "Планшет для учёбы"
}

### От GET /items/999 (товар не найден)

```json
{
  "detail": "Товар не найден"
}
(и статус 404)

## Примеры работы API

### Документация и общая структура
Здесь представлена автоматически сгенерированная документация Swagger UI, где видны все доступные эндпоинты и их методы.

![Обзор Swagger UI](screenshots/swagger-ui-overview.png)

### Успешное получение данных
Запрос `GET /items` возвращает пустой список (так как база изначально пуста). Статус `200 OK` подтверждает корректную работу соединения с базой данных и отсутствие ошибок на стороне сервера.

![Успешный GET-запрос (список)](screenshots/get-items-200-ok.png)

### Получение элемента по ID
Протестированы оба сценария работы эндпоинта `GET /items/{item_id}`:
*   **Успешный ответ (200 OK):** элемент найден.
*   **Ошибка (404 Not Found):** элемент с указанным ID не существует.

Такая проверка гарантирует, что API корректно обрабатывает как валидные, так и невалидные запросы.

![GET по ID (успех)](screenshots/get-items-item_id-200-ok.png)
![GET по ID (ошибка 404)](screenshots/get-items-item_id-404-not_found.png)

### Создание новой записи
Запрос `POST /items` успешно создаёт новую запись в базе данных. Статус `201 Created` и тело ответа подтверждают, что данные были сохранены.

![Создание товара (POST)](screenshots/post-items-201-created.png)

##Структура проекта

    `main.py` — роуты и эндпоинты
    `repository.py` — логика работы с БД (CRUD)
    `schemas.py` — Pydantic-модели
    `database.py` — настройка сессии и подключения к PostgreSQL
    `alembic/` — миграции
    `tests/` — автотесты
    `.github/workflows/ci.yml` — настройка CI
    `.env`, `.env.example` — переменные окружения

##Статус

Проект учебный: сделан для отработки стека FastAPI + PostgreSQL + CI. Не предназначен для продакшена.