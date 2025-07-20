from fastapi import FastAPI, Body, status, Query
from fastapi.responses import FileResponse
from db import get_user_tasks, add_new_task, update_task, delete_task, create_user, get_all_users, get_all_tasks, \
    close_task

app = FastAPI()


@app.get("/")
async def main():
    return FileResponse("public/index.html")


@app.get("/api/get_all_tasks")
def get_all_tasks_endpoint():
    return get_all_tasks()


@app.get("/api/get_users_info")
def get_all_user_info():
    return get_all_users()


@app.get("/api/get_user_tasks/{user_id}")
def get_user_tasks_endpoint(user_id: int):
    return get_user_tasks(user_id)


@app.post("/api/create_user", status_code=status.HTTP_201_CREATED)
def create_user_endpoint(data=Body()):
    return create_user(data['user_name'], data['email'], data['password'])


@app.post("/api/create_task")
def create_task(data=Body()):
    return add_new_task(data['user_id'], data['title'], data['desc'], data['due_date'])


@app.put("/api/update_task")
def update_task_endpoint(data=Body()):
    return update_task(data['task_id'], data['title'], data['desc'], data['due_date'])


@app.put("/api/close_task")
def close_task_endpoint(data=Body()):
    return close_task(data["task_id"])


@app.delete("/api/delete_task/{task_id}")
def delete_task_endpoint(task_id: int):
    return delete_task(task_id)

