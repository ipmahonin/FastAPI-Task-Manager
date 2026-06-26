#код из service.task_service.py
from schemas.task import Task_schema, TaskStatusUpdate
from repository.task_repository import create_task,get_tasks_by_user,get_task_by_id,update_task,delete_task,status_update
from db import SessionLocal
from core.logger import logger

def add_task(data:Task_schema, user_id:int):
    db = SessionLocal()
    try:
        result = create_task(db,data,user_id)
        logger.info(f"User {user_id} created task {result.id}")
        return{
            'id':result.id,
            'title':result.title,
            'description':result.description
        }
    finally:
        db.close()

def get_tasks_user(sort, status, limit, offset,user_id:int):
    db = SessionLocal()
    result = []
    try:
        rows = get_tasks_by_user(db,sort, status, limit, offset, user_id)
        for row in rows:
            result.append(
                {
            'id':row.id,
            'title':row.title,
            'description':row.description
        }
            )
        return result
    finally:
        db.close()

def get_task_id(task_id:int, user_id:int):
    db = SessionLocal()
    try:
        result = get_task_by_id(db, task_id,user_id)
        return{
            'id':result.id,
            'title':result.title,
            'description':result.description
        }
    finally:
        db.close()

def update_task_ser(user_id:int, task_id:int, data:Task_schema):
    db = SessionLocal()
    try:
        result = update_task(db,user_id,task_id,data)
        logger.info(f"User {user_id} update task {result.id}.")
        return{
            'id':result.id,
            'title':result.title,
            'description':result.description
        }
    finally:
        db.close()

def delete_task_ser(user_id:int, task_id:int):
    db = SessionLocal()
    try:
        result = delete_task(db,user_id,task_id)
        logger.info(f"User {user_id} deleted task {task_id}")
        return result
    finally:
        db.close()

def status_update_ser(user_id:int,task_id:int,new_status:TaskStatusUpdate):
    db =SessionLocal()
    try:
        result = status_update(db,user_id,task_id,new_status)
        logger.info(f"User {user_id} status update task {result.id}.")
        return{
            'id':result.id,
            'status': result.status.value
        }
    finally:
        db.close()