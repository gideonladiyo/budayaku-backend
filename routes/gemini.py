from fastapi import APIRouter
from models import ChatRequest, TtsRequest
from services.gemini_service import gemini_service

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/generate-text")
async def generate_text(request: ChatRequest):
    return gemini_service.generate_text(request=request)

@router.post("/generate-audio")
async def generate_audio(request: TtsRequest):
    return gemini_service.generate_audio(request=request)