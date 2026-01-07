from utils.database import get_db_connection
from model.paymentmodel import PaymentCreate, PaymentUpdate

class PaymentCRUD:
    
    @staticmethod
    def create_payment(payment_data: PaymentCreate):
        """Insert a new payment into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[Payments] 
            (org_id, invoice_id, payment_date, amount, method, reference_no, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                payment_data.org_id,
                payment_data.invoice_id,
                payment_data.payment_date,
                payment_data.amount,
                payment_data.method,
                payment_data.reference_no,
                payment_data.notes
            ))
            conn.commit()
            
            # Get the inserted payment_id
            cursor.execute("SELECT @@IDENTITY")
            payment_id = cursor.fetchone()[0]
            
            return {"payment_id": payment_id, **payment_data.dict()}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating payment: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_payment(payment_id: int):
        """Retrieve a single payment by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT payment_id, org_id, invoice_id, payment_date, amount, method, reference_no, notes FROM [dbo].[Payments] WHERE payment_id = ?"
            cursor.execute(query, (payment_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "payment_id": row[0],
                    "org_id": row[1],
                    "invoice_id": row[2],
                    "payment_date": row[3],
                    "amount": row[4],
                    "method": row[5],
                    "reference_no": row[6],
                    "notes": row[7]
                }
            return None
        
        except Exception as e:
            raise Exception(f"Error retrieving payment: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_payments():
        """Retrieve all payments"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT payment_id, org_id, invoice_id, payment_date, amount, method, reference_no, notes FROM [dbo].[Payments]"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            payments = []
            for row in rows:
                payments.append({
                    "payment_id": row[0],
                    "org_id": row[1],
                    "invoice_id": row[2],
                    "payment_date": row[3],
                    "amount": row[4],
                    "method": row[5],
                    "reference_no": row[6],
                    "notes": row[7]
                })
            return payments
        
        except Exception as e:
            raise Exception(f"Error retrieving payments: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_payments_by_org(org_id: int):
        """Retrieve all payments for a specific organization"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT payment_id, org_id, invoice_id, payment_date, amount, method, reference_no, notes FROM [dbo].[Payments] WHERE org_id = ?"
            cursor.execute(query, (org_id,))
            rows = cursor.fetchall()
            
            payments = []
            for row in rows:
                payments.append({
                    "payment_id": row[0],
                    "org_id": row[1],
                    "invoice_id": row[2],
                    "payment_date": row[3],
                    "amount": row[4],
                    "method": row[5],
                    "reference_no": row[6],
                    "notes": row[7]
                })
            return payments
        
        except Exception as e:
            raise Exception(f"Error retrieving payments: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_payments_by_invoice(invoice_id: int):
        """Retrieve all payments for a specific invoice"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT payment_id, org_id, invoice_id, payment_date, amount, method, reference_no, notes FROM [dbo].[Payments] WHERE invoice_id = ?"
            cursor.execute(query, (invoice_id,))
            rows = cursor.fetchall()
            
            payments = []
            for row in rows:
                payments.append({
                    "payment_id": row[0],
                    "org_id": row[1],
                    "invoice_id": row[2],
                    "payment_date": row[3],
                    "amount": row[4],
                    "method": row[5],
                    "reference_no": row[6],
                    "notes": row[7]
                })
            return payments
        
        except Exception as e:
            raise Exception(f"Error retrieving payments: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_payment(payment_id: int, payment_data: PaymentUpdate):
        """Update an existing payment"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if payment_data.org_id is not None:
                update_fields.append("org_id = ?")
                values.append(payment_data.org_id)
            if payment_data.invoice_id is not None:
                update_fields.append("invoice_id = ?")
                values.append(payment_data.invoice_id)
            if payment_data.payment_date is not None:
                update_fields.append("payment_date = ?")
                values.append(payment_data.payment_date)
            if payment_data.amount is not None:
                update_fields.append("amount = ?")
                values.append(payment_data.amount)
            if payment_data.method is not None:
                update_fields.append("method = ?")
                values.append(payment_data.method)
            if payment_data.reference_no is not None:
                update_fields.append("reference_no = ?")
                values.append(payment_data.reference_no)
            if payment_data.notes is not None:
                update_fields.append("notes = ?")
                values.append(payment_data.notes)
            
            if not update_fields:
                raise Exception("No fields to update")
            
            values.append(payment_id)
            
            query = f"UPDATE [dbo].[Payments] SET {', '.join(update_fields)} WHERE payment_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Payment not found")
            
            return {"message": "Payment updated successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error updating payment: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_payment(payment_id: int):
        """Delete a payment"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "DELETE FROM [dbo].[Payments] WHERE payment_id = ?"
            cursor.execute(query, (payment_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Payment not found")
            
            return {"message": "Payment deleted successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error deleting payment: {str(e)}")
        finally:
            cursor.close()
            conn.close()
