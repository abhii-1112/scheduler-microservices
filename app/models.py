# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, JSON, func, Text
from .database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    # keep consistent name: schedule_expression (cron string)
    schedule = Column(String, nullable=False)
    # optional custom attributes (payload)
    payload = Column(JSON, nullable=True)
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)
    status = Column(String, default="scheduled")  # scheduled, running, success, failed
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
