#код из main.py
from fastapi import FastAPI
from routes.users import router
from routes.tasks import tasks_router

app = FastAPI()


app.include_router(router,prefix='/users')
app.include_router(tasks_router, prefix='/tasks')