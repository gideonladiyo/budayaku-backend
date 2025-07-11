from fastapi import APIRouter
from models import ChatRequest, TtsRequest, ChatImageRequest, ChatImageTextRequest
from services.gemini_service import gemini_service

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/generate-text")
async def generate_text(request: ChatRequest):
    return gemini_service.generate_text(request=request)

@router.post("/generate-audio")
async def generate_audio(request: TtsRequest):
    return gemini_service.generate_audio(request=request)

@router.post("/generate-image")
async def generate_image(request: ChatImageRequest):
    return gemini_service.image_generator(request)

@router.post("/generate-image-from-text-and-image")
async def generate_image_from_text_and_image(request: ChatImageTextRequest):
    """
    Generate image based on input image and text prompt.
    The input image serves as a reference or base for the generation.
    """
    return gemini_service.image_text_generator(request)