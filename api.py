from fastapi import FastAPI, Body, status, Request, Query
from fastapi.responses import JSONResponse, FileResponse
from db import get_user_tasks, add_new_task, update_task, delete_task, create_user, get_all_users, get_all_tasks


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


@app.post("/api/create_user")
def create_user_endpoint(data = Body()):
    return create_user(data['user_name'], data['email'], data['password'])


@app.post("/api/create_task")
def create_task(data = Body()):
    return add_new_task(data['user_id'], data['title'], data['desc'], data['due_date'])


@app.put("/api/update_task")
def update_task_endpoint(data = Body()):
    return update_task(data['user_id'], data['task_id'], data['title'], data['desc'], data['due_date'])


@app.delete("/api/delete_task/{task_id}")
def delete_task_endpoint(task_id: int, user_id: int = Query()):
    return delete_task(user_id, task_id)
