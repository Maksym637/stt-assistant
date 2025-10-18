import datetime

from urllib.parse import urlparse

from schemas.user import UserResponse
from schemas.record import RecordResponse
from schemas.transcription import TranscriptionResponse


def to_iso_8601(dt: datetime.datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def tst_get_blob_name_from_url(url: str) -> str:
    return urlparse(url).path.split("/")[-1]


def tst_generate_sas_url(blob_name: str) -> str:
    return f"https://blob.example.com/{blob_name}?sas_token"


TEST_HEADERS = {"Authorization": "Bearer test_token"}

TEST_PAYLOAD = {"sub": "auth0|01234", "email": "tcase1@gmail.com"}

TEST_USER = UserResponse(
    id=1,
    auth0_id=TEST_PAYLOAD["sub"],
    email=TEST_PAYLOAD["email"],
)

TEST_RECORD = RecordResponse(
    id=1,
    audio_url="https://blob.example.com/first-phrase-en.mp3?sas_token",
    created_at=datetime.datetime.now(datetime.timezone.utc),
    user_id=1,
)

TEST_TRANSCRIPTION = TranscriptionResponse(
    id=1,
    language_code="en-US",
    transcription="Transcription text 1",
    created_at=datetime.datetime.now(datetime.timezone.utc),
    record_id=1,
)
TEST_TRANSCRIPTION_ALL_DB = [
    (
        "https://blob.example.com/first-phrase-en.mp3?sas_token",
        "Transcription text 1",
        datetime.datetime.now(datetime.timezone.utc),
    ),
    (
        "https://blob.example.com/second-phrase-en.mp3?sas_token",
        "Transcription text 2",
        datetime.datetime.now(datetime.timezone.utc),
    ),
    (
        "https://blob.example.com/third-phrase-en.mp3?sas_token",
        "Transcription text 3",
        datetime.datetime.now(datetime.timezone.utc),
    ),
]
