from utils.database import get_db_connection
from model.attendancemodel import AttendanceCreate, AttendanceUpdate

class AttendanceCRUD:
    
    @staticmethod
    def create_attendance(attendance_data: AttendanceCreate):
        """Insert a new attendance record into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[Attendance] 
            (session_id, enrollment_id, status, marked_at, marked_by)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                attendance_data.session_id,
                attendance_data.enrollment_id,
                attendance_data.status,
                attendance_data.marked_at,
                attendance_data.marked_by
            ))
            conn.commit()
            
            # Get the inserted attendance_id
            cursor.execute("SELECT @@IDENTITY")
            attendance_id = cursor.fetchone()[0]
            
            return {"attendance_id": attendance_id, **attendance_data.dict()}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating attendance: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_attendance(attendance_id: int):
        """Retrieve a single attendance record by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT attendance_id, session_id, enrollment_id, status, marked_at, marked_by FROM [dbo].[Attendance] WHERE attendance_id = ?"
            cursor.execute(query, (attendance_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "attendance_id": row[0],
                    "session_id": row[1],
                    "enrollment_id": row[2],
                    "status": row[3],
                    "marked_at": row[4],
                    "marked_by": row[5]
                }
            return None
        
        except Exception as e:
            raise Exception(f"Error retrieving attendance: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_attendance():
        """Retrieve all attendance records"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT attendance_id, session_id, enrollment_id, status, marked_at, marked_by FROM [dbo].[Attendance]"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            attendance_records = []
            for row in rows:
                attendance_records.append({
                    "attendance_id": row[0],
                    "session_id": row[1],
                    "enrollment_id": row[2],
                    "status": row[3],
                    "marked_at": row[4],
                    "marked_by": row[5]
                })
            return attendance_records
        
        except Exception as e:
            raise Exception(f"Error retrieving attendance records: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_attendance_by_session(session_id: int):
        """Retrieve all attendance records for a specific session"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT attendance_id, session_id, enrollment_id, status, marked_at, marked_by FROM [dbo].[Attendance] WHERE session_id = ?"
            cursor.execute(query, (session_id,))
            rows = cursor.fetchall()
            
            attendance_records = []
            for row in rows:
                attendance_records.append({
                    "attendance_id": row[0],
                    "session_id": row[1],
                    "enrollment_id": row[2],
                    "status": row[3],
                    "marked_at": row[4],
                    "marked_by": row[5]
                })
            return attendance_records
        
        except Exception as e:
            raise Exception(f"Error retrieving attendance records: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_attendance_by_enrollment(enrollment_id: int):
        """Retrieve all attendance records for a specific enrollment"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT attendance_id, session_id, enrollment_id, status, marked_at, marked_by FROM [dbo].[Attendance] WHERE enrollment_id = ?"
            cursor.execute(query, (enrollment_id,))
            rows = cursor.fetchall()
            
            attendance_records = []
            for row in rows:
                attendance_records.append({
                    "attendance_id": row[0],
                    "session_id": row[1],
                    "enrollment_id": row[2],
                    "status": row[3],
                    "marked_at": row[4],
                    "marked_by": row[5]
                })
            return attendance_records
        
        except Exception as e:
            raise Exception(f"Error retrieving attendance records: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_attendance(attendance_id: int, attendance_data: AttendanceUpdate):
        """Update an existing attendance record"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if attendance_data.session_id is not None:
                update_fields.append("session_id = ?")
                values.append(attendance_data.session_id)
            if attendance_data.enrollment_id is not None:
                update_fields.append("enrollment_id = ?")
                values.append(attendance_data.enrollment_id)
            if attendance_data.status is not None:
                update_fields.append("status = ?")
                values.append(attendance_data.status)
            if attendance_data.marked_at is not None:
                update_fields.append("marked_at = ?")
                values.append(attendance_data.marked_at)
            if attendance_data.marked_by is not None:
                update_fields.append("marked_by = ?")
                values.append(attendance_data.marked_by)
            
            if not update_fields:
                raise Exception("No fields to update")
            
            values.append(attendance_id)
            
            query = f"UPDATE [dbo].[Attendance] SET {', '.join(update_fields)} WHERE attendance_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Attendance record not found")
            
            return {"message": "Attendance updated successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error updating attendance: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_attendance(attendance_id: int):
        """Delete an attendance record"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "DELETE FROM [dbo].[Attendance] WHERE attendance_id = ?"
            cursor.execute(query, (attendance_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Attendance record not found")
            
            return {"message": "Attendance deleted successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error deleting attendance: {str(e)}")
        finally:
            cursor.close()
            conn.close()
