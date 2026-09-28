from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base


DATABASE_URL = "sqlite:///./womens_sports.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def init_db():
    """
    Create all database tables if they do not already exist.
    """
    Base.metadata.create_all(bind=engine)


def get_session():
    """
    Return a new SQLAlchemy database session.
    """
    return SessionLocal()