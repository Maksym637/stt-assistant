from sqlalchemy.orm import Session

from models.record import Record

from schemas.record import RecordCreate


def create_record(db: Session, data: RecordCreate):
    record = Record(audio_url=data.audio_url, user_id=data.user_id)

    db.add(record)
    db.commit()
    db.refresh(record)

    return record
