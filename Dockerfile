FROM python:3.9-slim

# Создаем папку /app внутри контейнера и заходим в неё
WORKDIR /app

# 1. Сначала копируем ТОЛЬКО список нужных программ (requirements.txt)
# Это нужно, чтобы Docker запомнил этот шаг и не качал всё заново при каждом изменении кода
COPY requirements.txt .

# 2. Устанавливаем эти программы (включая тот самый dotenv, из-за которого была ошибка)
RUN pip install --no-cache-dir -r requirements.txt

# 3. КОПИРУЕМ ВСЁ ОСТАЛЬНОЕ: main.py, models.py, database.py и т.д.
# Вот эта строчка решает твою проблему с ошибкой "requires two arguments"
COPY . .

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
