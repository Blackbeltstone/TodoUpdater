from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routers import todo
import logging
from app.database import init_db

# Initialize the database
init_db()

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Define the log message format
)
logger = logging.getLogger(__name__)  # Get the logger for this module

# Create the FastAPI application instance
app = FastAPI()

# Set up Jinja2 templates with the specified directory
templates = Jinja2Templates(directory="app/templates")

# Mount the "static" folder to serve static files (e.g., CSS, JavaScript)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include the ToDo router for handling task-related routes
app.include_router(todo.router)

@app.get("/")
def read_root(request: Request):
    """
    Handles the GET request for the root endpoint ("/").

    Args:
        request (Request): The HTTP request object.

    Returns:
        TemplateResponse: Renders the 'index.html' template.

    Behavior:
        - Renders the homepage ('index.html') template.
    """
    logger.info("Accessed the root endpoint.")
    return templates.TemplateResponse("todo.html", {"request": request})

@app.get("/items/{item_id}")
def read_item(request: Request, item_id: str):
    """
    Handles the GET request for the item details endpoint ("/items/{item_id}").

    Args:
        request (Request): The HTTP request object.
        item_id (str): The ID of the item to be retrieved.

    Returns:
        dict: A JSON response with the item ID and a placeholder message.

    Note:
        - This is a placeholder function and can be extended to fetch actual item details.
    """
    logger.info(f"Accessed item endpoint for item ID: {item_id}")
    return {"item_id": item_id, "message": "This is a placeholder response for item details."}
