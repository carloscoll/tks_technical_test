from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.db.session import get_db_session
from app.core.schemas import task_assignment_schemas as schemas
from app.services.task_assignment_service import TaskAssignmentService as Service

router = APIRouter()


@router.get("/task_assignment_id={task_assignment_id}", response_model=schemas.TaskAssignment)
async def get_assigned_task(task_assignment_id: UUID, session=Depends(get_db_session)):
    service = Service(session)
    assigned_task = service.get_assigned_task(task_assignment_id)
    return assigned_task


@router.get("/all/", response_model=List[schemas.TaskAssignment])
async def get_all_assigned_tasks(session=Depends(get_db_session)):
    service = Service(session)
    assigned_tasks = service.get_assigned_tasks()
    return assigned_tasks


@router.get("/inspector_id={inspector_id}/all/", response_model=List[schemas.TaskAssignment])
async def get_all_assigned_tasks_from_inspector(inspector_id: UUID, session=Depends(get_db_session)):
    service = Service(session)
    assigned_tasks = service.get_from_inspector(inspector_id)
    return assigned_tasks


@router.get("/inspector_id={inspector_id}/unfinished/all/", response_model=List[schemas.TaskAssignment])
async def get_unfinished_tasks_from_inspector(inspector_id: UUID, session=Depends(get_db_session)):
    service = Service(session)
    assigned_tasks = service.get_unfinished_from_inspector(inspector_id)
    return assigned_tasks


@router.get("/inspector_id={inspector_id}/finished/all/", response_model=List[schemas.TaskAssignment])
async def get_finished_tasks_from_inspector(inspector_id: UUID, session=Depends(get_db_session)):
    service = Service(session)
    assigned_tasks = service.get_finished_from_inspector(inspector_id)
    return assigned_tasks


@router.post("/assign/inspector_id={inspector_id}&task_id={task_id}", response_model=schemas.TaskAssignment)
async def create_assigned_task(inspector_id: UUID, task_id: UUID, task: schemas.TaskAssignmentCreate,
                               session=Depends(get_db_session)):
    service = Service(session)
    created_task = service.assign_task(inspector_id, task_id, task)
    return created_task


@router.post("/finish/task_assignment_id={task_assignment_id}", response_model=schemas.TaskAssignment)
async def finish_assigned_task(task_assignment_id: UUID, task: schemas.TaskAssignmentEvaluation,
                               session=Depends(get_db_session)):
    service = Service(session)
    finished_task = service.finish_task(task_assignment_id, task)
    return finished_task


@router.put("/task_assignment_id={task_assignment_id}", response_model=schemas.TaskAssignment)
async def update_assigned_task(task_assignment_id: UUID, task: schemas.TaskAssignmentUpdate,
                               session=Depends(get_db_session)):
    service = Service(session)
    assigned_task = service.update_assigned_task(task_assignment_id, task)
    return assigned_task


@router.delete("/task_assignment_id={task_assignment_id}")
async def delete_assigned_task(task_assignment_id: UUID, session=Depends(get_db_session)):
    service = Service(session)
    service.delete_assigned_task(task_assignment_id)
    return
