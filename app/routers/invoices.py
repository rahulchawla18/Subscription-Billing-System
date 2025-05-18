from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

# Create a router object for invoice-related endpoints
router = APIRouter()

# Endpoint to retrieve all invoices for a specific user
@router.get("/user/{user_id}", response_model=list[schemas.InvoiceOut])
def get_invoices(user_id: int, db: Session = Depends(get_db)):
    """
    Fetch all invoices for a given user.

    Args:
        user_id (int): ID of the user whose invoices are to be retrieved.
        db (Session): SQLAlchemy database session (injected by FastAPI).

    Returns:
        List[InvoiceOut]: A list of invoices related to the specified user.
    """
    return crud.get_user_invoices(db, user_id)
