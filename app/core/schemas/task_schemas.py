import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: datetime
    location: str


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: uuid.UUID
    created_at: Optional[datetime]
    last_updated: Optional[datetime]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
