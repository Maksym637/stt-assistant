import os

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

from core.db_session import get_db
from core.auth import get_current_account

from schemas.auth import Auth0Payload
from schemas.record import RecordCreate, RecordResponse

from crud.user import get_user_by_id
from crud.record import create_record

from services.storage_service import save_tmp_file, upload_and_cleanup


router = APIRouter()


@router.post(
    "/create",
    response_model=RecordResponse,
    description="Creates a new record by uploading an audio file",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Invalid or missing audio file"},
        401: {"description": "Not authenticated"},
        404: {"description": "User's account not found"},
    },
)
def upload_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    auth0_user: Auth0Payload = Depends(get_current_account),
):
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or missing audio file",
        )

    suffix = os.path.splitext(file.filename)[-1].lower()

    tmp_path = save_tmp_file(file, suffix)
    blob_url = upload_and_cleanup(tmp_path, suffix)
    db_user = get_user_by_id(db, auth0_user.sub)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User's account not found"
        )

    record = create_record(
        db, data=RecordCreate(audio_url=blob_url, user_id=db_user.id)
    )

    return record
