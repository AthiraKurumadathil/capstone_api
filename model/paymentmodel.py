from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from decimal import Decimal

class PaymentBase(BaseModel):
    org_id: int = Field(..., description="Organization ID")
    invoice_id: int = Field(..., description="Invoice ID")
    payment_date: date = Field(..., description="Payment date")
    amount: Decimal = Field(..., description="Payment amount")
    method: str = Field(..., min_length=1, max_length=20, description="Payment method")
    reference_no: Optional[str] = Field(None, max_length=100, description="Payment reference number")
    notes: Optional[str] = Field(None, max_length=500, description="Payment notes")

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    org_id: Optional[int] = None
    invoice_id: Optional[int] = None
    payment_date: Optional[date] = None
    amount: Optional[Decimal] = None
    method: Optional[str] = Field(None, min_length=1, max_length=20)
    reference_no: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=500)

class Payment(PaymentBase):
    payment_id: int

    class Config:
        from_attributes = True
