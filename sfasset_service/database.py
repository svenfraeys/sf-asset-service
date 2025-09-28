import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql",
    username=os.getenv("DB_USERNAME", "postgres"),
    password=os.getenv("DB_USERNAME", "root"),
    host=os.getenv("DB_USERNAME", "localhost"),
    database=os.getenv("DB_USERNAME", "sfpd"),
    port=int(os.getenv("DB_PORT", "5432")),
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
