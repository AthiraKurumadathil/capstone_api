from fastapi import APIRouter, HTTPException, status
from typing import List
from model.studentmodel import Student, StudentCreate, StudentUpdate
from services.studentcrud import StudentCRUD

router = APIRouter(prefix="/students", tags=["students"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreate):
    """
    Create a new student.
    
    - **org_id**: Organization ID (required)
    - **first_name**: First name (required)
    - **last_name**: Last name (required)
    - **dob**: Date of birth (optional)
    - **guardian_name**: Guardian name (optional)
    - **guardian_phone**: Guardian phone (optional)
    - **guardian_email**: Guardian email (optional)
    - **notes**: Additional notes (optional)
    - **active**: Active status (default: true)
    """
    try:
        result = StudentCRUD.create_student(student)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== GET ENDPOINTS ==============
@router.get("/organization/{org_id}", response_model=List[Student])
async def get_students_by_organization(org_id: int):
    """
    Retrieve all students for a specific organization.
    """
    try:
        students = StudentCRUD.get_students_by_org(org_id)
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[Student])
async def get_all_students():
    """
    Retrieve all students.
    """
    try:
        students = StudentCRUD.get_all_students()
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{student_id}", response_model=Student)
async def get_student(student_id: int):
    """
    Retrieve a single student by ID.
    """
    try:
        student = StudentCRUD.get_student(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{student_id}", response_model=dict)
async def update_student(student_id: int, student: StudentUpdate):
    """
    Update an existing student.
    
    - **student_id**: Student ID (required in URL)
    - All other fields are optional
    """
    try:
        result = StudentCRUD.update_student(student_id, student)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{student_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_student(student_id: int):
    """
    Delete a student by ID.
    """
    try:
        result = StudentCRUD.delete_student(student_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
