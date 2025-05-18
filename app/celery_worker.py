from celery import Celery
from app.config import settings

# Initialize Celery app with the given broker URL from settings
celery_app = Celery("tasks", broker=settings.REDIS_BROKER_URL)

# Configure periodic task schedule (Celery Beat)
celery_app.conf.beat_schedule = {
    # Task to generate invoices every 10 seconds
    "generate-invoices": {
        "task": "app.tasks.generate_invoices",
        "schedule": 10.0
    },
    # Task to mark overdue invoices every 10 seconds
    "mark-overdue": {
        "task": "app.tasks.mark_overdue",
        "schedule": 10.0
    },
    # Task to send payment reminders every 10 seconds
    "send-reminders": {
        "task": "app.tasks.send_reminders",
        "schedule": 10.0
    },
}

# Set the timezone for Celery tasks
celery_app.conf.timezone = "UTC"

# Import the task definitions to ensure Celery can discover them
import app.tasks
