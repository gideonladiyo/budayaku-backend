# Budayaku Backend – FastAPI

Backend untuk aplikasi chatbot budaya Indonesia yang terintegrasi dengan Google Gemini API.

## Fitur utama

• Chatbot budaya per provinsi
• Pembuatan gambar bertema budaya (mis. kerak telor, rumah adat)
• Text-to-speech dengan berbagai suara
• Validasi prompt: hanya topik budaya yang diterima
• List budaya yang ada di indonesia

## Langkah cepat menjalankan proyek

1. **Buat virtual environment**

   ```bash
   python -m venv myenv
   ```

2. **Aktifkan virtual environment**
   • Windows → `myenv\Scripts\activate`
   • macOS/Linux → `source myenv/bin/activate`

3. **Pasang seluruh dependensi**

   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan server FastAPI**

   ```bash
   uvicorn main:app --reload
   ```

## Pengaturan dotenv (.env)

Buat file `.env` di root proyek berisi:

```bash
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

Variabel ini di-load otomatis oleh modul konfigurasi (`python-dotenv` atau setting serupa) sehingga kunci rahasia tidak perlu ditulis langsung di kode.

## Dokumentasi otomatis API

• Swagger UI   → [http://localhost:8000/docs](http://localhost:8000/docs)

Selesai – backend siap digunakan!
