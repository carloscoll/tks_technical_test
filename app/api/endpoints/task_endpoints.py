from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.db.session import get_db_session
from app.core.schemas import task_schemas as schemas
from app.services.task_service import TaskService as Service

router = APIRouter()


@router.get("/task_id={task_id}", response_model=schemas.Task)
async def get_task(task_id: UUID, session=Depends(get_db_session)):
    service = Service(session)
    task = service.get_task(task_id)
    return task


@router.get("/all/", response_model=List[schemas.Task])
async def get_all_tasks(session=Depends(get_db_session)):
    service = Service(session)
    tasks = service.get_tasks()
    return tasks


@router.get("/available/all", response_model=List[schemas.Task])
async def get_all_available_tasks(session=Depends(get_db_session)):
    service = Service(session)
    available_tasks = service.get_available_tasks()
    return available_tasks


@router.post("/", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, session=Depends(get_db_session)):
    service = Service(session)
    created_task = service.create_task(task)
    return created_task


@router.put("/task_id={task_id}", response_model=schemas.Task)
async def update_task(task_id: UUID, task: schemas.TaskUpdate,
                      session=Depends(get_db_session)):
    service = Service(session)
    updated_task = service.update_task(task_id, task)
    return updated_task


@router.delete("/task_id={task_id}")
async def delete_task(task_id: UUID, session=Depends(get_db_session)):
    service = Service(session)
    service.delete_task(task_id)
    return
