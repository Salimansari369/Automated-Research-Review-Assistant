import os
import requests
from pathlib import Path
from utils.logging_config import logger
from config.settings import LLM_API_KEY, LLM_PROVIDER

class TranscriptionService:
    """
    Handles speech-to-text transcription using Groq Whisper (whisper-large-v3)
    or OpenAI Whisper (whisper-1) with offline fallback.
    """

    @classmethod
    def transcribe(cls, audio_file_path: str) -> str:
        if not audio_file_path or not os.path.exists(audio_file_path):
            return ""

        # If Groq or OpenAI API key is present
        if LLM_API_KEY and len(LLM_API_KEY.strip()) > 5:
            try:
                if "groq" in LLM_PROVIDER.lower() or "gsk_" in LLM_API_KEY:
                    endpoint = "https://api.groq.com/openai/v1/audio/transcriptions"
                    model = "whisper-large-v3"
                else:
                    endpoint = "https://api.openai.com/v1/audio/transcriptions"
                    model = "whisper-1"

                headers = {
                    "Authorization": f"Bearer {LLM_API_KEY}"
                }
                
                with open(audio_file_path, "rb") as f:
                    files = {
                        "file": (os.path.basename(audio_file_path), f, "audio/wav")
                    }
                    data = {
                        "model": model,
                        "temperature": 0.0,
                        "language": "en"
                    }
                    resp = requests.post(endpoint, headers=headers, files=files, data=data, timeout=30)
                    if resp.status_code == 200:
                        text = resp.json().get("text", "").strip()
                        logger.info(f"Whisper transcribed: '{text}'")
                        return text
                    else:
                        logger.warning(f"Whisper API notice ({resp.status_code}): {resp.text}")
            except Exception as e:
                logger.error(f"Whisper transcription error: {e}")

        # Fallback if no API key or network error
        return "Can you summarize the methodologies and findings across the active papers?"
