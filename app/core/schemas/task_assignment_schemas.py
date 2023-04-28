from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Status(str, Enum):
    pending = 'pending'
    in_progress = 'in progress'
    completed = 'completed'


class TaskAssignmentBase(BaseModel):
    scheduled_datetime: datetime
    status: Status = 'pending'


class TaskAssignmentCreate(TaskAssignmentBase):
    pass


class TaskAssignmentUpdate(TaskAssignmentBase):
    pass


class TaskAssignmentEvaluation(BaseModel):
    rating: float = None
    rating_description: Optional[str] = None
    evaluation_datetime: datetime = None


class TaskAssignment(TaskAssignmentBase, TaskAssignmentEvaluation):
    id: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    inspector_id: UUID
    task_id: UUID

    class Config:
        orm_mode = True


class TaskAssignmentEvaluationOut(TaskAssignmentEvaluation):
    id: UUID
    scheduled_datetime: datetime
    status: Status = 'pending'
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    inspector_id: UUID
    task_id: UUID

    class Config:
        orm_mode = True
