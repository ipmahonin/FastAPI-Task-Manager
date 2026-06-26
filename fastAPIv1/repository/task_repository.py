#код из task_repository.py
from sqlalchemy.orm import Session
from models.task import Task
from schemas.task import Task_schema
from fastapi import HTTPException
from schemas.task import TaskStatus, TaskStatusUpdate
from sqlalchemy import desc

def create_task(db: Session, task: Task_schema, user_id:int):
    add_task = Task(title=task.title, description=task.description, user_id=user_id)
    db.add(add_task)
    db.commit()
    db.refresh(add_task)
    return add_task

def get_tasks_by_user(db: Session,sort,status,limit, offset, user_id:int):
    task = db.query(Task
    ).filter(Task.user_id == user_id)
    if status is not None:
        task=task.filter(Task.status == status.status) 
    if sort == "desc":
       task = task.order_by(Task.created_at.desc())
    elif sort == "asc":
        task = task.order_by(Task.created_at)
    return  task.offset(offset).limit(limit).all()

def get_task_by_id(db: Session, task_id:int, user_id:int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404,detail="Not found")
    if not  task.user_id == user_id:
        raise HTTPException(status_code=403,detail='No access')
    return task

def update_task(db: Session, user_id:int, task_id:int, task_new: Task_schema):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404,detail="Not found")
    if not  task.user_id == user_id:
        raise HTTPException(status_code=403,detail='No access')
    task.title = task_new.title
    task.description = task_new.description
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, user_id: int, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404,detail="Not found")
    if not  task.user_id == user_id:
        raise HTTPException(status_code=403,detail='No access')
    db.delete(task)
    db.commit()
    return {"message": "deleted"}

def status_update(db:Session,user_id:int,task_id:int,new_status:TaskStatusUpdate):
    task= db.query(Task).filter(Task.id==task_id).first()
    if task is None:
        raise HTTPException(status_code=404,detail="Not found")
    if not  task.user_id == user_id:
        raise HTTPException(status_code=403,detail='No access')
    task.status=new_status.status
    db.commit()
    db.refresh(task)
    return task