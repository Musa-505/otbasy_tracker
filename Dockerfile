FROM python:3.11-slim

# Жұмыс директория
WORKDIR /app

# Тәуелділіктерді көшіру
COPY requirements.txt .

# Пакеттерді орнату
RUN pip install --no-cache-dir -r requirements.txt

# Барлық файлдарды көшіру
COPY . .

# Бастау командасы
CMD ["python", "main.py"]