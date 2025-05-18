from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import models, schemas
import datetime
from fastapi import HTTPException

# Create a new user in the database
def create_user(db: Session, user: schemas.UserCreate):
    try:
        db_user = models.User(name=user.name, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

# Create a new plan
def create_plan(db: Session, plan: schemas.PlanCreate):
    try:
        db_plan = models.Plan(name=plan.name, price=plan.price, description=plan.description)
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)
        return db_plan
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create plan: {str(e)}")

# Create a new subscription and generate the first invoice
def create_subscription(db: Session, sub: schemas.SubscriptionCreate):
    try:
        # Validate user
        user = db.query(models.User).filter(models.User.id == sub.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {sub.user_id} not found")

        # Validate plan
        plan = db.query(models.Plan).filter(models.Plan.id == sub.plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail=f"Plan with ID {sub.plan_id} not found")

        # Set subscription period (30 days)
        today = datetime.date.today()
        end_date = today + datetime.timedelta(days=30)

        # Create subscription
        db_sub = models.Subscription(
            user_id=sub.user_id,
            plan_id=sub.plan_id,
            start_date=today,
            end_date=end_date,
            status=models.SubscriptionStatus.active
        )
        db.add(db_sub)
        db.commit()
        db.refresh(db_sub)

        # Generate invoice for this subscription
        invoice = create_invoice(db, db_sub)

        return {
            "subscription": db_sub,
            "invoice": invoice
        }

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create subscription: {str(e)}")

# Cancel a subscription by updating its status
def cancel_subscription(db: Session, sub_id: int):
    try:
        sub = db.query(models.Subscription).get(sub_id)
        if not sub:
            raise HTTPException(status_code=404, detail=f"Subscription with ID {sub_id} not found")
        sub.status = models.SubscriptionStatus.cancelled
        db.commit()
        return sub
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to cancel subscription: {str(e)}")

# Fetch all invoices associated with a specific user
def get_user_invoices(db: Session, user_id: int):
    try:
        invoices = db.query(models.Invoice).filter(models.Invoice.user_id == user_id).all()
        return invoices
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch invoices: {str(e)}")

# Create an invoice based on a subscription
def create_invoice(db: Session, sub: models.Subscription):
    try:
        today = datetime.date.today()
        due = today + datetime.timedelta(days=7)

        plan = db.query(models.Plan).filter(models.Plan.id == sub.plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail=f"Plan with ID {sub.plan_id} not found")

        invoice = models.Invoice(
            user_id=sub.user_id,
            subscription_id=sub.id,
            amount=plan.price,
            issue_date=today,
            due_date=due,
            status=models.InvoiceStatus.pending
        )
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return invoice
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create invoice: {str(e)}")

# Mark invoices as overdue if their due date has passed and they are still pending
def mark_overdue_invoices(db: Session):
    try:
        today = datetime.date.today()
        overdue = db.query(models.Invoice).filter(
            models.Invoice.status == models.InvoiceStatus.pending,
            models.Invoice.due_date < today
        ).all()
        for inv in overdue:
            inv.status = models.InvoiceStatus.overdue
        db.commit()
        return overdue
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to mark overdue invoices: {str(e)}")
