from datetime import datetime

from pydantic import BaseModel


class RecordBase(BaseModel):
    audio_url: str


class RecordCreate(RecordBase):
    user_id: int


class RecordResponse(RecordBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True
