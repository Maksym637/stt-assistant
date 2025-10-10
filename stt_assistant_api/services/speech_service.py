import os
import shutil

from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, audio

from storage_service import download_from_blob

from config import az_settings


speech_config = SpeechConfig(
    subscription=az_settings.SPEECH_KEY, region=az_settings.SPEECH_REGION
)


def transcribe_and_cleanup(blob_name: str, language: str) -> str:
    try:

        tmp_path = download_from_blob(blob_name)

        speech_config.speech_recognition_language = language
        audio_config = audio.AudioConfig(filename=tmp_path)

        speech_recognizer = SpeechRecognizer(
            speech_config=speech_config, audio_config=audio_config
        )
        recognized_text = speech_recognizer.recognize_once()

        return recognized_text.text

    finally:
        shutil.rmtree(os.path.dirname(tmp_path), ignore_errors=True)
