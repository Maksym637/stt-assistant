import os
import shutil
from pydub import AudioSegment

from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, audio

from services.storage_service import download_from_blob

from utils.constants import AudioFormats

from config import az_settings


speech_config = SpeechConfig(
    subscription=az_settings.SPEECH_KEY, region=az_settings.SPEECH_REGION
)


def convert_mp3_to_wav(mp3_path: str) -> str:
    wav_path = os.path.splitext(mp3_path)[0] + f".{AudioFormats.WAV.value}"

    sound: AudioSegment = AudioSegment.from_file(
        mp3_path, format=AudioFormats.MP3.value
    )
    sound.export(wav_path, format=AudioFormats.WAV.value)

    return wav_path


def transcribe_audio(blob_name: str, language_code: str) -> str:
    tmp_path, wav_path = None, None

    try:

        tmp_path = download_from_blob(blob_name)
        wav_path = convert_mp3_to_wav(tmp_path)

        speech_config.speech_recognition_language = language_code
        audio_config = audio.AudioConfig(filename=wav_path)

        speech_recognizer = SpeechRecognizer(
            speech_config=speech_config, audio_config=audio_config
        )
        recognized_text = speech_recognizer.recognize_once()

        return recognized_text.text

    finally:
        for path in [tmp_path, wav_path]:
            if path and os.path.exists(os.path.dirname(path)):
                shutil.rmtree(os.path.dirname(path), ignore_errors=True)
