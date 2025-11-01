from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from routes import gemini
from routes import budaya

# Inisialisasi FastAPI
app = FastAPI()

# Tambahkan TrustedHostMiddleware untuk menangani proxy dari Railway
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Izinkan semua host untuk Railway
)

# Konfigurasi CORS - harus ditambahkan setelah TrustedHostMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(gemini.router)
app.include_router(budaya.router)
