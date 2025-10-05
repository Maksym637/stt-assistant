from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

from config import db_settings


Base: DeclarativeMeta = declarative_base()

engine = create_engine(
    url=(
        f"postgresql+psycopg2://{db_settings.DB_USER}:"
        f"{db_settings.DB_PASSWORD}@{db_settings.DB_HOST}:"
        f"{db_settings.DB_PORT}/{db_settings.DB_NAME}"
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
