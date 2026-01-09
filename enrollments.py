from fastapi import APIRouter, HTTPException, status
from typing import List
from model.enrollmentmodel import Enrollment, EnrollmentCreate, EnrollmentUpdate
from services.enrollmentcrud import EnrollmentCRUD

router = APIRouter(prefix="/enrollments", tags=["enrollments"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_enrollment(enrollment: EnrollmentCreate):
    """
    Create a new enrollment record.
    
    - **org_id**: Organization ID (required)
    - **batch_id**: Batch ID (required)
    - **student_id**: Student ID (required)
    - **enrolled_on**: Enrollment date (required)
    - **status**: Enrollment status (required)
    """
    try:
        result = EnrollmentCRUD.create_enrollment(enrollment)
        return result
    except Exception as e:
        error_msg = str(e)
        # Return 409 Conflict for duplicate enrollment
        if "already enrolled" in error_msg.lower():
            raise HTTPException(status_code=409, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)

# ============== GET ENDPOINTS ==============
@router.get("/student/{student_id}", response_model=List[Enrollment])
async def get_enrollments_by_student(student_id: int):
    """
    Retrieve all enrollments for a specific student.
    """
    try:
        enrollments = EnrollmentCRUD.get_enrollments_by_student(student_id)
        return enrollments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/batch/{batch_id}", response_model=List[Enrollment])
async def get_enrollments_by_batch(batch_id: int):
    """
    Retrieve all enrollments for a specific batch.
    """
    try:
        enrollments = EnrollmentCRUD.get_enrollments_by_batch(batch_id)
        return enrollments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/organization/{org_id}", response_model=List[Enrollment])
async def get_enrollments_by_org(org_id: int):
    """
    Retrieve all enrollments for a specific organization.
    """
    try:
        enrollments = EnrollmentCRUD.get_enrollments_by_org(org_id)
        return enrollments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[Enrollment])
async def get_all_enrollments():
    """
    Retrieve all enrollment records.
    """
    try:
        enrollments = EnrollmentCRUD.get_all_enrollments()
        return enrollments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{enrollment_id}", response_model=Enrollment)
async def get_enrollment(enrollment_id: int):
    """
    Retrieve a single enrollment record by ID.
    """
    try:
        enrollment = EnrollmentCRUD.get_enrollment(enrollment_id)
        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment record not found")
        return enrollment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{enrollment_id}", response_model=dict)
async def update_enrollment(enrollment_id: int, enrollment: EnrollmentUpdate):
    """
    Update an existing enrollment record.
    
    - **enrollment_id**: Enrollment ID (required in URL)
    - All other fields are optional
    """
    try:
        result = EnrollmentCRUD.update_enrollment(enrollment_id, enrollment)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{enrollment_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_enrollment(enrollment_id: int):
    """
    Delete an enrollment record by ID.
    """
    try:
        result = EnrollmentCRUD.delete_enrollment(enrollment_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
