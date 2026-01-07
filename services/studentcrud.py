from utils.database import get_db_connection
from model.studentmodel import StudentCreate, StudentUpdate
from datetime import datetime

class StudentCRUD:
    
    @staticmethod
    def create_student(student_data: StudentCreate):
        """Insert a new student into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[Students] 
            (org_id, first_name, last_name, dob, guardian_name, guardian_phone, guardian_email, notes, active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                student_data.org_id,
                student_data.first_name,
                student_data.last_name,
                student_data.dob,
                student_data.guardian_name,
                student_data.guardian_phone,
                student_data.guardian_email,
                student_data.notes,
                student_data.active if student_data.active is not None else True,
                datetime.now()
            ))
            conn.commit()
            
            # Get the inserted student_id
            cursor.execute("SELECT @@IDENTITY")
            student_id = cursor.fetchone()[0]
            
            return {"student_id": student_id, **student_data.dict(), "created_at": datetime.now()}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating student: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_student(student_id: int):
        """Retrieve a single student by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT student_id, org_id, first_name, last_name, dob, guardian_name, guardian_phone, guardian_email, notes, active, created_at FROM [dbo].[Students] WHERE student_id = ?"
            cursor.execute(query, (student_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "student_id": row[0],
                    "org_id": row[1],
                    "first_name": row[2],
                    "last_name": row[3],
                    "dob": row[4],
                    "guardian_name": row[5],
                    "guardian_phone": row[6],
                    "guardian_email": row[7],
                    "notes": row[8],
                    "active": row[9],
                    "created_at": row[10]
                }
            return None
        
        except Exception as e:
            raise Exception(f"Error retrieving student: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_students():
        """Retrieve all students"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT student_id, org_id, first_name, last_name, dob, guardian_name, guardian_phone, guardian_email, notes, active, created_at FROM [dbo].[Students]"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            students = []
            for row in rows:
                students.append({
                    "student_id": row[0],
                    "org_id": row[1],
                    "first_name": row[2],
                    "last_name": row[3],
                    "dob": row[4],
                    "guardian_name": row[5],
                    "guardian_phone": row[6],
                    "guardian_email": row[7],
                    "notes": row[8],
                    "active": row[9],
                    "created_at": row[10]
                })
            return students
        
        except Exception as e:
            raise Exception(f"Error retrieving students: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_students_by_org(org_id: int):
        """Retrieve all students for a specific organization"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT student_id, org_id, first_name, last_name, dob, guardian_name, guardian_phone, guardian_email, notes, active, created_at FROM [dbo].[Students] WHERE org_id = ?"
            cursor.execute(query, (org_id,))
            rows = cursor.fetchall()
            
            students = []
            for row in rows:
                students.append({
                    "student_id": row[0],
                    "org_id": row[1],
                    "first_name": row[2],
                    "last_name": row[3],
                    "dob": row[4],
                    "guardian_name": row[5],
                    "guardian_phone": row[6],
                    "guardian_email": row[7],
                    "notes": row[8],
                    "active": row[9],
                    "created_at": row[10]
                })
            return students
        
        except Exception as e:
            raise Exception(f"Error retrieving students: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_student(student_id: int, student_data: StudentUpdate):
        """Update an existing student"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if student_data.org_id is not None:
                update_fields.append("org_id = ?")
                values.append(student_data.org_id)
            if student_data.first_name is not None:
                update_fields.append("first_name = ?")
                values.append(student_data.first_name)
            if student_data.last_name is not None:
                update_fields.append("last_name = ?")
                values.append(student_data.last_name)
            if student_data.dob is not None:
                update_fields.append("dob = ?")
                values.append(student_data.dob)
            if student_data.guardian_name is not None:
                update_fields.append("guardian_name = ?")
                values.append(student_data.guardian_name)
            if student_data.guardian_phone is not None:
                update_fields.append("guardian_phone = ?")
                values.append(student_data.guardian_phone)
            if student_data.guardian_email is not None:
                update_fields.append("guardian_email = ?")
                values.append(student_data.guardian_email)
            if student_data.notes is not None:
                update_fields.append("notes = ?")
                values.append(student_data.notes)
            if student_data.active is not None:
                update_fields.append("active = ?")
                values.append(student_data.active)
            
            if not update_fields:
                raise Exception("No fields to update")
            
            values.append(student_id)
            
            query = f"UPDATE [dbo].[Students] SET {', '.join(update_fields)} WHERE student_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Student not found")
            
            return {"message": "Student updated successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error updating student: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_student(student_id: int):
        """Delete a student"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "DELETE FROM [dbo].[Students] WHERE student_id = ?"
            cursor.execute(query, (student_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Student not found")
            
            return {"message": "Student deleted successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error deleting student: {str(e)}")
        finally:
            cursor.close()
            conn.close()
