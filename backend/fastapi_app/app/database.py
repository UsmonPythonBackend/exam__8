from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL

ENGINE = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker()
