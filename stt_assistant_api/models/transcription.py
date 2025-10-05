import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.db_session import Base


class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True, index=True)
    transcription = Column(Text, nullable=False)
    language_code = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.timezone.utc)
    record_id = Column(Integer, ForeignKey("records.id"), nullable=False)

    record = relationship("Record", back_populates="transcription")
