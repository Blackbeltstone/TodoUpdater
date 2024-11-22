from sqlalchemy.orm import Session
from app.models import ToDo
from app.database import SessionLocal

def create_task(db: Session, title: str):
    """
    Creates a new task in the database.

    Args:
        db (Session): A SQLAlchemy session for database interaction.
        title (str): The title of the task to be created.

    Returns:
        ToDo: The created task object.

    Behavior:
        - Initializes a new `ToDo` object with the given title.
        - Adds the task to the database session and commits the changes.
        - Refreshes the task object to get its updated state (e.g., assigned ID).
    """
    # Initialize a new task with the provided title and default 'completed' status as False
    db_task = ToDo(title=title, completed=False)
    db.add(db_task)  # Add the task to the session
    db.commit()      # Commit the transaction to save the task in the database
    db.refresh(db_task)  # Refresh the task object to get the generated ID
    return db_task  # Return the created task object

def get_tasks(db: Session):
    """
    Retrieves all tasks from the database.

    Args:
        db (Session): A SQLAlchemy session for database interaction.

    Returns:
        List[ToDo]: A list of all task objects in the database.

    Behavior:
        - Queries the `ToDo` table and returns all task records.
    """
    # Query the database for all tasks and return the result
    return db.query(ToDo).all()

def delete_task(db: Session, task_id: int):
    """
    Deletes a task from the database by its ID.

    Args:
        db (Session): A SQLAlchemy session for database interaction.
        task_id (int): The ID of the task to be deleted.

    Returns:
        ToDo | None: The deleted task object if found, otherwise None.

    Behavior:
        - Queries the database for a task with the given ID.
        - If the task exists, it is deleted and the changes are committed.
        - If the task does not exist, returns None.
    """
    # Retrieve the task with the specified ID
    task = db.query(ToDo).filter(ToDo.id == task_id).first()
    if task:
        db.delete(task)  # Delete the task from the session
        db.commit()      # Commit the transaction to apply the deletion
        return task      # Return the deleted task object
    return None  # Return None if the task was not found
