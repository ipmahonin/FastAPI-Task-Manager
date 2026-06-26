#код из models/user.py
from sqlalchemy import Column, Integer,String, DateTime
from db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now() )
    tasks = relationship('Task', back_populates='user')