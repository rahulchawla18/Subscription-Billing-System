from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    name: str
    email: str

class PlanCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

    class Config:
        orm_mode = True

class SubscriptionCreate(BaseModel):
    user_id: int
    plan_id: int

class InvoiceOut(BaseModel):
    id: int
    amount: float
    issue_date: date
    due_date: date
    status: str

    class Config:
        orm_mode = True
