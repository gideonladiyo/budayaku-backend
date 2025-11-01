# Gunakan image dasar Python yang ringan
FROM python:3.11-slim

# Tentukan direktori kerja di dalam container
WORKDIR /app

# Salin file requirements.txt terlebih dahulu untuk cache layer
COPY requirements.txt .

# Instal dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasi ke dalam container
COPY . .

# Set environment variable untuk port (Railway akan otomatis mengatur nilai PORT)
ENV PORT=8000

# Expose port untuk dokumentasi (tidak wajib di Railway, tapi baik untuk eksplisit)
EXPOSE 8000

# Jalankan server FastAPI menggunakan Uvicorn dengan proxy headers untuk Railway
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT} --proxy-headers --forwarded-allow-ips='*'"]
