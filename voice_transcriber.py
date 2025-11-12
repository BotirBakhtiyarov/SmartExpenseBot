"""
Voice transcription using Vosk for Speech-to-Text.
Supports Uzbek, Russian, and English.
"""

import os
import json
import subprocess
import logging
from vosk import Model, KaldiRecognizer
from config import Config

logger = logging.getLogger(__name__)


class VoiceTranscriber:
    """Voice transcription handler using Vosk."""
    
    def __init__(self):
        self.models = {}
        self._load_models()
    
    def _load_models(self):
        """Load Vosk models for supported languages."""
        language_paths = {
            "uz": Config.VOSK_MODEL_PATH_UZ,
            "ru": Config.VOSK_MODEL_PATH_RU,
            "en": Config.VOSK_MODEL_PATH_EN,
        }
        
        for lang, model_path in language_paths.items():
            if model_path and os.path.exists(model_path):
                try:
                    self.models[lang] = Model(model_path)
                    logger.info(f"Loaded Vosk model for {lang} from {model_path}")
                except Exception as e:
                    logger.error(f"Error loading model for {lang}: {e}")
            else:
                logger.warning(f"Model not found for {lang} at {model_path}")
    
    def transcribe(self, audio_file_path: str, language: str = "en") -> str:
        """
        Transcribe audio file to text.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code (uz, ru, en)
        
        Returns:
            Transcribed text
        """
        if language not in self.models:
            # Fallback to English if model not available
            language = "en" if "en" in self.models else list(self.models.keys())[0] if self.models else None
        
        if not language or language not in self.models:
            return "Voice transcription not available. Please send text message."
        
        try:
            # Convert audio to WAV format using ffmpeg directly
            wav_path = audio_file_path.replace(".ogg", ".wav").replace(".mp3", ".wav")
            
            # Use ffmpeg to convert to 16kHz mono 16-bit WAV (required by Vosk)
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", audio_file_path,
                "-ar", "16000",  # Sample rate: 16kHz
                "-ac", "1",      # Channels: mono
                "-sample_fmt", "s16",  # Sample format: 16-bit signed
                "-y",            # Overwrite output file
                wav_path
            ]
            
            # Run ffmpeg conversion
            result = subprocess.run(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            
            # Transcribe using Vosk
            model = self.models[language]
            rec = KaldiRecognizer(model, 16000)
            rec.SetWords(True)
            
            text_parts = []
            
            with open(wav_path, "rb") as wav_file:
                while True:
                    data = wav_file.read(4000)
                    if len(data) == 0:
                        break
                    
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        if "text" in result:
                            text_parts.append(result["text"])
            
            # Get final result
            final_result = json.loads(rec.FinalResult())
            if "text" in final_result:
                text_parts.append(final_result["text"])
            
            # Clean up temporary file
            if os.path.exists(wav_path) and wav_path != audio_file_path:
                os.remove(wav_path)
            
            return " ".join(text_parts).strip()
        
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return "Could not transcribe audio. Please try again or send text message."

