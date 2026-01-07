from utils.database import get_db_connection
from model.invoicemodel import InvoiceCreate, InvoiceUpdate

class InvoiceCRUD:
    
    @staticmethod
    def create_invoice(invoice_data: InvoiceCreate):
        """Insert a new invoice into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[Invoices] 
            (org_id, enrollment_id, invoice_date, due_date, total_amount, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                invoice_data.org_id,
                invoice_data.enrollment_id,
                invoice_data.invoice_date,
                invoice_data.due_date,
                invoice_data.total_amount,
                invoice_data.status
            ))
            conn.commit()
            
            # Get the inserted invoice_id
            cursor.execute("SELECT @@IDENTITY")
            invoice_id = cursor.fetchone()[0]
            
            return {"invoice_id": invoice_id, **invoice_data.dict()}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating invoice: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_invoice(invoice_id: int):
        """Retrieve a single invoice by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT invoice_id, org_id, enrollment_id, invoice_date, due_date, total_amount, status FROM [dbo].[Invoices] WHERE invoice_id = ?"
            cursor.execute(query, (invoice_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "invoice_id": row[0],
                    "org_id": row[1],
                    "enrollment_id": row[2],
                    "invoice_date": row[3],
                    "due_date": row[4],
                    "total_amount": row[5],
                    "status": row[6]
                }
            return None
        
        except Exception as e:
            raise Exception(f"Error retrieving invoice: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_invoices():
        """Retrieve all invoices"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT invoice_id, org_id, enrollment_id, invoice_date, due_date, total_amount, status FROM [dbo].[Invoices]"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            invoices = []
            for row in rows:
                invoices.append({
                    "invoice_id": row[0],
                    "org_id": row[1],
                    "enrollment_id": row[2],
                    "invoice_date": row[3],
                    "due_date": row[4],
                    "total_amount": row[5],
                    "status": row[6]
                })
            return invoices
        
        except Exception as e:
            raise Exception(f"Error retrieving invoices: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_invoices_by_org(org_id: int):
        """Retrieve all invoices for a specific organization"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT invoice_id, org_id, enrollment_id, invoice_date, due_date, total_amount, status FROM [dbo].[Invoices] WHERE org_id = ?"
            cursor.execute(query, (org_id,))
            rows = cursor.fetchall()
            
            invoices = []
            for row in rows:
                invoices.append({
                    "invoice_id": row[0],
                    "org_id": row[1],
                    "enrollment_id": row[2],
                    "invoice_date": row[3],
                    "due_date": row[4],
                    "total_amount": row[5],
                    "status": row[6]
                })
            return invoices
        
        except Exception as e:
            raise Exception(f"Error retrieving invoices: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_invoices_by_enrollment(enrollment_id: int):
        """Retrieve all invoices for a specific enrollment"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT invoice_id, org_id, enrollment_id, invoice_date, due_date, total_amount, status FROM [dbo].[Invoices] WHERE enrollment_id = ?"
            cursor.execute(query, (enrollment_id,))
            rows = cursor.fetchall()
            
            invoices = []
            for row in rows:
                invoices.append({
                    "invoice_id": row[0],
                    "org_id": row[1],
                    "enrollment_id": row[2],
                    "invoice_date": row[3],
                    "due_date": row[4],
                    "total_amount": row[5],
                    "status": row[6]
                })
            return invoices
        
        except Exception as e:
            raise Exception(f"Error retrieving invoices: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_invoice(invoice_id: int, invoice_data: InvoiceUpdate):
        """Update an existing invoice"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if invoice_data.org_id is not None:
                update_fields.append("org_id = ?")
                values.append(invoice_data.org_id)
            if invoice_data.enrollment_id is not None:
                update_fields.append("enrollment_id = ?")
                values.append(invoice_data.enrollment_id)
            if invoice_data.invoice_date is not None:
                update_fields.append("invoice_date = ?")
                values.append(invoice_data.invoice_date)
            if invoice_data.due_date is not None:
                update_fields.append("due_date = ?")
                values.append(invoice_data.due_date)
            if invoice_data.total_amount is not None:
                update_fields.append("total_amount = ?")
                values.append(invoice_data.total_amount)
            if invoice_data.status is not None:
                update_fields.append("status = ?")
                values.append(invoice_data.status)
            
            if not update_fields:
                raise Exception("No fields to update")
            
            values.append(invoice_id)
            
            query = f"UPDATE [dbo].[Invoices] SET {', '.join(update_fields)} WHERE invoice_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Invoice not found")
            
            return {"message": "Invoice updated successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error updating invoice: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_invoice(invoice_id: int):
        """Delete an invoice"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "DELETE FROM [dbo].[Invoices] WHERE invoice_id = ?"
            cursor.execute(query, (invoice_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Invoice not found")
            
            return {"message": "Invoice deleted successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error deleting invoice: {str(e)}")
        finally:
            cursor.close()
            conn.close()
