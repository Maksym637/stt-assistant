from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status

from core.db_session import get_db
from core.auth import get_current_account

from schemas.auth import Auth0Payload
from schemas.transcription import TranscriptionCreate, TranscriptionResponse

from crud.user import get_user_by_id
from crud.record import get_record_by_id
from crud.transcription import create_transcription

from services.speech_service import transcribe_and_cleanup

from utils.constants import SupportedLanguage


router = APIRouter()


@router.post(
    "/create",
    response_model=TranscriptionResponse,
    description="Creates a new transcription by processing an audio file",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Provided language is not supported"},
        401: {"description": "Not authenticated"},
        404: {"description": "Record|User's account not found"},
    },
)
def process_record(
    record_id: int,
    language: str = SupportedLanguage.EN,
    db: Session = Depends(get_db),
    auth0_user: Auth0Payload = Depends(get_current_account),
):
    # TODO
    # Update verification for adding the same record
    if language not in SupportedLanguage.list():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provided language is not supported",
        )

    db_record = get_record_by_id(db, record_id)
    if not db_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )

    db_user = get_user_by_id(db, auth0_user.sub)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User's account not found"
        )

    transcribed_text = transcribe_and_cleanup(
        blob_name=db_record.audio_url, language=language
    )
    transcription = create_transcription(
        db, data=TranscriptionCreate(language, transcribed_text, record_id)
    )

    return transcription
