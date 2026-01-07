from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class FeePlanBase(BaseModel):
    org_id: int = Field(..., description="Organization ID")
    name: str = Field(..., min_length=1, max_length=100, description="Fee plan name")
    billing_type: str = Field(..., min_length=1, max_length=20, description="Billing type")
    amount: Decimal = Field(..., description="Fee amount")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code (3 chars)")
    active: bool = Field(True, description="Active status")

class FeePlanCreate(FeePlanBase):
    pass

class FeePlanUpdate(BaseModel):
    org_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    billing_type: Optional[str] = Field(None, min_length=1, max_length=20)
    amount: Optional[Decimal] = None
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    active: Optional[bool] = None

class FeePlan(FeePlanBase):
    fee_plan_id: int

    class Config:
        from_attributes = True
