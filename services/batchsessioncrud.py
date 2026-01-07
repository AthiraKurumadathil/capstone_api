from utils.database import get_db_connection
from model.batchsessionmodel import BatchSessionCreate, BatchSessionUpdate

class BatchSessionCRUD:
    
    @staticmethod
    def create_batch_session(batch_session_data: BatchSessionCreate):
        """Insert a new batch session into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[BatchSessions] 
            (batch_id, session_date, start_time, end_time, status, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                batch_session_data.batch_id,
                batch_session_data.session_date,
                batch_session_data.start_time,
                batch_session_data.end_time,
                batch_session_data.status,
                batch_session_data.notes
            ))
            conn.commit()
            
            # Get the inserted session_id
            cursor.execute("SELECT @@IDENTITY")
            session_id = cursor.fetchone()[0]
            
            return {"session_id": session_id, **batch_session_data.dict()}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating batch session: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_batch_session(session_id: int):
        """Retrieve a single batch session by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT session_id, batch_id, session_date, start_time, end_time, status, notes FROM [dbo].[BatchSessions] WHERE session_id = ?"
            cursor.execute(query, (session_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "session_id": row[0],
                    "batch_id": row[1],
                    "session_date": row[2],
                    "start_time": row[3],
                    "end_time": row[4],
                    "status": row[5],
                    "notes": row[6]
                }
            return None
        
        except Exception as e:
            raise Exception(f"Error retrieving batch session: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_batch_sessions():
        """Retrieve all batch sessions"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT session_id, batch_id, session_date, start_time, end_time, status, notes FROM [dbo].[BatchSessions]"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            batch_sessions = []
            for row in rows:
                batch_sessions.append({
                    "session_id": row[0],
                    "batch_id": row[1],
                    "session_date": row[2],
                    "start_time": row[3],
                    "end_time": row[4],
                    "status": row[5],
                    "notes": row[6]
                })
            return batch_sessions
        
        except Exception as e:
            raise Exception(f"Error retrieving batch sessions: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_sessions_by_batch(batch_id: int):
        """Retrieve all sessions for a specific batch"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT session_id, batch_id, session_date, start_time, end_time, status, notes FROM [dbo].[BatchSessions] WHERE batch_id = ?"
            cursor.execute(query, (batch_id,))
            rows = cursor.fetchall()
            
            batch_sessions = []
            for row in rows:
                batch_sessions.append({
                    "session_id": row[0],
                    "batch_id": row[1],
                    "session_date": row[2],
                    "start_time": row[3],
                    "end_time": row[4],
                    "status": row[5],
                    "notes": row[6]
                })
            return batch_sessions
        
        except Exception as e:
            raise Exception(f"Error retrieving batch sessions: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_batch_session(session_id: int, batch_session_data: BatchSessionUpdate):
        """Update an existing batch session"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if batch_session_data.batch_id is not None:
                update_fields.append("batch_id = ?")
                values.append(batch_session_data.batch_id)
            if batch_session_data.session_date is not None:
                update_fields.append("session_date = ?")
                values.append(batch_session_data.session_date)
            if batch_session_data.start_time is not None:
                update_fields.append("start_time = ?")
                values.append(batch_session_data.start_time)
            if batch_session_data.end_time is not None:
                update_fields.append("end_time = ?")
                values.append(batch_session_data.end_time)
            if batch_session_data.status is not None:
                update_fields.append("status = ?")
                values.append(batch_session_data.status)
            if batch_session_data.notes is not None:
                update_fields.append("notes = ?")
                values.append(batch_session_data.notes)
            
            if not update_fields:
                raise Exception("No fields to update")
            
            values.append(session_id)
            
            query = f"UPDATE [dbo].[BatchSessions] SET {', '.join(update_fields)} WHERE session_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Batch session not found")
            
            return {"message": "Batch session updated successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error updating batch session: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_batch_session(session_id: int):
        """Delete a batch session"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "DELETE FROM [dbo].[BatchSessions] WHERE session_id = ?"
            cursor.execute(query, (session_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Batch session not found")
            
            return {"message": "Batch session deleted successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error deleting batch session: {str(e)}")
        finally:
            cursor.close()
            conn.close()
