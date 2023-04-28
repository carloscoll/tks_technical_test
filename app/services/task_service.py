import uuid
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models import models
from app.core.schemas import task_schemas as schemas


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task: schemas.TaskCreate) -> models.Task:
        try:
            db_task = models.Task(**task.dict())
            db_task.id = uuid.uuid4()
            self.db.add(db_task)
            self.db.commit()
            self.db.refresh(db_task)
            return db_task
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def get_task(self, task_id: UUID) -> models.Task:
        try:
            task = self.db.query(models.Task).filter(models.Task.id == task_id).first()
            return task
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def get_tasks(self) -> List[models.Task]:
        try:
            return self.db.query(models.Task).all()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def get_available_tasks(self) -> List[models.Task]:
        try:
            return self.db.query(models.Task).join(models.TaskAssignment)\
                .filter(models.Task.id != models.TaskAssignment.task_id).all()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def update_task(self, task_id: UUID, task: schemas.TaskUpdate) -> models.Task:
        try:
            db_task = self.get_task(task_id)
            update_data = task.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_task, key, value)
            self.db.commit()
            self.db.refresh(db_task)
            return db_task
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def delete_task(self, task_id: UUID):
        try:
            db_task = self.get_task(task_id)
            self.db.delete(db_task)
            self.db.commit()
            return
        except Exception as e:
            self.db.rollback()
            raise e
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()
