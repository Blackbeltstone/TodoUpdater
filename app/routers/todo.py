import logging
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.crud import create_task, get_tasks, delete_task
from app.database import SessionLocal
from app.models import ToDo
# Create an API router instance
router = APIRouter()

# Initialize Jinja2 templates with the directory where templates are stored
templates = Jinja2Templates(directory="app/templates")

# Configure the logger for this module
logger = logging.getLogger(__name__)

def get_db():
    """
    Provides a database session dependency for routes.

    Yields:
        db (Session): A SQLAlchemy database session.
    
    Ensures the database session is properly closed after each use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
async def read_tasks(request: Request, db: Session = Depends(get_db)):
    """
    Handles the GET request to fetch and display all tasks.

    Args:
        request (Request): The HTTP request object.
        db (Session): A SQLAlchemy session, provided by the `get_db` dependency.

    Returns:
        HTMLResponse: Renders the 'todo.html' template with the list of tasks.

    Logs:
        INFO: "Fetched all tasks from the database."
    """
    tasks = get_tasks(db)  # Fetch all tasks from the database
    logger.info("Fetched all tasks from the database.")
    # Render the 'todo.html' template with the tasks context
    return templates.TemplateResponse("todo.html", {"request": request, "tasks": tasks})

@router.post("/add", response_class=HTMLResponse)
async def add_task(request: Request, db: Session = Depends(get_db)):
    """
    Handles the POST request to add a new task.

    Args:
        request (Request): The HTTP request object containing form data.
        db (Session): A SQLAlchemy session, provided by the `get_db` dependency.

    Returns:
        HTMLResponse: Renders the 'task_list.html' template with the updated list of tasks.

    Logs:
        INFO: "Added new task: {title}" if the task is successfully added.
        WARNING: "Attempted to add a task with an empty title." if the title is missing.
    """
    form = await request.form()  # Extract form data from the request
    title = form.get("title")    # Get the 'title' field from the form
    if title:
        create_task(db, title)   # Add the task to the database
        logger.info(f"Added new task: {title}")
    else:
        logger.warning("Attempted to add a task with an empty title.")
    
    tasks = get_tasks(db)  # Fetch the updated list of tasks
    # Render the 'task_list.html' template with the updated tasks context
    return templates.TemplateResponse("task_list.html", {"request": request, "tasks": tasks})

@router.post("/delete/{task_id}", response_class=HTMLResponse)
async def remove_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    """
    Handles the POST request to delete a task by its ID.

    Args:
        request (Request): The HTTP request object.
        task_id (int): The ID of the task to be deleted.
        db (Session): A SQLAlchemy session, provided by the `get_db` dependency.

    Returns:
        HTMLResponse: Renders the 'task_list.html' template with the updated list of tasks.

    Logs:
        INFO: "Deleted task with ID {task_id}: {task.title}" if the task is successfully deleted.
        WARNING: "Attempted to delete a non-existent task with ID {task_id}" if the task is not found.
    """
    task = delete_task(db, task_id)  # Attempt to delete the task by ID
    if task:
        logger.info(f"Deleted task with ID {task_id}: {task.title}")
    else:
        logger.warning(f"Attempted to delete a non-existent task with ID {task_id}")
    
    tasks = get_tasks(db)  # Fetch the updated list of tasks
    # Render the 'task_list.html' template with the updated tasks context
    return templates.TemplateResponse("task_list.html", {"request": request, "tasks": tasks})


@router.post("/toggle/{task_id}", response_class=HTMLResponse)
async def toggle_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    """
    Handles the POST request to toggle the completion status of a task.

    Args:
        request (Request): The HTTP request object.
        task_id (int): The ID of the task to be toggled.
        db (Session): A SQLAlchemy session, provided by the `get_db` dependency.

    Returns:
        HTMLResponse: Renders the 'task_list.html' template with the updated list of tasks.

    Logs:
        INFO: "Toggled task with ID {task_id} to {'completed' if task.completed else 'incomplete'}."
        WARNING: "Attempted to toggle a non-existent task with ID {task_id}."
    """
    task = db.query(ToDo).filter(ToDo.id == task_id).first()
    if task:
        task.completed = not task.completed  # Toggle the completed status
        db.commit()
    tasks = get_tasks(db)
    return templates.TemplateResponse("task_list.html", {"request": request, "tasks": tasks})
