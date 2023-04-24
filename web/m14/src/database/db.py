
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from src.conf.config import settings


SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    """
The get_db function is a context manager that returns the database session.
It also handles any exceptions that may occur during the session, and closes
the connection when it's done.
:return: A database session that can be used to query the database
:doc-author: Trelent
"""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()