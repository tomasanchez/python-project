"""
This module contains the Database and SQLAlchemy session configuration.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from allocation.adapters.orm import start_mappers

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine)


def get_session_factory():
    """
    Returns a session factory for the database.
    """
    start_mappers()
    yield SessionLocal
    clear_mappers()
