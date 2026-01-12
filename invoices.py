from fastapi import APIRouter, HTTPException, status
from typing import List
from model.invoicemodel import Invoice, InvoiceCreate, InvoiceUpdate
from services.invoicecrud import InvoiceCRUD

router = APIRouter(prefix="/invoices", tags=["invoices"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_invoice(invoice: InvoiceCreate):
    """
    Create a new invoice.
    
    - **org_id**: Organization ID (required)
    - **enrollment_id**: Enrollment ID (required)
    - **invoice_date**: Invoice date (required)
    - **due_date**: Due date (required)
    - **total_amount**: Total invoice amount (required)
    - **status**: Invoice status (required)
    """
    try:
        result = InvoiceCRUD.create_invoice(invoice)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== GET ENDPOINTS ==============
@router.get("/organization/{org_id}", response_model=List[Invoice])
async def get_invoices_by_organization(org_id: int):
    """
    Retrieve all invoices for a specific organization.
    """
    try:
        invoices = InvoiceCRUD.get_invoices_by_org(org_id)
        return invoices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/enrollment/{enrollment_id}", response_model=List[Invoice])
async def get_invoices_by_enrollment(enrollment_id: int):
    """
    Retrieve all invoices for a specific enrollment.
    """
    try:
        invoices = InvoiceCRUD.get_invoices_by_enrollment(enrollment_id)
        return invoices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[Invoice])
async def get_all_invoices():
    """
    Retrieve all invoices.
    """
    try:
        invoices = InvoiceCRUD.get_all_invoices()
        return invoices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{invoice_id}", response_model=Invoice)
async def get_invoice(invoice_id: int):
    """
    Retrieve a single invoice by ID.
    """
    try:
        invoice = InvoiceCRUD.get_invoice(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/amount/{enrollment_id}", response_model=dict)
async def get_invoice_amount_by_enrollment(enrollment_id: int):
    """
    Retrieve the invoice amount for an enrollment by joining:
    Enrollments -> Batches -> FeePlans
    
    - **enrollment_id**: Enrollment ID (required)
    
    Returns:
    - **enrollment_id**: The enrollment ID
    - **amount**: The fee plan amount associated with the enrollment's batch
    """
    try:
        result = InvoiceCRUD.get_invoice_amount_by_enrollment(enrollment_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"No invoice amount found for enrollment {enrollment_id}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{invoice_id}", response_model=dict)
async def update_invoice(invoice_id: int, invoice: InvoiceUpdate):
    """
    Update an existing invoice.
    
    - **invoice_id**: Invoice ID (required in URL)
    - All other fields are optional
    """
    try:
        result = InvoiceCRUD.update_invoice(invoice_id, invoice)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{invoice_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_invoice(invoice_id: int):
    """
    Delete an invoice by ID.
    """
    try:
        result = InvoiceCRUD.delete_invoice(invoice_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
