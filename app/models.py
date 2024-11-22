from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class ToDo(Base):
    """
    SQLAlchemy model representing a task in the ToDo list application.

    Attributes:
        id (Integer): The primary key of the task, a unique identifier.
        title (String): The title or description of the task.
        completed (Boolean): A flag indicating whether the task is completed (default is False).
    """
    __tablename__ = "todos"  # Defines the table name in the database

    # Primary key column 'id', unique identifier for each task
    id = Column(Integer, primary_key=True, index=True)

    # Column 'title' for storing the task title, indexed for faster search
    title = Column(String, index=True)

    # Column 'completed' to track the completion status of the task (default is False)
    completed = Column(Boolean, default=False)
