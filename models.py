from pydantic import BaseModel, Field
from typing import Optional

class TtsRequest(BaseModel):
    text: str
    voice: str = "Despina"

# Schema untuk Chat
class ChatTurn(BaseModel):
    user: str
    bot: str

class ChatRequest(BaseModel):
    history: list[ChatTurn]
    province: str
    new_chat: str

class ChatImageRequest(BaseModel):
    prompt: str
    province: str

class ChatImageTextRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded image data")
    province: Optional[str] = Field(
        None, description="Province context for cultural validation"
    )

    class Config:
        schema_extra = {
            "example": {
                "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
                "province": "Jawa",
            }
        }


class RumahAdatModel(BaseModel):
    nama_rumah_adat: str
    deskripsi_rumah_adat: str
    url_rumah_adat: Optional[str] = None


class PakaianAdatModel(BaseModel):
    nama_pakaian_adat: str
    deskripsi_pakaian_adat: str
    url_pakaian_adat: Optional[str] = None


class AlatMusikModel(BaseModel):
    nama_alat_musik: str
    deskripsi_alat_musik: str
    url_alat_musik: Optional[str] = None


class BudayaModel(BaseModel):
    id: int
    nama_provinsi: str
    slug: str
    rumah_adat: RumahAdatModel
    pakaian_adat: PakaianAdatModel
    alat_musik: AlatMusikModel
