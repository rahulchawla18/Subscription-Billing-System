import logging
import datetime
from app.celery_worker import celery_app
from app.database import SessionLocal
from app import crud, models

logger = logging.getLogger(__name__)

@celery_app.task
def generate_invoices():
    logger.info("Starting task: generate_invoices")
    db = SessionLocal()
    try:
        today = datetime.date.today()
        subs = db.query(models.Subscription).filter(
            models.Subscription.status == models.SubscriptionStatus.active,
            models.Subscription.start_date == today
        ).all()
        for sub in subs:
            try:
                crud.create_invoice(db, sub)
                logger.info(f"Invoice created for subscription ID {sub.id}")
            except Exception as e:
                logger.error(f"Failed to create invoice for subscription ID {sub.id}: {e}")
    except Exception as e:
        logger.error(f"Error in generate_invoices task: {e}")
        raise
    finally:
        db.close()
    logger.info("Completed task: generate_invoices")
    return "Invoices generated"

@celery_app.task
def mark_overdue():
    logger.info("Starting task: mark_overdue")
    db = SessionLocal()
    try:
        overdue_invoices = crud.mark_overdue_invoices(db)
        logger.info(f"Marked {len(overdue_invoices)} invoices as overdue")
    except Exception as e:
        logger.error(f"Error in mark_overdue task: {e}")
        raise
    finally:
        db.close()
    logger.info("Completed task: mark_overdue")
    return "Marked overdue invoices"

@celery_app.task
def send_reminders():
    logger.info("Starting task: send_reminders")
    db = SessionLocal()
    try:
        today = datetime.date.today()
        unpaid_invoices = db.query(models.Invoice).filter(
            models.Invoice.status == models.InvoiceStatus.pending,
            models.Invoice.due_date <= today
        ).all()
        for inv in unpaid_invoices:
            logger.info(f"Reminder: Invoice #{inv.id} for User {inv.user_id} is still unpaid.")
    except Exception as e:
        logger.error(f"Error in send_reminders task: {e}")
        raise
    finally:
        db.close()
    logger.info("Completed task: send_reminders")
