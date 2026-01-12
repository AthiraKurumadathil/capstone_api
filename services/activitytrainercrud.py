from utils.database import get_db_connection
from model.activitytrainermodel import ActivityTrainerCreate, ActivityTrainerUpdate

class ActivityTrainerCRUD:
    
    @staticmethod
    def create_activity_trainer(activity_trainer_data: ActivityTrainerCreate):
        """Insert a new activity-trainer relationship into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[ActivityTrainers] 
            (activity_id, trainer_id, role)
            VALUES (?, ?, ?)
            """
            cursor.execute(query, (
                activity_trainer_data.activity_id,
                activity_trainer_data.trainer_id,
                activity_trainer_data.role
            ))
            conn.commit()
            
            return {"activity_id": activity_trainer_data.activity_id, "trainer_id": activity_trainer_data.trainer_id, "role": activity_trainer_data.role}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating activity trainer: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_activity_trainer(activity_id: int, trainer_id: int):
        """Retrieve a specific activity-trainer relationship"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT activity_id, trainer_id, role FROM [dbo].[ActivityTrainers] WHERE activity_id = ? AND trainer_id = ?"
            cursor.execute(query, (activity_id, trainer_id))
            row = cursor.fetchone()
            
            if row:
                return {
                    "activity_id": row[0],
                    "trainer_id": row[1],
                    "role": row[2]
                }
            return None
        
        except Exception as e:
            raise Exception(f"Error retrieving activity trainer: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_activity_trainers():
        """Retrieve all activity-trainer relationships"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT activity_id, trainer_id, role FROM [dbo].[ActivityTrainers]"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            activity_trainers = []
            for row in rows:
                activity_trainers.append({
                    "activity_id": row[0],
                    "trainer_id": row[1],
                    "role": row[2]
                })
            return activity_trainers
        
        except Exception as e:
            raise Exception(f"Error retrieving activity trainers: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_trainers_by_activity(activity_id: int):
        """Retrieve all trainers assigned to a specific activity"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT activity_id, trainer_id, role FROM [dbo].[ActivityTrainers] WHERE activity_id = ?"
            cursor.execute(query, (activity_id,))
            rows = cursor.fetchall()
            
            activity_trainers = []
            for row in rows:
                activity_trainers.append({
                    "activity_id": row[0],
                    "trainer_id": row[1],
                    "role": row[2]
                })
            return activity_trainers
        
        except Exception as e:
            raise Exception(f"Error retrieving trainers for activity: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_activities_by_trainer(trainer_id: int):
        """Retrieve all activities assigned to a specific trainer"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT activity_id, trainer_id, role FROM [dbo].[ActivityTrainers] WHERE trainer_id = ?"
            cursor.execute(query, (trainer_id,))
            rows = cursor.fetchall()
            
            activity_trainers = []
            for row in rows:
                activity_trainers.append({
                    "activity_id": row[0],
                    "trainer_id": row[1],
                    "role": row[2]
                })
            return activity_trainers
        
        except Exception as e:
            raise Exception(f"Error retrieving activities for trainer: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_activity_trainer(activity_id: int, trainer_id: int, activity_trainer_data: ActivityTrainerUpdate):
        """Update an existing activity-trainer relationship"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if activity_trainer_data.role is not None:
                update_fields.append("role = ?")
                values.append(activity_trainer_data.role)
            
            if not update_fields:
                raise Exception("No fields to update")
            
            values.extend([activity_id, trainer_id])
            
            query = f"UPDATE [dbo].[ActivityTrainers] SET {', '.join(update_fields)} WHERE activity_id = ? AND trainer_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Activity trainer relationship not found")
            
            return {"message": "Activity trainer updated successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error updating activity trainer: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_activity_trainer(activity_id: int, trainer_id: int):
        """Delete an activity-trainer relationship"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "DELETE FROM [dbo].[ActivityTrainers] WHERE activity_id = ? AND trainer_id = ?"
            cursor.execute(query, (activity_id, trainer_id))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Activity trainer relationship not found")
            
            return {"message": "Activity trainer deleted successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error deleting activity trainer: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def get_activity_trainers_by_org(org_id: int):
        """Retrieve all activity trainers for a specific organization by joining ActivityTrainers with Activities"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            SELECT at.activity_id, at.trainer_id, at.role, t.first_name, t.last_name, a.name AS activity_name
            FROM [dbo].[ActivityTrainers] at
            INNER JOIN [dbo].[Activities] a ON at.activity_id = a.activity_id
            INNER JOIN [dbo].[Trainers] t ON at.trainer_id = t.trainer_id
            WHERE a.org_id = ?
            """
            cursor.execute(query, (org_id,))
            rows = cursor.fetchall()
            
            activity_trainers = []
            for row in rows:
                activity_trainers.append({
                    "activity_id": row[0],
                    "trainer_id": row[1],
                    "role": row[2],
                    "trainer_first_name": row[3],
                    "trainer_last_name": row[4],
                    "activity_name": row[5]
                })
            return activity_trainers
        
        except Exception as e:
            raise Exception(f"Error retrieving activity trainers for organization: {str(e)}")
        finally:
            cursor.close()
            conn.close()