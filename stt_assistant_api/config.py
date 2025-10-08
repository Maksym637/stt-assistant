import os

from dotenv import load_dotenv


BASE_ENV_PATH = os.path.join(os.path.dirname(__file__), "../env")

load_dotenv(os.path.join(BASE_ENV_PATH, ".azure.env"))
load_dotenv(os.path.join(BASE_ENV_PATH, ".api.env"))


class AZSettings:
    # Configurations for Azure Speech Studio
    # TODO

    # Configurations for Azure Blob Storage
    # TODO

    # Configurations for Azure Database for PostgreSQL
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")


class APISettings:
    ENV = os.getenv("ENV")

    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")


az_settings = AZSettings()
api_settings = APISettings()
