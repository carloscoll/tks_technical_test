import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Inspector(Base):
    __tablename__ = "inspectors"
    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, index=True, unique=True)
    name = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    timezone = Column(String(50), index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_update = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    assignments = relationship("TaskAssignment", back_populates="inspector")


class Task(Base):
    __tablename__ = "jobs"
    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, index=True, unique=True)
    title = Column(String(100), index=True)
    description = Column(String(500))
    deadline = Column(DateTime(timezone=True), nullable=True)
    location = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_update = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    assignments = relationship("TaskAssignment", back_populates="task")


class TaskAssignment(Base):
    __tablename__ = "task_assignments"
    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, index=True, unique=True)
    inspector_id = Column(postgresql.UUID(as_uuid=True), ForeignKey("inspectors.id"))
    task_id = Column(postgresql.UUID(as_uuid=True), ForeignKey("jobs.id"), unique=True)
    scheduled_datetime = Column(DateTime(timezone=True))
    status = Column(String(10))
    evaluation_datetime = Column(DateTime(timezone=True))
    rating = Column(Float)
    rating_description = Column(String(500))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_update = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    inspector = relationship("Inspector", back_populates="assignments")
    task = relationship("Task", back_populates="assignments")
