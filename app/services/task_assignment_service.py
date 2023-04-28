import uuid
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models import models
from app.core.schemas import task_assignment_schemas as schemas


class TaskAssignmentService:
    def __init__(self, db: Session):
        self.db = db

    def assign_task(self, inspector_id: UUID, task_id: UUID, task_assignment: schemas.TaskAssignmentCreate) \
            -> models.Task:
        try:
            inspector = self.db.query(models.Inspector).filter(models.Inspector.id == inspector_id).first()
            if not inspector:
                raise ValueError("Inspector not found.")
            task = self.db.query(models.Task).filter(models.Task.id == task_id).first()
            if not task:
                raise ValueError("Task not found.")
            if task_assignment.scheduled_datetime > task.deadline:
                raise ValueError("Scheduled datetime is after deadline.")

            db_task_assignment = models.TaskAssignment(**task_assignment.dict())
            db_task_assignment.id = uuid.uuid4()
            db_task_assignment.inspector_id = inspector.id
            db_task_assignment.task_id = task.id

            self.db.add(db_task_assignment)
            self.db.commit()
            self.db.refresh(db_task_assignment)
            return db_task_assignment
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def finish_task(self, task_assignment_id: UUID, task_assignment: schemas.TaskAssignmentEvaluation) \
            -> models.Task:
        try:
            db_task_assignment = self.get_assigned_task(task_assignment_id)
            if not db_task_assignment:
                raise ValueError("Assignation not found.")
            if task_assignment.evaluation_datetime > db_task_assignment.scheduled_datetime:
                raise ValueError("Evaluation date is after schedule datetime.")

            db_task_assignment.evaluation_datetime = task_assignment.evaluation_datetime
            db_task_assignment.rating = task_assignment.rating
            db_task_assignment.rating_description = task_assignment.rating_description
            db_task_assignment.status = "completed"

            self.db.add(db_task_assignment)
            self.db.commit()
            self.db.refresh(db_task_assignment)
            return db_task_assignment
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def get_assigned_task(self, task_assignment_id: UUID) -> models.TaskAssignment:
        try:
            task_assignment = self.db.query(models.TaskAssignment). \
                filter(models.TaskAssignment.id == task_assignment_id).first()
            return task_assignment
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def get_assigned_tasks(self) -> List[models.TaskAssignment]:
        try:
            return self.db.query(models.TaskAssignment).all()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def get_from_inspector(self, inspector_id: UUID) -> List[models.TaskAssignment]:
        try:
            return self.db.query(models.TaskAssignment).filter(models.TaskAssignment.inspector_id == inspector_id).all()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def get_unfinished_from_inspector(self, inspector_id: UUID) -> List[models.TaskAssignment]:
        try:
            return self.db.query(models.TaskAssignment).filter(models.TaskAssignment.inspector_id == inspector_id) \
                .filter(models.TaskAssignment.status == "pending").all()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def get_finished_from_inspector(self, inspector_id: UUID) -> List[models.TaskAssignment]:
        try:
            return self.db.query(models.TaskAssignment).filter(models.TaskAssignment.inspector_id == inspector_id) \
                .filter(models.TaskAssignment.status == "completed").all()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def update_assigned_task(self, task_assignment_id: UUID,
                             task_assignment: schemas.TaskAssignmentUpdate) -> models.Task:
        try:
            db_task_assignment = self.get_assigned_task(task_assignment_id)
            update_data = task_assignment.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_task_assignment, key, value)
            self.db.commit()
            self.db.refresh(db_task_assignment)
            return db_task_assignment
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def delete_assigned_task(self, task_assignment_id: UUID):
        try:
            db_assignment_task = self.get_assigned_task(task_assignment_id)
            self.db.delete(db_assignment_task)
            self.db.commit()
            return
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()
