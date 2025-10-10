from sqlalchemy.orm import Session

from models.transcription import Transcription

from schemas.transcription import TranscriptionCreate


def create_transcription(db: Session, data: TranscriptionCreate):
    transcription = Transcription(
        transcription=data.transcription,
        language_code=data.language_code,
        record_id=data.record_id,
    )

    db.add(transcription)
    db.commit()
    db.refresh(transcription)

    return transcription
