from fastapi import APIRouter
from models import IslandCulture
from services.firebase_service import firebase_serivce

router = APIRouter(prefix="/budaya", tags=["Budaya"])

@router.get("/")
async def get_all():
    return firebase_serivce.get_all_culture()

@router.get("/{id}")
async def get_by_id(id: str):
    return firebase_serivce.get_culture_by_id(id)