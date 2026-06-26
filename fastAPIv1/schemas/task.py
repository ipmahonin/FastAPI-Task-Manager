from pydantic import BaseModel
import enum

class Task_schema(BaseModel):
    title: str
    description: str

class TaskStatus(enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskStatusUpdate(BaseModel):
    status: TaskStatus