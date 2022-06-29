from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://mysql:mysql123@127.0.0.1:3306/test?charset=utf8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

MODEL = declarative_base()