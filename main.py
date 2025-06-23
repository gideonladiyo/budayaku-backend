import os
import io
import base64
import wave
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from my_utils import get_context
from google import genai
from google.genai import types
from routes import gemini
from routes import budaya


# Inisialisasi FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(gemini.router)
app.include_router(budaya.router)