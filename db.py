from sqlalchemy import create_engine
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from models import User, Task
from datetime import datetime

# строка подключения
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# создаем движок SqlAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()


def get_all_users():
    users = db.query(User).all()
    return users


def get_all_tasks():
    tasks = db.query(Task).all()
    return tasks


def create_user(user_name: str, email: str, password: str):
    try:
        new_user = User(username=user_name, email=email, hashed_password=password)
        db.add(new_user)
        db.commit()
        return {"status": "success", "message": "User created", "user_id": new_user.id}

    except IntegrityError as e:
        db.rollback()
        if "username" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        elif "email" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error: {str(e)}"
        )


def get_user_tasks(user_id: int):
    if not isinstance(user_id, int) or user_id <= 0:
        raise HTTPException(400, "Invalid user_id format")

    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks


def add_new_task(user_id: int, title: str, desc: str, due_date: str):
    if not all([user_id, title, due_date]):
        raise HTTPException(400, "Missing required fields")

    if not isinstance(user_id, int) or user_id <= 0:
        raise HTTPException(400, "Invalid user_id format")

    try:
        due_date_parsed = datetime.strptime(due_date, "%d.%m.%Y")
        if due_date_parsed < datetime.now():
            raise HTTPException(400, "Due date cannot be in the past")
    except ValueError:
        raise HTTPException(400, "Invalid date format. Use DD.MM.YYYY")

    try:
        new_task = Task(
            title=title,
            description=desc,
            due_date=due_date_parsed,
            user_id=user_id
        )
        db.add(new_task)
        db.commit()
        return {"status": "success", "task_id": new_task.id}

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(400, "Database integrity error")

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Server error: {str(e)}")


def update_task(task_id: int, upd_field_title: str, upd_field_desc: str, upd_due_date):
    if not isinstance(task_id, int) or task_id <= 0:
        raise HTTPException(400, "Invalid task_id format")

    old_task = db.query(Task).filter(Task.id == task_id).first()

    if len(upd_due_date) > 0:
        try:
            due_date_parsed = datetime.strptime(upd_due_date, "%d.%m.%Y")
            if due_date_parsed < datetime.now():
                raise HTTPException(400, "Due date cannot be in the past")
            if old_task.due_date != due_date_parsed:
                old_task.due_date = due_date_parsed
        except ValueError:
            raise HTTPException(400, "Invalid date format. Use DD.MM.YYYY")

    if len(upd_field_title) > 0 and old_task.title != upd_field_title:
        old_task.title = upd_field_title
    if len(upd_field_desc) > 0 and old_task.description != upd_field_desc:
        old_task.description = upd_field_desc

    db.commit()
    return {"status": "success updated", "task_id": task_id}


def close_task(task_id: int):
    if not isinstance(task_id, int) or task_id <= 0:
        raise HTTPException(400, "Invalid task_id format")

    task = db.query(Task).filter(Task.id == task_id).first()
    task.is_completed = True
    db.commit()
    return {"status": "success closed", "task_id": task_id}


def delete_task(task_id: int):
    if not isinstance(task_id, int) or task_id <= 0:
        raise HTTPException(400, "Invalid task_id format")

    task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(task)
    db.commit()
    return {"status": "success deleted", "task_id": task_id}
