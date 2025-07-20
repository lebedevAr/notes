from sqlalchemy import create_engine
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String
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

def get_user_tasks(user_id):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks



def add_new_task(user_id, title, desc, due_date):
    due_date_red = datetime.strptime(due_date, "%d.%m.%Y")
    new_task = Task(title=title, description=desc, due_date=due_date_red, user_id=user_id)
    db.add(new_task)
    db.commit()
    return True

def update_task(user_id, task_id, upd_field_title, upd_field_desc, upd_due_date):
    pass

def delete_task(user_id, task_id):
    pass
