from typing import List

from enum import Enum


class SupportedLanguageCode(str, Enum):
    EN = "en-US"
    DE = "de-DE"
    ES = "es-ES"
    FR = "fr-FR"
    PT = "pt-PT"

    @classmethod
    def list(cls) -> List[str]:
        return [lang_code.value for lang_code in cls]


class AudioFormats(Enum):
    MP3 = "mp3"
    WAV = "wav"
