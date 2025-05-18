from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Plan
from app.schemas import PlanCreate
from app.database import get_db
from typing import List

# Initialize API router for plan-related endpoints
router = APIRouter()

# Endpoint to create a new subscription plan
@router.post("/plans/")
def create_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    """
    Create a new subscription plan.

    Args:
        plan (PlanCreate): Schema containing name, price, and description of the plan.
        db (Session): SQLAlchemy session dependency.

    Returns:
        dict: Basic information about the newly created plan.
    """
    # Check if a plan with the same name already exists
    existing_plan = db.query(Plan).filter(Plan.name == plan.name).first()
    if existing_plan:
        raise HTTPException(status_code=400, detail="Plan with this name already exists")

    # Create and save the new plan
    new_plan = Plan(name=plan.name, price=plan.price, description=plan.description)
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return {"id": new_plan.id, "name": new_plan.name, "price": new_plan.price, "description": new_plan.description}

# Endpoint to retrieve a plan by its ID
@router.get("/{plan_id}", response_model=PlanCreate)
def get_plan_by_id(plan_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a subscription plan by its ID.

    Args:
        plan_id (int): ID of the plan to retrieve.
        db (Session): SQLAlchemy session dependency.

    Returns:
        PlanCreate: The requested plan details if found.
    """
    # Fetch the plan from the database
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    return plan
