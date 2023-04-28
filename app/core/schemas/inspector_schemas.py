import uuid
from enum import Enum

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Timezone(str, Enum):
    madrid = 'Madrid'
    mexico_city = 'Mexico city'
    uk = 'UK'


class InspectorBase(BaseModel):
    name: str
    email: Optional[str] = None
    timezone: Timezone


class InspectorCreate(InspectorBase):
    pass


class InspectorUpdate(InspectorBase):
    pass


class Inspector(InspectorBase):
    id: uuid.UUID
    created_at: Optional[datetime]
    last_updated: Optional[datetime]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
