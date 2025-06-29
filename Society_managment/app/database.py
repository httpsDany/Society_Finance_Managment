# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from fastapi import Depends

# Directly paste the full URL here
DATABASE_URL = "postgresql://society_management_sipu_user:JmEjQhJ9Fa0ZsiQ5P3m5mH6XYFxMLBAS@dpg-d1ge92umcj7s73clsn3g-a.oregon-postgres.render.com/society_management_sipu"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
