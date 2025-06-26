from fastapi import HTTPException
from fastapi.responses import Response, JSONResponse
from config.config import settings
from models import TtsRequest, ChatRequest, ChatImageRequest
from google import genai
from google.genai import types
from my_utils import get_context, classifier_context
import base64
import wave
import io
from io import BytesIO
from PIL import Image

class GeminiService:
    def __init__(self):
        self.gemini_key = settings.google_api_key
        self.LLM_MODEL_ID = "gemini-2.0-flash"
        self.TTS_MODEL_ID = "gemini-2.5-flash-preview-tts"
        self.LLM_CLASSIFIER_MODEL = "gemini-2.0-flash"
        self.IMAGEN_MODEL = "gemini-2.0-flash-preview-image-generation"
        self.llm_client = genai.Client(api_key=self.gemini_key)
        self.llm_classifier_client = genai.Client(api_key=self.gemini_key)
        self.imagen_client = genai.Client(api_key=self.gemini_key)
        self.tts_client = genai.Client(api_key=self.gemini_key)

    def generate_text(self, request: ChatRequest):
        try:
            konteks = get_context(request.province)
            history = [konteks]
            for line in request.history:
                history.append(f"User: {line.user}")
                history.append(f"Budibot: {line.bot}")
            history.append(f"User: {request.new_chat}")

            prompt = "\n".join(history)

            response = self.llm_client.models.generate_content(
                model=self.LLM_MODEL_ID, contents=prompt
            )

            if not hasattr(response, "text"):
                raise Exception("Model tidak mengembalikan teks.")

            return {"response": response.text.strip()}

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Gagal menghasilkan teks: {str(e)}"
            )

    def generate_audio(self, request: TtsRequest):
        try:
            response = self.tts_client.models.generate_content(
                model=self.TTS_MODEL_ID,
                contents=request.text,
                config={
                    "response_modalities": ["Audio"],
                    "speech_config": {
                        "voice_config": {
                            "prebuilt_voice_config": {"voice_name": request.voice}
                        }
                    },
                },
            )

            print(f"Response candidates: {len(response.candidates)}")
            if response.candidates:
                print(f"Content parts: {len(response.candidates[0].content.parts)}")

            audio_blob = response.candidates[0].content.parts[0].inline_data
            if hasattr(audio_blob, "data"):
                if isinstance(audio_blob.data, str):
                    audio_data = base64.b64decode(audio_blob.data)
                    print(f"Base64 decoded data length: {len(audio_data)} bytes")
                else:
                    audio_data = audio_blob.data
                    print(f"Direct audio data length: {len(audio_data)} bytes")
            else:
                raise Exception("Audio blob tidak memiliki data")

            expected_duration = len(audio_data) / (24000 * 2)
            print(f"Expected duration: {expected_duration:.2f} seconds")

            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(audio_data)

            wav_buffer.seek(0)

            wav_content = wav_buffer.read()

            return Response(content=wav_content, media_type="audio/wav")

        except Exception as e:
            print(f"Terjadi error: {e}")
            import traceback

            traceback.print_exc()
            raise HTTPException(
                status_code=500, detail=f"Gagal menghasilkan audio: {str(e)}"
            )

    def image_generator(self, request: ChatImageRequest):
        classifier_prompt = classifier_context(
            prompt=request.prompt,
            nama_provinsi=request.province
        )

        classifier_resp = self.llm_classifier_client.models.generate_content(
            model=self.LLM_MODEL_ID,
            contents=classifier_prompt
        )
        answer = classifier_resp.text.strip().upper()

        if not answer.startswith("YA"):
            return JSONResponse(
                content={"message": "Maaf, permintaan gambar di luar konteks budaya Indonesia."},
                status_code=200
            )

        resp = self.imagen_client.models.generate_content(
            model=self.IMAGEN_MODEL,
            contents=request.prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"]
            )
        )

        description = ""
        image_b64 = ""

        for part in resp.candidates[0].content.parts:
            if getattr(part, "text", None):
                description += part.text
            elif getattr(part, "inline_data", None):
                image_b64 = base64.b64encode(part.inline_data.data).decode()

        return JSONResponse(
            content={"description": description.strip(), "image_base64": image_b64},
            status_code=200,
        )

gemini_service = GeminiService()
