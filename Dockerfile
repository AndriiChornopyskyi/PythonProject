# 1. Використовуємо офіційний Python образ
FROM python:3.10-slim

# 2. Встановлюємо робочу директорію
WORKDIR /app

# 3. Копіюємо файли в контейнер
COPY . .

# 4. Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# 5. Відкриваємо порт для Flask
EXPOSE 8080

# 6. Запускаємо додаток
CMD ["python", "app.py"]