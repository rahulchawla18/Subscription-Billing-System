from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

# Initialize API router for subscription-related endpoints
router = APIRouter()

# Endpoint to create a new subscription
@router.post("/")
def create_subscription(sub: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    """
    Create a new subscription for a user to a plan.

    Args:
        sub (SubscriptionCreate): Schema containing user_id and plan_id.
        db (Session): SQLAlchemy session dependency.

    Returns:
        dict: Created subscription and its associated invoice.
    """
    return crud.create_subscription(db, sub)

# Endpoint to cancel an existing subscription
@router.post("/cancel/{sub_id}")
def cancel_subscription(sub_id: int, db: Session = Depends(get_db)):
    """
    Cancel an active subscription by its ID.

    Args:
        sub_id (int): ID of the subscription to cancel.
        db (Session): SQLAlchemy session dependency.

    Returns:
        Subscription: The updated subscription with cancelled status.
    """
    return crud.cancel_subscription(db, sub_id)
