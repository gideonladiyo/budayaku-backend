# Gunakan image dasar Python
FROM python:3.11-slim
WORKDIR /app
# Salin file requirements.txt dan instal dependensi
COPY requirements.txt .
# Instal dependensi Python
RUN pip install --no-cache-dir -r requirements.txt
# Salin seluruh kode aplikasi ke dalam container
COPY . .
# Perintah untuk menjalankan aplikasi menggunakan Uvicorn
# Railway akan menyediakan environment variable PORT secara otomatis
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips=*