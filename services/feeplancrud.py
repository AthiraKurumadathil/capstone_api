from utils.database import get_db_connection
from model.feeplanmodel import FeePlanCreate, FeePlanUpdate

class FeePlanCRUD:
    
    @staticmethod
    def create_fee_plan(fee_plan_data: FeePlanCreate):
        """Insert a new fee plan into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[FeePlans] 
            (org_id, name, billing_type_id, amount, currency, active)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                fee_plan_data.org_id,
                fee_plan_data.name,
                fee_plan_data.billing_type_id,
                fee_plan_data.amount,
                fee_plan_data.currency,
                fee_plan_data.active
            ))
            conn.commit()
            
            # Get the inserted fee_plan_id
            cursor.execute("SELECT @@IDENTITY")
            fee_plan_id = cursor.fetchone()[0]
            
            return {"fee_plan_id": fee_plan_id, **fee_plan_data.dict()}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating fee plan: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_fee_plan(fee_plan_id: int):
        """Retrieve a single fee plan by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT fee_plan_id, org_id, name, billing_type_id, amount, currency, active FROM [dbo].[FeePlans] WHERE fee_plan_id = ?"
            cursor.execute(query, (fee_plan_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "fee_plan_id": row[0],
                    "org_id": row[1],
                    "name": row[2],
                    "billing_type_id": row[3],
                    "amount": row[4],
                    "currency": row[5],
                    "active": row[6]
                }
            return None
        
        except Exception as e:
            raise Exception(f"Error retrieving fee plan: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_fee_plans():
        """Retrieve all fee plans"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT fee_plan_id, org_id, name, billing_type_id, amount, currency, active FROM [dbo].[FeePlans]"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            fee_plans = []
            for row in rows:
                fee_plans.append({
                    "fee_plan_id": row[0],
                    "org_id": row[1],
                    "name": row[2],
                    "billing_type_id": row[3],
                    "amount": row[4],
                    "currency": row[5],
                    "active": row[6]
                })
            return fee_plans
        
        except Exception as e:
            raise Exception(f"Error retrieving fee plans: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_fee_plans_by_org(org_id: int):
        """Retrieve all fee plans for a specific organization"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT fee_plan_id, org_id, name, billing_type_id, amount, currency, active FROM [dbo].[FeePlans] WHERE org_id = ?"
            cursor.execute(query, (org_id,))
            rows = cursor.fetchall()
            
            fee_plans = []
            for row in rows:
                fee_plans.append({
                    "fee_plan_id": row[0],
                    "org_id": row[1],
                    "name": row[2],
                    "billing_type_id": row[3],
                    "amount": row[4],
                    "currency": row[5],
                    "active": row[6]
                })
            return fee_plans
        
        except Exception as e:
            raise Exception(f"Error retrieving fee plans: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_fee_plan(fee_plan_id: int, fee_plan_data: FeePlanUpdate):
        """Update an existing fee plan"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if fee_plan_data.org_id is not None:
                update_fields.append("org_id = ?")
                values.append(fee_plan_data.org_id)
            if fee_plan_data.name is not None:
                update_fields.append("name = ?")
                values.append(fee_plan_data.name)
            if fee_plan_data.billing_type_id is not None:
                update_fields.append("billing_type_id = ?")
                values.append(fee_plan_data.billing_type_id)
            if fee_plan_data.amount is not None:
                update_fields.append("amount = ?")
                values.append(fee_plan_data.amount)
            if fee_plan_data.currency is not None:
                update_fields.append("currency = ?")
                values.append(fee_plan_data.currency)
            if fee_plan_data.active is not None:
                update_fields.append("active = ?")
                values.append(fee_plan_data.active)
            
            if not update_fields:
                raise Exception("No fields to update")
            
            values.append(fee_plan_id)
            
            query = f"UPDATE [dbo].[FeePlans] SET {', '.join(update_fields)} WHERE fee_plan_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Fee plan not found")
            
            return {"message": "Fee plan updated successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error updating fee plan: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_fee_plan(fee_plan_id: int):
        """Delete a fee plan"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "DELETE FROM [dbo].[FeePlans] WHERE fee_plan_id = ?"
            cursor.execute(query, (fee_plan_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Fee plan not found")
            
            return {"message": "Fee plan deleted successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error deleting fee plan: {str(e)}")
        finally:
            cursor.close()
            conn.close()
