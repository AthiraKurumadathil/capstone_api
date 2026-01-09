from utils.database import get_db_connection
from model.enrollmentmodel import EnrollmentCreate, EnrollmentUpdate

class EnrollmentCRUD:
    
    @staticmethod
    def create_enrollment(enrollment_data: EnrollmentCreate):
        """Insert a new enrollment record into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[Enrollments] 
            (org_id, batch_id, student_id, enrolled_on, status)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                enrollment_data.org_id,
                enrollment_data.batch_id,
                enrollment_data.student_id,
                enrollment_data.enrolled_on,
                enrollment_data.status
            ))
            conn.commit()
            
            # Get the inserted enrollment_id
            cursor.execute("SELECT @@IDENTITY")
            enrollment_id = cursor.fetchone()[0]
            
            return {"enrollment_id": enrollment_id, **enrollment_data.dict()}
        
        except Exception as e:
            conn.rollback()
            error_str = str(e)
            
            # Handle UNIQUE KEY constraint violation (error code 23000)
            if "23000" in error_str or "UNIQUE KEY" in error_str or "duplicate key" in error_str.lower():
                raise Exception(f"Student is already enrolled in this batch (enrollment_id: {enrollment_data.student_id}, batch_id: {enrollment_data.batch_id})")
            
            raise Exception(f"Error creating enrollment: {error_str}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_enrollment(enrollment_id: int):
        """Retrieve a single enrollment record by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT enrollment_id, org_id, batch_id, student_id, enrolled_on, status FROM [dbo].[Enrollments] WHERE enrollment_id = ?"
            cursor.execute(query, (enrollment_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "enrollment_id": row[0],
                    "org_id": row[1],
                    "batch_id": row[2],
                    "student_id": row[3],
                    "enrolled_on": row[4],
                    "status": row[5]
                }
            return None
        
        except Exception as e:
            raise Exception(f"Error retrieving enrollment: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_enrollments():
        """Retrieve all enrollment records"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT enrollment_id, org_id, batch_id, student_id, enrolled_on, status FROM [dbo].[Enrollments]"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            enrollments = []
            for row in rows:
                enrollments.append({
                    "enrollment_id": row[0],
                    "org_id": row[1],
                    "batch_id": row[2],
                    "student_id": row[3],
                    "enrolled_on": row[4],
                    "status": row[5]
                })
            return enrollments
        
        except Exception as e:
            raise Exception(f"Error retrieving enrollments: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_enrollments_by_student(student_id: int):
        """Retrieve all enrollments for a specific student"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT enrollment_id, org_id, batch_id, student_id, enrolled_on, status FROM [dbo].[Enrollments] WHERE student_id = ?"
            cursor.execute(query, (student_id,))
            rows = cursor.fetchall()
            
            enrollments = []
            for row in rows:
                enrollments.append({
                    "enrollment_id": row[0],
                    "org_id": row[1],
                    "batch_id": row[2],
                    "student_id": row[3],
                    "enrolled_on": row[4],
                    "status": row[5]
                })
            return enrollments
        
        except Exception as e:
            raise Exception(f"Error retrieving enrollments: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_enrollments_by_batch(batch_id: int):
        """Retrieve all enrollments for a specific batch"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT enrollment_id, org_id, batch_id, student_id, enrolled_on, status FROM [dbo].[Enrollments] WHERE batch_id = ?"
            cursor.execute(query, (batch_id,))
            rows = cursor.fetchall()
            
            enrollments = []
            for row in rows:
                enrollments.append({
                    "enrollment_id": row[0],
                    "org_id": row[1],
                    "batch_id": row[2],
                    "student_id": row[3],
                    "enrolled_on": row[4],
                    "status": row[5]
                })
            return enrollments
        
        except Exception as e:
            raise Exception(f"Error retrieving enrollments: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_enrollments_by_org(org_id: int):
        """Retrieve all enrollments for a specific organization"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT enrollment_id, org_id, batch_id, student_id, enrolled_on, status FROM [dbo].[Enrollments] WHERE org_id = ?"
            cursor.execute(query, (org_id,))
            rows = cursor.fetchall()
            
            enrollments = []
            for row in rows:
                enrollments.append({
                    "enrollment_id": row[0],
                    "org_id": row[1],
                    "batch_id": row[2],
                    "student_id": row[3],
                    "enrolled_on": row[4],
                    "status": row[5]
                })
            return enrollments
        
        except Exception as e:
            raise Exception(f"Error retrieving enrollments: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_enrollment(enrollment_id: int, enrollment_data: EnrollmentUpdate):
        """Update an existing enrollment record"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if enrollment_data.org_id is not None:
                update_fields.append("org_id = ?")
                values.append(enrollment_data.org_id)
            
            if enrollment_data.batch_id is not None:
                update_fields.append("batch_id = ?")
                values.append(enrollment_data.batch_id)
            
            if enrollment_data.student_id is not None:
                update_fields.append("student_id = ?")
                values.append(enrollment_data.student_id)
            
            if enrollment_data.enrolled_on is not None:
                update_fields.append("enrolled_on = ?")
                values.append(enrollment_data.enrolled_on)
            
            if enrollment_data.status is not None:
                update_fields.append("status = ?")
                values.append(enrollment_data.status)
            
            if not update_fields:
                raise Exception("No fields to update")
            
            values.append(enrollment_id)
            
            query = f"UPDATE [dbo].[Enrollments] SET {', '.join(update_fields)} WHERE enrollment_id = ?"
            cursor.execute(query, values)
            
            if cursor.rowcount == 0:
                conn.rollback()
                raise Exception("Enrollment not found")
            
            conn.commit()
            return {"message": "Enrollment updated successfully", "enrollment_id": enrollment_id}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error updating enrollment: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_enrollment(enrollment_id: int):
        """Delete an enrollment record by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "DELETE FROM [dbo].[Enrollments] WHERE enrollment_id = ?"
            cursor.execute(query, (enrollment_id,))
            
            if cursor.rowcount == 0:
                conn.rollback()
                raise Exception("Enrollment not found")
            
            conn.commit()
            return {"message": "Enrollment deleted successfully", "enrollment_id": enrollment_id}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error deleting enrollment: {str(e)}")
        finally:
            cursor.close()
            conn.close()
