from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import gemini
from routes import budaya

app = FastAPI()

# ✅ Daftar asal (frontend) yang boleh akses
origins = ["http://localhost:3000", "https://budayaku-psi.vercel.app"]

# ✅ Tambahkan CORS middleware paling awal
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Baru include router
app.include_router(gemini.router)
app.include_router(budaya.router)
