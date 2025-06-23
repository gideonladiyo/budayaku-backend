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