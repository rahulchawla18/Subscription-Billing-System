# Subscription-Billing-System
A backend service for managing users, plans, subscriptions, and invoices, built with FastAPI, SQLAlchemy, and Celery. This service supports creating users, plans, subscriptions, automatic invoice generation, marking overdue invoices, and sending reminders.

# Table of Contents

- Features
- Tech Stack
- Setup & Installation
- Environment Variables
- Database
- API Endpoints
- Running Celery Workers & Scheduler
- Testing
- Project Structure
- License

# Features
- User registration and management
- CRUD for subscription plans
- Creating and cancelling subscriptions
- Automatic invoice generation upon subscription creation
- Mark overdue invoices after due date passes
- Scheduled tasks with Celery for generating invoices, marking overdue invoices, and sending reminders
- Error handling with meaningful messages

# Tech Stack
- Python 3.10+
- FastAPI
- SQLAlchemy (ORM)
- SQLite (default, can be replaced by any other supported DB)
- Celery for asynchronous task processing
- Redis as Celery broker
- Pydantic for data validation
- Uvicorn as ASGI server

# Setup & Installation
1. Clone the repository
    - git clone https://github.com/yourusername/subscription-billing-api.git
    - cd subscription-billing-api

2. Create and activate a virtual environment  
    - python -m venv venv
    - source venv/bin/activate  # Linux/macOS
    - venv\Scripts\activate     # Windows

3. Install dependencies
    - pip install -r requirements.txt

4. Run database migrations / create tables
    - Tables will be automatically created on app startup using SQLAlchemy.

# Environment Variables
- Configure your environment variables in .env or modify app/config.py:
    - DATABASE_URL=sqlite:///./test.db
    - REDIS_BROKER_URL=redis://localhost:6379/0
    - I am using redis using docker (docker run -d -p 6379:6379 redis)

# Database
- By default, SQLite is used (test.db file). You can switch to PostgreSQL, MySQL, or other supported databases by updating DATABASE_URL in the config.

# API Endpoints
1. Users
    - POST /users/ — Create a new user

2. Plans
    - POST /plans/ — Create a new subscription plan
    - GET /plans/{plan_id} — Get plan details by ID

3. Subscriptions
    - POST /subscriptions/ — Create a subscription
    - POST /subscriptions/cancel/{sub_id} — Cancel a subscription by ID

4. Invoices
    - GET /invoices/user/{user_id} — Get all invoices for a user

5. Test Scheduler (for triggering Celery tasks manually)
    - GET /test/test-tasks — Trigger invoice generation, overdue marking, and reminders tasks manually

# Running Celery Workers & Scheduler
- Make sure Redis is running on your machine.
- Start Celery worker:
    - celery -A app.celery_worker.celery_app worker --loglevel=info --pool=solo
- Start Celery beat scheduler:
    - celery -A app.celery_worker.celery_app beat --loglevel=info    

# Running the FastAPI app
- uvicorn app.main:app --reload
- Access interactive API docs at: http://localhost:8000/docs

# Testing
- To test Celery task execution manually:
    - curl http://localhost:8000/test/test-tasks
- This triggers background tasks for generating invoices, marking overdue invoices, and sending reminders.

# Project Structure
- app/
      - crud.py                  # Database CRUD operations with error handling
      - database.py              # SQLAlchemy engine, session, and Base setup
      - models.py                # SQLAlchemy ORM models (User, Plan, Subscription, Invoice, Enums)
      - schemas.py               # Pydantic schemas for data validation (UserCreate, PlanCreate, SubscriptionCreate, InvoiceOut, etc.)
      - tasks.py                 # Celery task definitions (generate invoices, mark overdue, send reminders)
      - celery_worker.py         # Celery app instance and beat scheduler configuration
      - config.py                # Application configuration (environment variables, settings)
- main.py                  # FastAPI application initialization and route inclusion
- routers/                 # API route modules, each with its own FastAPI router
      - users.py             # User endpoints (create user)
      - plans.py             # Plan endpoints (create/get plan)
      - subscriptions.py     # Subscription endpoints (create/cancel subscription)
      - invoices.py          # Invoice endpoints (get invoices by user)
      - test.py              # Test endpoints to trigger Celery tasks manually
- __init__.py              # Makes 'app' a package (optional but recommended)

# License
- This project is licensed under the MIT License.
