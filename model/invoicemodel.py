from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from decimal import Decimal

class InvoiceBase(BaseModel):
    org_id: int = Field(..., description="Organization ID")
    enrollment_id: int = Field(..., description="Enrollment ID")
    invoice_date: date = Field(..., description="Invoice date")
    due_date: date = Field(..., description="Due date")
    total_amount: Decimal = Field(..., description="Total invoice amount")
    status: str = Field(..., min_length=1, max_length=20, description="Invoice status")

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    org_id: Optional[int] = None
    enrollment_id: Optional[int] = None
    invoice_date: Optional[date] = None
    due_date: Optional[date] = None
    total_amount: Optional[Decimal] = None
    status: Optional[str] = Field(None, min_length=1, max_length=20)

class Invoice(InvoiceBase):
    invoice_id: int

    class Config:
        from_attributes = True
