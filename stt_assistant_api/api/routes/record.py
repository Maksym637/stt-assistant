import os

from typing import Optional

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

from core.db_session import get_db
from core.auth import get_current_account

from schemas.auth import Auth0Payload
from schemas.record import RecordCreate, RecordResponse

from crud.user import get_user_by_id
from crud.record import create_record

from services.storage_service import (
    get_blob_name_from_url,
    generate_sas_url,
    upload_to_blob,
)


router = APIRouter()


@router.post(
    "/create",
    response_model=RecordResponse,
    description="Creates a new record by uploading an audio file",
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "description": (
                "**Bad Request:**\n\n"
                "- Invalid or missing audio file  \n"
                "- Provided audio file already exists"
            )
        },
        401: {"description": "Not authenticated"},
        404: {"description": "User's account not found"},
    },
)
def upload_audio(
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    auth0_user: Auth0Payload = Depends(get_current_account),
):
    db_user = get_user_by_id(db, auth0_user.sub)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User's account not found"
        )

    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or missing audio file",
        )

    suffix = os.path.splitext(file.filename)[-1].lower()
    blob_url = upload_to_blob(file, suffix)

    if not blob_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provided audio file already exists",
        )

    db_record = create_record(
        db, data=RecordCreate(audio_url=blob_url, user_id=db_user.id)
    )
    record = RecordResponse(
        audio_url=generate_sas_url(
            blob_name=get_blob_name_from_url(db_record.audio_url)
        ),
        id=db_record.id,
        created_at=db_record.created_at,
        user_id=db_record.user_id,
    )

    return record
