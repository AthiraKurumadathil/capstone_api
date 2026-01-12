from utils.database import get_db_connection
from model.enrollmentmodel import EnrollmentCreate, EnrollmentUpdate
from utils.email_helper import EmailHelper
import os

class EnrollmentCRUD:
    
    @staticmethod
    def create_enrollment(enrollment_data: EnrollmentCreate):
        """Insert a new enrollment record into the database and send email to guardian"""
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
            
            # Fetch student details including guardian email
            student_query = """
            SELECT first_name, last_name, guardian_name, guardian_email 
            FROM [dbo].[Students] 
            WHERE student_id = ?
            """
            cursor.execute(student_query, (enrollment_data.student_id,))
            student_row = cursor.fetchone()
            
            # Send email to guardian if guardian_email exists
            if student_row and student_row[3]:  # student_row[3] is guardian_email
                try:
                    student_first_name = student_row[0]
                    student_last_name = student_row[1]
                    guardian_name = student_row[2]
                    guardian_email = student_row[3]
                    
                    email_helper = EmailHelper()
                    
                    html_body = f"""
                    <html>
                        <body style="font-family: Arial, sans-serif;">
                            <h2>Enrollment Confirmation</h2>
                            <p>Dear {guardian_name},</p>
                            <p>We are pleased to confirm that your ward <strong>{student_first_name} {student_last_name}</strong> has been successfully enrolled in our program.</p>
                            <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin: 20px 0;">
                                <p><strong>Enrollment Details:</strong></p>
                                <p><strong>Enrollment ID:</strong> <code style="background-color: #e0e0e0; padding: 5px;">{enrollment_id}</code></p>
                                <p><strong>Student Name:</strong> {student_first_name} {student_last_name}</p>
                                <p><strong>Enrollment Date:</strong> {enrollment_data.enrolled_on}</p>
                            </div>
                            <p>Please keep this Enrollment ID for your records as it may be required for future reference.</p>
                            <p>If you have any questions regarding the enrollment, please do not hesitate to contact us.</p>
                            <p>Best regards,<br>System Administration Team</p>
                        </body>
                    </html>
                    """
                    
                    email_helper.send_html_email(
                        recipient_email=guardian_email,
                        subject=f"Enrollment Confirmation - {student_first_name} {student_last_name}",
                        html_body=html_body
                    )
                except Exception as email_error:
                    # Log email error but don't fail enrollment creation
                    print(f"Warning: Could not send enrollment email to {guardian_email}: {str(email_error)}")
            
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
