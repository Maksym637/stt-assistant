from datetime import datetime

from pydantic import BaseModel


class TranscriptionBase(BaseModel):
    language_code: str


class TranscriptionCreate(TranscriptionBase):
    record_id: str


class TranscriptionResponse(TranscriptionBase):
    id: int
    transcription: str
    create_at: datetime
    record_id: int

    class Config:
        orm_mode = True
