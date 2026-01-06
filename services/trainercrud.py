from utils.database import get_db_connection
from model.trainermodel import TrainerCreate, TrainerUpdate

class TrainerCRUD:
    
    @staticmethod
    def create_trainer(trainer_data: TrainerCreate):
        """Insert a new trainer into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[Trainers] 
            (org_id, first_name, last_name, phone, email, hire_date, active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                trainer_data.org_id,
                trainer_data.first_name,
                trainer_data.last_name,
                trainer_data.phone,
                trainer_data.email,
                trainer_data.hire_date,
                trainer_data.active if trainer_data.active is not None else True
            ))
            conn.commit()
            
            # Get the inserted trainer_id
            cursor.execute("SELECT @@IDENTITY")
            trainer_id = cursor.fetchone()[0]
            
            return {"trainer_id": trainer_id, **trainer_data.dict()}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating trainer: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_trainer(trainer_id: int):
        """Retrieve a single trainer by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT trainer_id, org_id, first_name, last_name, phone, email, hire_date, active FROM [dbo].[Trainers] WHERE trainer_id = ?"
            cursor.execute(query, (trainer_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "trainer_id": row[0],
                    "org_id": row[1],
                    "first_name": row[2],
                    "last_name": row[3],
                    "phone": row[4],
                    "email": row[5],
                    "hire_date": row[6],
                    "active": row[7]
                }
            return None
        
        except Exception as e:
            raise Exception(f"Error retrieving trainer: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_trainers():
        """Retrieve all trainers"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT trainer_id, org_id, first_name, last_name, phone, email, hire_date, active FROM [dbo].[Trainers]"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            trainers = []
            for row in rows:
                trainers.append({
                    "trainer_id": row[0],
                    "org_id": row[1],
                    "first_name": row[2],
                    "last_name": row[3],
                    "phone": row[4],
                    "email": row[5],
                    "hire_date": row[6],
                    "active": row[7]
                })
            return trainers
        
        except Exception as e:
            raise Exception(f"Error retrieving trainers: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_trainers_by_org(org_id: int):
        """Retrieve all trainers for a specific organization"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT trainer_id, org_id, first_name, last_name, phone, email, hire_date, active FROM [dbo].[Trainers] WHERE org_id = ?"
            cursor.execute(query, (org_id,))
            rows = cursor.fetchall()
            
            trainers = []
            for row in rows:
                trainers.append({
                    "trainer_id": row[0],
                    "org_id": row[1],
                    "first_name": row[2],
                    "last_name": row[3],
                    "phone": row[4],
                    "email": row[5],
                    "hire_date": row[6],
                    "active": row[7]
                })
            return trainers
        
        except Exception as e:
            raise Exception(f"Error retrieving trainers: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_trainer(trainer_id: int, trainer_data: TrainerUpdate):
        """Update an existing trainer"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if trainer_data.org_id is not None:
                update_fields.append("org_id = ?")
                values.append(trainer_data.org_id)
            if trainer_data.first_name is not None:
                update_fields.append("first_name = ?")
                values.append(trainer_data.first_name)
            if trainer_data.last_name is not None:
                update_fields.append("last_name = ?")
                values.append(trainer_data.last_name)
            if trainer_data.phone is not None:
                update_fields.append("phone = ?")
                values.append(trainer_data.phone)
            if trainer_data.email is not None:
                update_fields.append("email = ?")
                values.append(trainer_data.email)
            if trainer_data.hire_date is not None:
                update_fields.append("hire_date = ?")
                values.append(trainer_data.hire_date)
            if trainer_data.active is not None:
                update_fields.append("active = ?")
                values.append(trainer_data.active)
            
            if not update_fields:
                raise Exception("No fields to update")
            
            values.append(trainer_id)
            
            query = f"UPDATE [dbo].[Trainers] SET {', '.join(update_fields)} WHERE trainer_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Trainer not found")
            
            return {"message": "Trainer updated successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error updating trainer: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_trainer(trainer_id: int):
        """Delete a trainer"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "DELETE FROM [dbo].[Trainers] WHERE trainer_id = ?"
            cursor.execute(query, (trainer_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Trainer not found")
            
            return {"message": "Trainer deleted successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error deleting trainer: {str(e)}")
        finally:
            cursor.close()
            conn.close()
