from fastapi import APIRouter, HTTPException, status
from typing import List
from model.attendancemodel import Attendance, AttendanceCreate, AttendanceUpdate
from services.attendancecrud import AttendanceCRUD

router = APIRouter(prefix="/attendance", tags=["attendance"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_attendance(attendance: AttendanceCreate):
    """
    Create a new attendance record.
    
    - **session_id**: Session ID (required)
    - **session_name**: Session name (required)
    - **enrollment_id**: Enrollment ID (required)
    - **status**: Attendance status (required)
    - **marked_at**: Timestamp when marked (required)
    - **marked_by**: User ID who marked attendance (optional)
    """
    try:
        result = AttendanceCRUD.create_attendance(attendance)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== GET ENDPOINTS ==============
@router.get("/session/{session_id}", response_model=List[Attendance])
async def get_attendance_by_session(session_id: int):
    """
    Retrieve all attendance records for a specific session.
    """
    try:
        attendance_records = AttendanceCRUD.get_attendance_by_session(session_id)
        return attendance_records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/enrollment/{enrollment_id}", response_model=List[Attendance])
async def get_attendance_by_enrollment(enrollment_id: int):
    """
    Retrieve all attendance records for a specific enrollment.
    """
    try:
        attendance_records = AttendanceCRUD.get_attendance_by_enrollment(enrollment_id)
        return attendance_records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[Attendance])
async def get_all_attendance():
    """
    Retrieve all attendance records.
    """
    try:
        attendance_records = AttendanceCRUD.get_all_attendance()
        return attendance_records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{attendance_id}", response_model=Attendance)
async def get_attendance(attendance_id: int):
    """
    Retrieve a single attendance record by ID.
    """
    try:
        attendance = AttendanceCRUD.get_attendance(attendance_id)
        if not attendance:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        return attendance
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{attendance_id}", response_model=dict)
async def update_attendance(attendance_id: int, attendance: AttendanceUpdate):
    """
    Update an existing attendance record.
    
    - **attendance_id**: Attendance ID (required in URL)
    - All other fields are optional
    """
    try:
        result = AttendanceCRUD.update_attendance(attendance_id, attendance)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{attendance_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_attendance(attendance_id: int):
    """
    Delete an attendance record by ID.
    """
    try:
        result = AttendanceCRUD.delete_attendance(attendance_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
