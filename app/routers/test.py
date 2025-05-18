from fastapi import APIRouter
from app.tasks import generate_invoices, mark_overdue, send_reminders

# Initialize API router for task testing endpoints
test_router = APIRouter()

@test_router.get("/test-tasks")
def run_tasks():
    """
    Endpoint to manually trigger background Celery tasks.

    This is useful for testing that the tasks are correctly queued and executed by the worker.
    The tasks triggered:
        - generate_invoices: Creates invoices for active subscriptions.
        - mark_overdue: Marks invoices as overdue if past due date.
        - send_reminders: Sends reminders for pending invoices.

    Returns:
        dict: Confirmation message indicating tasks were triggered.
    """
    # Trigger asynchronous Celery tasks using .delay()
    generate_invoices.delay()
    mark_overdue.delay()
    send_reminders.delay()
    
    return {"message": "Tasks triggered"}
