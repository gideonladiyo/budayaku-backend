from fastapi import APIRouter
from services.province_service import province_service

router = APIRouter(prefix="/budaya", tags=["Budaya"])

@router.get("/")
async def get_all():
    return province_service.get_all()

@router.get("/{slug}")
async def get_by_slug(slug: str):
    return province_service.get_by_slug(slug)