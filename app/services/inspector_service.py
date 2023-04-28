import uuid
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models import models
from app.core.schemas import inspector_schemas as schemas


class InspectorService:
    def __init__(self, db: Session):
        self.db = db

    def create_inspector(self, inspector: schemas.InspectorCreate) -> models.Inspector:
        try:
            db_inspector = models.Inspector(**inspector.dict())
            db_inspector.id = uuid.uuid4()
            self.db.add(db_inspector)
            self.db.commit()
            self.db.refresh(db_inspector)
            return db_inspector
        except Exception as e:
            self.db.rollback()
            raise e

    def get_inspector(self, inspector_id: UUID) -> models.Inspector:
        inspector = self.db.query(models.Inspector).filter(models.Inspector.id == inspector_id).first()
        return inspector

    def get_inspectors(self) -> List[models.Inspector]:
        return self.db.query(models.Inspector).all()

    def update_inspector(self, inspector_id: UUID, inspector: schemas.InspectorUpdate) -> models.Inspector:
        try:
            db_inspector = self.get_inspector(inspector_id)
            update_data = inspector.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_inspector, key, value)
            self.db.commit()
            self.db.refresh(db_inspector)
        except Exception as e:
            self.db.rollback()
            raise e
        return db_inspector

    def delete_inspector(self, inspector_id: UUID):
        try:
            db_inspector = self.get_inspector(inspector_id)
            self.db.delete(db_inspector)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        return

