from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config.settings import DBSettings

DATABASE_URL = DBSettings.get_database_url()
if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be configured in settings")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
