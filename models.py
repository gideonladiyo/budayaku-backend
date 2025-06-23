from pydantic import BaseModel

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

class CultureType(BaseModel):
    nama: str
    deskripsi: str

class Culture(BaseModel):
    nama_pulau: str
    pakaian_adat: CultureType
    rumah_adat: CultureType
    alat_musik: CultureType

class IslandCulture(BaseModel):
    id: str
    data: Culture