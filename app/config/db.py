from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData

from app.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL, connect_args=settings.DATABASE_CONNECT_DICT
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata = MetaData()