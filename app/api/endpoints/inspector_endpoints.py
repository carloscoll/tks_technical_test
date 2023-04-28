from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.db.session import get_db_session
from app.core.schemas import inspector_schemas
from app.services.inspector_service import InspectorService as Service

router = APIRouter()


@router.get("/inspector_id={inspector_id}", response_model=inspector_schemas.Inspector)
async def get_inspector(inspector_id: UUID, session=Depends(get_db_session)):
    service = Service(session)
    inspector = service.get_inspector(inspector_id)
    return inspector


@router.get("/all/", response_model=List[inspector_schemas.Inspector])
async def get_all_inspectors(session=Depends(get_db_session)):
    service = Service(session)
    inspectors = service.get_inspectors()
    return inspectors


@router.post("/", response_model=inspector_schemas.Inspector)
async def create_inspector(inspector: inspector_schemas.InspectorCreate, session=Depends(get_db_session)):
    service = Service(session)
    created_inspector = service.create_inspector(inspector)
    return created_inspector


@router.put("/inspector_id={inspector_id}", response_model=inspector_schemas.Inspector)
async def update_inspector(inspector_id: UUID, inspector: inspector_schemas.InspectorUpdate,
                           session=Depends(get_db_session)):
    service = Service(session)
    updated_inspector = service.update_inspector(inspector_id, inspector)
    return updated_inspector


@router.delete("/inspector_id={inspector_id}")
async def delete_inspector(inspector_id: UUID, session=Depends(get_db_session)):
    service = Service(session)
    service.delete_inspector(inspector_id)
    return
