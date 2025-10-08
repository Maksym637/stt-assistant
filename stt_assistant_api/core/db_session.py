from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

from config import az_settings


Base: DeclarativeMeta = declarative_base()

engine = create_engine(
    url=(
        f"postgresql+psycopg2://{az_settings.DB_USER}:"
        f"{az_settings.DB_PASSWORD}@{az_settings.DB_HOST}:"
        f"{az_settings.DB_PORT}/{az_settings.DB_NAME}"
        "?sslmode=require"
    ),
    echo=True,
)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:

        yield db

    finally:
        db.close()
