# 🚀 Panduan Deployment Budayaku Backend ke Railway

## ✅ Persiapan yang Sudah Selesai

1. ✅ Dockerfile sudah diperbaiki untuk Railway
2. ✅ Railway configuration file (railway.toml) sudah dibuat
3. ✅ FastAPI sudah dikonfigurasi dengan CORS

## 📋 Environment Variables yang Diperlukan

Aplikasi ini membutuhkan 3 environment variables:

1. **GOOGLE_API_KEY** - API key untuk Google Generative AI
2. **SUPABASE_URL** - URL instance Supabase Anda
3. **SUPABASE_KEY** - API Key Supabase Anda

## 🛠️ Langkah-Langkah Deployment ke Railway

### 1️⃣ Persiapan Akun Railway

1. Buka [railway.app](https://railway.app)
2. Sign up atau login menggunakan akun GitHub Anda
3. Railway akan meminta akses ke repository GitHub Anda

### 2️⃣ Deploy dari GitHub

1. **Klik "New Project"** di dashboard Railway
2. Pilih **"Deploy from GitHub repo"**
3. Pilih repository **budayaku-backend**
4. Railway akan otomatis mendeteksi Dockerfile

### 3️⃣ Konfigurasi Environment Variables

Setelah project dibuat:

1. Klik pada service yang baru dibuat
2. Buka tab **"Variables"**
3. Tambahkan 3 environment variables:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   SUPABASE_URL=your_supabase_url_here
   SUPABASE_KEY=your_supabase_key_here
   ```
4. Klik **"Add"** untuk setiap variable

### 4️⃣ Deploy

1. Railway akan otomatis melakukan deployment setelah environment variables ditambahkan
2. Tunggu proses build dan deploy selesai (biasanya 2-5 menit)
3. Lihat logs untuk memastikan tidak ada error

### 5️⃣ Dapatkan Public URL

1. Buka tab **"Settings"** di service Anda
2. Scroll ke bagian **"Networking"**
3. Klik **"Generate Domain"**
4. Railway akan memberikan URL publik seperti: `https://your-app.up.railway.app`

### 6️⃣ Update CORS Settings

Setelah mendapatkan URL Railway:

1. Edit file `main.py` di repository
2. Update CORS origins untuk menambahkan URL Railway:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "https://budayaku-psi.vercel.app",
           "https://your-app.up.railway.app"  # Tambahkan URL Railway
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```
3. Commit dan push perubahan
4. Railway akan otomatis re-deploy

## 🧪 Testing API

Setelah deployment berhasil, test API dengan:

```bash
# Health check (jika ada endpoint root)
curl https://your-app.up.railway.app

# Test endpoint Gemini
curl https://your-app.up.railway.app/gemini/...

# Test endpoint Budaya
curl https://your-app.up.railway.app/budaya/...
```

## 📊 Monitoring

1. **Logs**: Lihat real-time logs di tab "Deployments"
2. **Metrics**: Monitor CPU, Memory, Network di tab "Metrics"
3. **Health Checks**: Railway otomatis melakukan health checks

## 💰 Biaya

- Railway menyediakan **$5 free credit per bulan** untuk trial plan
- Setelah itu, biaya berdasarkan usage (CPU, RAM, Network)
- Perkiraan biaya untuk aplikasi kecil: ~$5-10/bulan

## 🔧 Troubleshooting

### Build Gagal
- Periksa logs untuk error detail
- Pastikan semua dependencies ada di `requirements.txt`
- Pastikan Dockerfile syntax benar

### Application Crash
- Periksa environment variables sudah benar
- Lihat application logs untuk error messages
- Pastikan port menggunakan $PORT dari Railway

### CORS Error
- Pastikan URL Railway sudah ditambahkan di CORS origins
- Redeploy setelah update CORS settings

## 📝 Catatan Penting

1. **Auto-Deploy**: Railway akan otomatis deploy setiap kali ada push ke branch yang dipilih
2. **Custom Domain**: Anda bisa tambahkan custom domain di Settings > Networking
3. **Database**: Jika perlu database Railway, bisa tambahkan PostgreSQL/MySQL dari Railway
4. **Backup**: Selalu backup environment variables Anda

## 🔗 Resources

- [Railway Documentation](https://docs.railway.app)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Railway Discord Community](https://discord.gg/railway)

---

**Created**: 2025-11-01
**Last Updated**: 2025-11-01
