from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

# Initialize API router for user-related endpoints
router = APIRouter()

@router.post("/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the system.

    Args:
        user (schemas.UserCreate): The user data sent in the request body.
        db (Session): SQLAlchemy database session (injected by FastAPI dependency).

    Returns:
        schemas.UserCreate: The created user's information.
    """
    return crud.create_user(db, user)
