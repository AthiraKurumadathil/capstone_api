from utils.database import get_db_connection
from model.studentmodel import StudentCreate, StudentUpdate
from datetime import datetime
import os
import shutil
from pathlib import Path

class StudentCRUD:
    
    @staticmethod
    def create_student(student_data: StudentCreate):
        """Insert a new student into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[Students] 
            (org_id, first_name, last_name, dob, guardian_name, guardian_phone, guardian_email, student_photo_path, notes, active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                student_data.org_id,
                student_data.first_name,
                student_data.last_name,
                student_data.dob,
                student_data.guardian_name,
                student_data.guardian_phone,
                student_data.guardian_email,
                student_data.student_photo_path,
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
    def create_student_with_photo(org_id: int, first_name: str, last_name: str, 
                                   dob: str = None, guardian_name: str = None, 
                                   guardian_phone: str = None, guardian_email: str = None,
                                   notes: str = None, active: bool = True, 
                                   student_photo = None):
        """Insert a new student with photo upload into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        student_photo_path = None
        
        try:
            # Handle file upload if photo is provided
            if student_photo:
                # Create images directory if it doesn't exist
                base_dir = Path(__file__).parent.parent  # Get the project root directory
                images_dir = base_dir / "images"
                images_dir.mkdir(exist_ok=True)
                
                # Generate unique filename
                file_extension = os.path.splitext(student_photo.filename)[1]
                filename = f"student_{org_id}_{first_name}_{last_name}_{int(datetime.now().timestamp())}{file_extension}"
                filepath = images_dir / filename
                
                # Save the file
                with open(str(filepath), "wb") as f:
                    content = student_photo.file.read()
                    f.write(content)
                
                # Store relative path
                student_photo_path = f"images/{filename}"
            
            query = """
            INSERT INTO [dbo].[Students] 
            (org_id, first_name, last_name, dob, guardian_name, guardian_phone, guardian_email, student_photo_path, notes, active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                org_id,
                first_name,
                last_name,
                dob,
                guardian_name,
                guardian_phone,
                guardian_email,
                student_photo_path,
                notes,
                active if active is not None else True,
                datetime.now()
            ))
            conn.commit()
            
            # Get the inserted student_id
            cursor.execute("SELECT @@IDENTITY")
            student_id = cursor.fetchone()[0]
            
            return {
                "student_id": student_id,
                "org_id": org_id,
                "first_name": first_name,
                "last_name": last_name,
                "dob": dob,
                "guardian_name": guardian_name,
                "guardian_phone": guardian_phone,
                "guardian_email": guardian_email,
                "student_photo_path": student_photo_path,
                "notes": notes,
                "active": active,
                "created_at": datetime.now()
            }
        
        except Exception as e:
            conn.rollback()
            # Delete uploaded file if database insert fails
            if student_photo_path:
                try:
                    base_dir = Path(__file__).parent.parent
                    full_path = base_dir / student_photo_path
                    if full_path.exists():
                        os.remove(str(full_path))
                except:
                    pass
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
            query = "SELECT student_id, org_id, first_name, last_name, dob, guardian_name, guardian_phone, guardian_email, student_photo_path, notes, active, created_at FROM [dbo].[Students] WHERE student_id = ?"
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
                    "student_photo_path": row[8],
                    "notes": row[9],
                    "active": row[10],
                    "created_at": row[11]
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
            query = "SELECT student_id, org_id, first_name, last_name, dob, guardian_name, guardian_phone, guardian_email, student_photo_path, notes, active, created_at FROM [dbo].[Students]"
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
                    "student_photo_path": row[8],
                    "notes": row[9],
                    "active": row[10],
                    "created_at": row[11]
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
            query = "SELECT student_id, org_id, first_name, last_name, dob, guardian_name, guardian_phone, guardian_email, student_photo_path, notes, active, created_at FROM [dbo].[Students] WHERE org_id = ?"
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
                    "student_photo_path": row[8],
                    "notes": row[9],
                    "active": row[10],
                    "created_at": row[11]
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
            if student_data.student_photo_path is not None:
                update_fields.append("student_photo_path = ?")
                values.append(student_data.student_photo_path)
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
