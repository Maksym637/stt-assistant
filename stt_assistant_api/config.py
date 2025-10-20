import os

from dotenv import load_dotenv


BASE_ENV_PATH = os.path.join(os.path.dirname(__file__), "../env")

load_dotenv(os.path.join(BASE_ENV_PATH, ".azure.env"))
load_dotenv(os.path.join(BASE_ENV_PATH, ".api.env"))


class AZSettings:
    SPEECH_KEY = os.getenv("SPEECH_KEY")
    SPEECH_REGION = os.getenv("SPEECH_REGION")

    STORAGE_CONNECTION_STRING = os.getenv("STORAGE_CONNECTION_STRING")
    STORAGE_ACCOUNT_NAME = os.getenv("STORAGE_ACCOUNT_NAME")
    STORAGE_ACCOUNT_KEY = os.getenv("STORAGE_ACCOUNT_KEY")
    STORAGE_BLOB_CONTAINER = os.getenv("STORAGE_BLOB_CONTAINER")

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")


class APISettings:
    ENV = os.getenv("ENV")

    ORIGINS = os.getenv("ORIGINS")

    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")


az_settings = AZSettings()
api_settings = APISettings()
