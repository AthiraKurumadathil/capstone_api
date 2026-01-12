from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form
from typing import List, Optional
from model.studentmodel import Student, StudentCreate, StudentUpdate
from services.studentcrud import StudentCRUD

router = APIRouter(prefix="/students", tags=["students"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_student(
    org_id: int = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    dob: Optional[str] = Form(None),
    guardian_name: Optional[str] = Form(None),
    guardian_phone: Optional[str] = Form(None),
    guardian_email: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    active: Optional[bool] = Form(True),
    student_photo: Optional[UploadFile] = File(None)
):
    """
    Create a new student with optional photo upload.
    
    - **org_id**: Organization ID (required)
    - **first_name**: First name (required)
    - **last_name**: Last name (required)
    - **dob**: Date of birth (optional)
    - **guardian_name**: Guardian name (optional)
    - **guardian_phone**: Guardian phone (optional)
    - **guardian_email**: Guardian email (optional)
    - **notes**: Additional notes (optional)
    - **active**: Active status (default: true)
    - **student_photo**: Student photo file (optional)
    """
    try:
        result = StudentCRUD.create_student_with_photo(
            org_id=org_id,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            guardian_name=guardian_name,
            guardian_phone=guardian_phone,
            guardian_email=guardian_email,
            notes=notes,
            active=active,
            student_photo=student_photo
        )
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
