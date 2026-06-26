#код из routes.tasks.py
from fastapi import APIRouter, Depends, HTTPException,Query
from service.task_service import add_task, get_tasks_user, get_task_id, update_task_ser, delete_task_ser, status_update_ser
from schemas.task import Task_schema, TaskStatusUpdate
from core.security import get_current_user
from typing import Literal

tasks_router = APIRouter()

@tasks_router.post('', status_code=201)
def add_task_app(data: Task_schema, current_user = Depends(get_current_user)):
    result=add_task(data,current_user.id)
    if result is None:
        raise HTTPException(status_code=400,detail='Error add')
    return result

@tasks_router.get('')
def get_tasks(sort: Literal["asc", "desc"] | None = None,status:TaskStatusUpdate |None=None,limit: int = Query(10,le=100), offset: int = Query(0,ge=0),current_user=Depends(get_current_user)):
    result = get_tasks_user(sort,status,limit, offset,current_user.id)
    if result is None:
        raise HTTPException(status_code=400,detail='Error add')
    return result

@tasks_router.get('/{task_id}')
def get_task_id_app(task_id:int ,current_user=Depends(get_current_user)):
    result = get_task_id(task_id,current_user.id)
    if result is None:
        raise HTTPException(status_code=400,detail='Error add')
    return result

@tasks_router.put('/{task_id}',status_code=200)
def update_task_app(data: Task_schema, task_id:int, current_user=Depends(get_current_user)):
    result = update_task_ser(current_user.id,task_id,data)
    if result is None:
        raise HTTPException(status_code=400,detail='Error add')
    return result

@tasks_router.delete('/{task_id}',status_code=204)
def task_delete_app(task_id: int ,current_user=Depends(get_current_user)):
    result = delete_task_ser(current_user.id,task_id)
    if result is None:
        raise HTTPException(status_code=400,detail='Error add')


@tasks_router.patch('/{task_id}/status')
def status_update_app(task_id:int,data:TaskStatusUpdate,current_user=Depends(get_current_user)):
    result = status_update_ser(current_user.id,task_id,data)
    if result is None:
        raise HTTPException(status_code=400,detail='Error add')
    return result


    