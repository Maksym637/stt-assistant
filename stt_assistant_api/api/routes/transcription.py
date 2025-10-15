from typing import Annotated

from sqlalchemy.orm import Session

from fastapi import Body, APIRouter, Depends, HTTPException, status

from core.db_session import get_db
from core.auth import get_current_account

from schemas.auth import Auth0Payload
from schemas.transcription import (
    TranscriptionCreate,
    TranscriptionResponse,
    TranscriptionPayload,
    TranscriptionItem,
    TranscriptionAllResponse,
)

from crud.user import get_user_by_id
from crud.record import get_record_by_id
from crud.transcription import (
    create_transcription,
    get_transcription_by_record_id,
    get_transcriptions_by_user_id,
)

from services.storage_service import get_blob_name_from_url, generate_sas_url
from services.speech_service import transcribe_audio

from utils.constants import SupportedLanguageCode


router = APIRouter()


@router.post(
    "/create",
    response_model=TranscriptionResponse,
    description="Creates a new transcription by processing an audio file",
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "description": (
                "**Bad Request:**\n\n"
                "- Provided language code is not supported  \n"
                "- Transcription with the provided record already exists"
            ),
        },
        401: {"description": "Not authenticated"},
        404: {
            "description": (
                "**Not Found:**\n\n"
                "- Record not found  \n"
                "- User's account not found"
            ),
        },
    },
)
def process_record(
    payload: Annotated[TranscriptionPayload, Body(...)],
    db: Session = Depends(get_db),
    auth0_user: Auth0Payload = Depends(get_current_account),
):
    record_id, language_code = payload.record_id, payload.language_code

    if not get_user_by_id(db, auth0_user.sub):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User's account not found"
        )

    if language_code not in SupportedLanguageCode.list():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provided language code is not supported",
        )

    db_record = get_record_by_id(db, record_id)
    if not db_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )

    if get_transcription_by_record_id(db, db_record.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transcription with the provided record already exists",
        )

    transcribed_text = transcribe_audio(
        blob_name=get_blob_name_from_url(db_record.audio_url),
        language_code=language_code,
    )

    transcription = create_transcription(
        db,
        data=TranscriptionCreate(
            record_id=record_id,
            language_code=language_code,
            transcription=transcribed_text,
        ),
    )

    return transcription


@router.get(
    "/all",
    response_model=TranscriptionAllResponse,
    description="Returns all transcriptions with the associated records",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Not authenticated"},
        404: {"description": "User's account not found"},
    },
)
def get_all_transcriptions(
    db: Session = Depends(get_db),
    auth0_user: Auth0Payload = Depends(get_current_account),
):
    db_user = get_user_by_id(db, auth0_user.sub)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User's account not found"
        )

    db_transcriptions = get_transcriptions_by_user_id(db, db_user.id)
    transcriptions = TranscriptionAllResponse(
        data=[
            TranscriptionItem(
                audio_url=generate_sas_url(blob_name=get_blob_name_from_url(audio_url)),
                transcription=transcription,
                created_at=created_at,
            )
            for audio_url, transcription, created_at in db_transcriptions
        ]
    )

    return transcriptions
