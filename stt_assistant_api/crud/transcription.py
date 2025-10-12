from sqlalchemy.orm import Session

from models.record import Record
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


def get_transcription_by_record_id(db: Session, record_id: int):
    return db.query(Transcription).filter(Transcription.record_id == record_id).first()


def get_transcriptions_by_user_id(db: Session, user_id: int):
    query = db.query(
        Record.audio_url,
        Transcription.transcription,
        Transcription.created_at,
    ).join(
        target=Transcription,
        onclause=((Record.id == Transcription.record_id) & (Record.user_id == user_id)),
    )

    return query.all()
