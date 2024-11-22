from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL, specifies the database file location
DATABASE_URL = "sqlite:///./todo.db"

# Create the SQLite engine
# - `check_same_thread=False` allows the database to be accessed from different threads.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class for database interactions
SessionLocal = sessionmaker(
    autocommit=False,   # Disables automatic commits, changes must be explicitly committed
    autoflush=False,    # Disables automatic flushing of changes to the database
    bind=engine         # Binds the session to the SQLite engine
)

# Base class for declarative models
# - All models will inherit from this base class to create tables in the database.
Base = declarative_base()

def init_db():
    """
    Initializes the database by creating all tables.

    Behavior:
        - Uses the metadata of the `Base` class to create tables in the database.
        - If tables already exist, they are not recreated (no changes are made).
    
    Usage:
        - This function should be called at the application startup to ensure that
          all necessary tables are created before any database operations are performed.
    """
    # Create all tables based on the defined models (e.g., `ToDo` model)
    Base.metadata.create_all(bind=engine)
