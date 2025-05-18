from fastapi import FastAPI
from app.routers import users, subscriptions, invoices, plans, test
from app.database import Base, engine

# Create database tables based on models
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app instance
app = FastAPI(
    title="Subscription Billing API",
    description="API for managing users, plans, subscriptions, and invoices",
    version="1.0.0",
)

# Include routers for different API endpoints with prefixes and tags
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])
app.include_router(plans.router, prefix="/plans", tags=["Plans"])
app.include_router(test.test_router, prefix="/test", tags=["Test Scheduler"])
