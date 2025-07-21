from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import gemini
from routes import budaya

# Inisialisasi FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://budayaku-psi.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(gemini.router)
app.include_router(budaya.router)
