from utils.database import get_db_connection
from model.batchmodel import BatchCreate, BatchUpdate

class BatchCRUD:
    
    @staticmethod
    def create_batch(batch_data: BatchCreate):
        """Insert a new batch into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[Batches] 
            (org_id, activity_id, fee_plan_id, name, start_date, end_date, capacity, location, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                batch_data.org_id,
                batch_data.activity_id,
                batch_data.fee_plan_id,
                batch_data.name,
                batch_data.start_date,
                batch_data.end_date,
                batch_data.capacity,
                batch_data.location,
                batch_data.status
            ))
            conn.commit()
            
            # Get the inserted batch_id
            cursor.execute("SELECT @@IDENTITY")
            batch_id = cursor.fetchone()[0]
            
            return {"batch_id": batch_id, **batch_data.dict()}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating batch: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_batch(batch_id: int):
        """Retrieve a single batch by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT batch_id, org_id, activity_id, fee_plan_id, name, start_date, end_date, capacity, location, status FROM [dbo].[Batches] WHERE batch_id = ?"
            cursor.execute(query, (batch_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "batch_id": row[0],
                    "org_id": row[1],
                    "activity_id": row[2],
                    "fee_plan_id": row[3],
                    "name": row[4],
                    "start_date": row[5],
                    "end_date": row[6],
                    "capacity": row[7],
                    "location": row[8],
                    "status": row[9]
                }
            return None
        
        except Exception as e:
            raise Exception(f"Error retrieving batch: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_batches():
        """Retrieve all batches"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT batch_id, org_id, activity_id, fee_plan_id, name, start_date, end_date, capacity, location, status FROM [dbo].[Batches]"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            batches = []
            for row in rows:
                batches.append({
                    "batch_id": row[0],
                    "org_id": row[1],
                    "activity_id": row[2],
                    "fee_plan_id": row[3],
                    "name": row[4],
                    "start_date": row[5],
                    "end_date": row[6],
                    "capacity": row[7],
                    "location": row[8],
                    "status": row[9]
                })
            return batches
        
        except Exception as e:
            raise Exception(f"Error retrieving batches: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_batches_by_org(org_id: int):
        """Retrieve all batches for a specific organization"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT batch_id, org_id, activity_id, fee_plan_id, name, start_date, end_date, capacity, location, status FROM [dbo].[Batches] WHERE org_id = ?"
            cursor.execute(query, (org_id,))
            rows = cursor.fetchall()
            
            batches = []
            for row in rows:
                batches.append({
                    "batch_id": row[0],
                    "org_id": row[1],
                    "activity_id": row[2],
                    "fee_plan_id": row[3],
                    "name": row[4],
                    "start_date": row[5],
                    "end_date": row[6],
                    "capacity": row[7],
                    "location": row[8],
                    "status": row[9]
                })
            return batches
        
        except Exception as e:
            raise Exception(f"Error retrieving batches: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_batches_by_activity(activity_id: int):
        """Retrieve all batches for a specific activity"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT batch_id, org_id, activity_id, fee_plan_id, name, start_date, end_date, capacity, location, status FROM [dbo].[Batches] WHERE activity_id = ?"
            cursor.execute(query, (activity_id,))
            rows = cursor.fetchall()
            
            batches = []
            for row in rows:
                batches.append({
                    "batch_id": row[0],
                    "org_id": row[1],
                    "activity_id": row[2],
                    "fee_plan_id": row[3],
                    "name": row[4],
                    "start_date": row[5],
                    "end_date": row[6],
                    "capacity": row[7],
                    "location": row[8],
                    "status": row[9]
                })
            return batches
        
        except Exception as e:
            raise Exception(f"Error retrieving batches: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_batch(batch_id: int, batch_data: BatchUpdate):
        """Update an existing batch"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if batch_data.org_id is not None:
                update_fields.append("org_id = ?")
                values.append(batch_data.org_id)
            if batch_data.activity_id is not None:
                update_fields.append("activity_id = ?")
                values.append(batch_data.activity_id)
            if batch_data.fee_plan_id is not None:
                update_fields.append("fee_plan_id = ?")
                values.append(batch_data.fee_plan_id)
            if batch_data.name is not None:
                update_fields.append("name = ?")
                values.append(batch_data.name)
            if batch_data.start_date is not None:
                update_fields.append("start_date = ?")
                values.append(batch_data.start_date)
            if batch_data.end_date is not None:
                update_fields.append("end_date = ?")
                values.append(batch_data.end_date)
            if batch_data.capacity is not None:
                update_fields.append("capacity = ?")
                values.append(batch_data.capacity)
            if batch_data.location is not None:
                update_fields.append("location = ?")
                values.append(batch_data.location)
            if batch_data.status is not None:
                update_fields.append("status = ?")
                values.append(batch_data.status)
            
            if not update_fields:
                raise Exception("No fields to update")
            
            values.append(batch_id)
            
            query = f"UPDATE [dbo].[Batches] SET {', '.join(update_fields)} WHERE batch_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Batch not found")
            
            return {"message": "Batch updated successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error updating batch: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_batch(batch_id: int):
        """Delete a batch"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "DELETE FROM [dbo].[Batches] WHERE batch_id = ?"
            cursor.execute(query, (batch_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Batch not found")
            
            return {"message": "Batch deleted successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error deleting batch: {str(e)}")
        finally:
            cursor.close()
            conn.close()
