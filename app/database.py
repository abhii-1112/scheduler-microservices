
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base
import os



DATABASE_URL = os.getenv("DATABASE_URL")


try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("✅ SQLAlchemy connected successfully")
except Exception as e:
    print("❌ SQLAlchemy failed:", e)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():

    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db

    except SQLAlchemyError as e:

        raise
    finally:
        db.close()
