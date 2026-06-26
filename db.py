#код из db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

engine = create_engine("postgresql://user:password@localhost:5432/tasks")
SessionLocal = sessionmaker(bind=engine)