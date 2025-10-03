import os
from dotenv import load_dotenv
from fastapi import FastAPI


load_dotenv()


app = FastAPI(
    title=f"stt-assistant-api-{os.getenv('ENV')}",
    description="The STT-Assistant API that transcribes audio into editable text",
)


@app.get("/transcriber")
def perform_transcription():
    return {"message": "Hello STT-Assistant API!"}
