from fastapi import FastAPI

from core.db_session import Base, engine

from models.user import User
from models.record import Record
from models.transcription import Transcription


app = FastAPI(
    title="stt-assistant-api",
    description="The STT-Assistant API that transcribes audio into editable text",
)


@app.on_event("startup")
def on_startup():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created!")


@app.on_event("shutdown")
def on_shutdown():
    print("Dropping tables...")
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped!")


@app.get("/transcriber")
def perform_transcription():
    return {"message": "Hello STT-Assistant API!"}
