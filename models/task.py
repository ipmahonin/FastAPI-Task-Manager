#код из models/task.py
from db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from schemas.task import TaskStatus


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(TaskStatus),default=TaskStatus.todo)
    created_at = Column(DateTime, server_default=func.now() )
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now() )
    user_id= Column(Integer, ForeignKey('users.id'))
    user = relationship('User',back_populates='tasks')
