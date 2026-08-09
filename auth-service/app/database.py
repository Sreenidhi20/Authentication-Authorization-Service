import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

load_dotenv()

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL")
SERVER_NAME = os.getenv("SERVER_NAME")
DATABASE_NAME = os.getenv("DATABASE_NAME")

def _build_engine():
    if DATABASE_URL:
        return create_engine(DATABASE_URL)

    if SERVER_NAME and DATABASE_NAME:
        connection_string = (
            f"mssql+pyodbc://{SERVER_NAME}/{DATABASE_NAME}"
            "?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
        )
        return create_engine(connection_string)

    raise RuntimeError(
        "No database configuration found. Set DATABASE_URL or SERVER_NAME + DATABASE_NAME in .env"
    )

engine = _build_engine()

SessionLocal = sessionmaker(
    bind=engine, 
    autoflush=False, 
    autocommit=False
)

def init_db() -> None:
    """Creates database tables if they do not exist."""
    Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    """FastAPI Dependency providing a transactional database session context."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
