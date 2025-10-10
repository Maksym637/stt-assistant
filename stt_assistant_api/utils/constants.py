from typing import List

from enum import Enum


class SupportedLanguage(str, Enum):
    EN = "en-US"
    DE = "de-DE"
    ES = "es-ES"
    FR = "fr-FR"
    PT = "pt-PT"

    @classmethod
    def list(cls) -> List[str]:
        return [lang.value for lang in cls]
