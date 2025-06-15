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

# Load API key dari .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise Exception("GOOGLE_API_KEY not found in .env file")

# Client terpisah
llm_client = genai.Client(api_key=api_key)
tts_client = genai.Client(api_key=api_key)

# Model ID - PERBAIKAN: hapus "models/" prefix
LLM_MODEL_ID = "models/gemini-2.0-flash"
TTS_MODEL_ID = "gemini-2.5-flash-preview-tts"  # Sama seperti di notebook

# Inisialisasi FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Schema untuk TTS
class TtsRequest(BaseModel):
    text: str
    voice: str = "Sadaltager"


# Schema untuk Chat
class ChatTurn(BaseModel):
    user: str
    bot: str


class ChatRequest(BaseModel):
    history: list[ChatTurn]
    province: str
    new_chat: str


@app.post("/generate-text")
async def generate_text(request: ChatRequest):
    try:
        konteks = get_context(request.province)
        history = [konteks]
        for line in request.history:  # Hanya 10 percakapan terakhir
            history.append(f"User: {line.user}")
            history.append(f"Budibot: {line.bot}")
        history.append(f"User: {request.new_chat}")

        prompt = "\n".join(history)

        response = llm_client.models.generate_content(
            model=LLM_MODEL_ID, contents=prompt
        )

        if not hasattr(response, "text"):
            raise Exception("Model tidak mengembalikan teks.")

        return {"response": response.text.strip()}

    except Exception as e:
        print(f"Terjadi error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Gagal menghasilkan teks: {str(e)}"
        )


@app.post("/generate-audio")
async def generate_audio(request: TtsRequest):
    try:
        print(f"Input text: '{request.text}'")
        print(f"Text length: {len(request.text)}")

        # PERBAIKAN: Konfigurasi sama persis dengan notebook
        response = tts_client.models.generate_content(
            model=TTS_MODEL_ID,
            contents=request.text,
            config={
                "response_modalities": ["Audio"],  # Gunakan 'Audio' bukan "AUDIO"
                "speech_config": {
                    "voice_config": {
                        "prebuilt_voice_config": {"voice_name": request.voice}
                    }
                },
            },
        )

        # Debug response structure
        print(f"Response candidates: {len(response.candidates)}")
        if response.candidates:
            print(f"Content parts: {len(response.candidates[0].content.parts)}")

        audio_blob = response.candidates[0].content.parts[0].inline_data
        print(f"Audio blob mime type: {audio_blob.mime_type}")

        # PERBAIKAN: Akses data langsung seperti di notebook
        # Cek apakah data sudah dalam format bytes atau masih base64
        if hasattr(audio_blob, "data"):
            if isinstance(audio_blob.data, str):
                # Jika masih string base64, decode dulu
                audio_data = base64.b64decode(audio_blob.data)
                print(f"Base64 decoded data length: {len(audio_data)} bytes")
            else:
                # Jika sudah bytes, gunakan langsung
                audio_data = audio_blob.data
                print(f"Direct audio data length: {len(audio_data)} bytes")
        else:
            raise Exception("Audio blob tidak memiliki data")

        # Hitung durasi yang diharapkan
        expected_duration = len(audio_data) / (24000 * 2)  # 24kHz, 16-bit
        print(f"Expected duration: {expected_duration:.2f} seconds")

        # Bungkus jadi WAV dengan parameter yang sama seperti notebook
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, "wb") as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit (2 bytes)
            wf.setframerate(24000)  # 24kHz sample rate
            wf.writeframes(audio_data)  # Gunakan audio_data bukan pcm_data

        wav_buffer.seek(0)

        # Debug: save file untuk testing
        with open("debug_output.wav", "wb") as f:
            f.write(wav_buffer.getvalue())
        print(
            f"Saved debug_output.wav with size: {wav_buffer.getbuffer().nbytes} bytes"
        )

        wav_content = wav_buffer.read()
        print(f"WAV content size: {len(wav_content)} bytes")

        return Response(content=wav_content, media_type="audio/wav")

    except Exception as e:
        print(f"Terjadi error: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Gagal menghasilkan audio: {str(e)}"
        )
