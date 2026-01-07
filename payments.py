from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from model.paymentmodel import Payment, PaymentCreate, PaymentUpdate
from services.paymentcrud import PaymentCRUD
from utils.auth import verify_jwt_token

router = APIRouter(prefix="/payments", tags=["payments"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_payment(payment: PaymentCreate, current_user: dict = Depends(verify_jwt_token)):
    """
    Create a new payment.
    
    - **org_id**: Organization ID (required)
    - **invoice_id**: Invoice ID (required)
    - **payment_date**: Payment date (required)
    - **amount**: Payment amount (required)
    - **method**: Payment method (required)
    - **reference_no**: Payment reference number (optional)
    - **notes**: Payment notes (optional)
    """
    try:
        result = PaymentCRUD.create_payment(payment)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== GET ENDPOINTS ==============
@router.get("/organization/{org_id}", response_model=List[Payment])
async def get_payments_by_organization(org_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve all payments for a specific organization.
    """
    try:
        payments = PaymentCRUD.get_payments_by_org(org_id)
        return payments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/invoice/{invoice_id}", response_model=List[Payment])
async def get_payments_by_invoice(invoice_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve all payments for a specific invoice.
    """
    try:
        payments = PaymentCRUD.get_payments_by_invoice(invoice_id)
        return payments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[Payment])
async def get_all_payments(current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve all payments.
    """
    try:
        payments = PaymentCRUD.get_all_payments()
        return payments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{payment_id}", response_model=Payment)
async def get_payment(payment_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve a single payment by ID.
    """
    try:
        payment = PaymentCRUD.get_payment(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{payment_id}", response_model=dict)
async def update_payment(payment_id: int, payment: PaymentUpdate, current_user: dict = Depends(verify_jwt_token)):
    """
    Update an existing payment.
    
    - **payment_id**: Payment ID (required in URL)
    - All other fields are optional
    """
    try:
        result = PaymentCRUD.update_payment(payment_id, payment)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{payment_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_payment(payment_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Delete a payment by ID.
    """
    try:
        result = PaymentCRUD.delete_payment(payment_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
