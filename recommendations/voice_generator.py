import os
from gtts import gTTS
from django.core.files.base import ContentFile
from django.core.files import File
import tempfile

class VoiceGenerator:
    def __init__(self):
        self.audio_dir = 'audio/'
    
    def text_to_speech_english(self, text: str) -> bytes:
        """Convert English text to speech"""
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                with open(tmp_file.name, 'rb') as audio_file:
                    audio_data = audio_file.read()
                os.unlink(tmp_file.name)
                return audio_data
        except Exception as e:
            print(f"Error generating English TTS: {e}")
            return None
    
    def text_to_speech_hindi(self, text: str) -> bytes:
        """Convert Hindi text to speech"""
        try:
            tts = gTTS(text=text, lang='hi', slow=False)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                with open(tmp_file.name, 'rb') as audio_file:
                    audio_data = audio_file.read()
                os.unlink(tmp_file.name)
                return audio_data
        except Exception as e:
            print(f"Error generating Hindi TTS: {e}")
            return None
    
    def save_audio_file(self, audio_data: bytes, filename: str) -> ContentFile:
        """Save audio data as Django ContentFile"""
        if audio_data:
            return ContentFile(audio_data, name=filename)
        return None