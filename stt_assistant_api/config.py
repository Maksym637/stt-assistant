import os

from dotenv import load_dotenv


BASE_ENV_PATH = os.path.join(os.path.dirname(__file__), "../env")

load_dotenv(os.path.join(BASE_ENV_PATH, ".db.env"))
load_dotenv(os.path.join(BASE_ENV_PATH, ".azure.env"))
load_dotenv(os.path.join(BASE_ENV_PATH, ".api.env"))


class DBSettings:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DB_NAME = os.getenv("DB_NAME")


class AZSettings:
    pass


class APISettings:
    pass


db_settings = DBSettings()
az_settings = AZSettings()
api_settings = APISettings()
