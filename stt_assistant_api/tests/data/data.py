import datetime

from schemas.user import UserResponse
from schemas.record import RecordResponse
from schemas.transcription import (
    TranscriptionResponse,
    TranscriptionItem,
    TranscriptionAllResponse,
)


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
TEST_TRANSCRIPTION_ALL = TranscriptionAllResponse(
    data=[
        TranscriptionItem(
            audio_url="https://blob.example.com/first-phrase-en.mp3?sas_token",
            transcription="Transcription text 1",
            created_at=datetime.datetime.now(datetime.timezone.utc),
        ),
        TranscriptionItem(
            audio_url="https://blob.example.com/second-phrase-en.mp3?sas_token",
            transcription="Transcription text 2",
            created_at=datetime.datetime.now(datetime.timezone.utc),
        ),
        TranscriptionItem(
            audio_url="https://blob.example.com/third-phrase-en.mp3?sas_token",
            transcription="Transcription text 3",
            created_at=datetime.datetime.now(datetime.timezone.utc),
        ),
    ]
)
