from fastapi import APIRouter

from api.routes import user, record, transcription


api_router = APIRouter()

api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(record.router, prefix="/record", tags=["Record"])
api_router.include_router(
    transcription.router, prefix="/transcription", tags=["Transcription"]
)
