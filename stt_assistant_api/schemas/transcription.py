from datetime import datetime

from pydantic import BaseModel


class TranscriptionPayload(BaseModel):
    record_id: int
    language_code: str


class TranscriptionBase(BaseModel):
    language_code: str
    transcription: str


class TranscriptionCreate(TranscriptionBase):
    record_id: int


class TranscriptionResponse(TranscriptionBase):
    id: int
    created_at: datetime
    record_id: int

    class Config:
        orm_mode = True
