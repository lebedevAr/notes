from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import  Column, Integer, String, Text, DateTime, Boolean, ForeignKey, create_engine
from datetime import datetime


class Base(DeclarativeBase): pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    telegram_id = Column(String, nullable=True)  # Для привязки Telegram-аккаунта
    tasks = relationship("Task", back_populates="user")
    knowledge_items = relationship("KnowledgeItem", back_populates="user")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)  # None = бессрочная
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")


class KnowledgeItem(Base):
    __tablename__ = "knowledge_items"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)  # Может быть Markdown или plain text
    source_url = Column(String, nullable=True)  # Если это ссылка
    created_at = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="knowledge_items")


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# создаем движок SqlAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
Base.metadata.create_all(engine)