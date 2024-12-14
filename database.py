from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Создаем подключение к базе данных PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgres:vika1234@localhost:5432/lab9"

# Создаем движок и сессию
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()