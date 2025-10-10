from fastapi import FastAPI

from core.db_session import Base, engine

from api.router import api_router

from config import api_settings


app = FastAPI(
    title=f"stt-assistant-api-{api_settings.ENV}",
    description="The STT-Assistant API that transcribes audio into editable text",
)

app.include_router(api_router)


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
