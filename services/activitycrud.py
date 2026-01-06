from utils.database import get_db_connection
from model.activitymodel import ActivityCreate, ActivityUpdate
from datetime import datetime

class ActivityCRUD:
    
    @staticmethod
    def create_activity(activity_data: ActivityCreate):
        """Insert a new activity into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[Activities] 
            (org_id, name, category_id, description, default_fee, active)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                activity_data.org_id,
                activity_data.name,
                activity_data.category_id,
                activity_data.description,
                activity_data.default_fee,
                activity_data.active if activity_data.active is not None else True
            ))
            conn.commit()
            
            # Get the inserted activity_id
            cursor.execute("SELECT @@IDENTITY")
            activity_id = cursor.fetchone()[0]
            
            return {"activity_id": activity_id, **activity_data.dict()}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating activity: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_activity(activity_id: int):
        """Retrieve a single activity by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT activity_id, org_id, name, category_id, description, default_fee, active FROM [dbo].[Activities] WHERE activity_id = ?"
            cursor.execute(query, (activity_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "activity_id": row[0],
                    "org_id": row[1],
                    "name": row[2],
                    "category_id": row[3],
                    "description": row[4],
                    "default_fee": row[5],
                    "active": row[6],
                   
                }
            return None
        
        except Exception as e:
            raise Exception(f"Error retrieving activity: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_activities():
        """Retrieve all activities"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT activity_id, org_id, name, category_id, description, default_fee, active FROM [dbo].[Activities]"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            activities = []
            for row in rows:
                activities.append({
                    "activity_id": row[0],
                    "org_id": row[1],
                    "name": row[2],
                    "category_id": row[3],
                    "description": row[4],
                    "default_fee": row[5],
                    "active": row[6]
                })
            return activities
        
        except Exception as e:
            raise Exception(f"Error retrieving activities: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_activities_by_org(org_id: int):
        """Retrieve all activities for a specific organization"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT activity_id, org_id, name, category_id, description, default_fee, active FROM [dbo].[Activities] WHERE org_id = ?"
            cursor.execute(query, (org_id,))
            rows = cursor.fetchall()
            
            activities = []
            for row in rows:
                activities.append({
                    "activity_id": row[0],
                    "org_id": row[1],
                    "name": row[2],
                    "category_id": row[3],
                    "description": row[4],
                    "default_fee": row[5],
                    "active": row[6]
                })
            return activities
        
        except Exception as e:
            raise Exception(f"Error retrieving activities: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_activity(activity_id: int, activity_data: ActivityUpdate):
        """Update an existing activity"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if activity_data.org_id is not None:
                update_fields.append("org_id = ?")
                values.append(activity_data.org_id)
            if activity_data.name is not None:
                update_fields.append("name = ?")
                values.append(activity_data.name)
            if activity_data.category_id is not None:
                update_fields.append("category_id = ?")
                values.append(activity_data.category_id)
            if activity_data.description is not None:
                update_fields.append("description = ?")
                values.append(activity_data.description)
            if activity_data.default_fee is not None:
                update_fields.append("default_fee = ?")
                values.append(activity_data.default_fee)
            if activity_data.active is not None:
                update_fields.append("active = ?")
                values.append(activity_data.active)
            
            if not update_fields:
                raise Exception("No fields to update")
            
            values.append(activity_id)
            
            query = f"UPDATE [dbo].[Activities] SET {', '.join(update_fields)} WHERE activity_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Activity not found")
            
            return {"message": "Activity updated successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error updating activity: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_activity(activity_id: int):
        """Delete an activity"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "DELETE FROM [dbo].[Activities] WHERE activity_id = ?"
            cursor.execute(query, (activity_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Activity not found")
            
            return {"message": "Activity deleted successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error deleting activity: {str(e)}")
        finally:
            cursor.close()
            conn.close()
