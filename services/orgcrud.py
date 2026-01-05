from utils.database import get_db_connection
from model.orgmodel import OrganizationCreate, OrganizationUpdate
from datetime import datetime

class OrganizationCRUD:
    
    @staticmethod
    def create_organization(org_data: OrganizationCreate):
        """Insert a new organization into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[Organizations] 
            (name, address, city, zip, state, phone, email, active, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                org_data.name,
                org_data.address,
                org_data.city,
                org_data.zip,
                org_data.state,
                org_data.phone,
                org_data.email,
                org_data.active if org_data.active is not None else True,
                datetime.now()
            ))
            conn.commit()
            
            # Get the inserted org_id
            cursor.execute("SELECT @@IDENTITY")
            org_id = cursor.fetchone()[0]
            
            return {"org_id": org_id, **org_data.dict()}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating organization: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_organization(org_id: int):
        """Retrieve a single organization by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT * FROM [dbo].[Organizations] WHERE org_id = ?"
            cursor.execute(query, (org_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            if cursor.description is None:
                return None
            
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        
        except Exception as e:
            raise Exception(f"Error retrieving organization: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_all_organizations():
        """Retrieve all organizations"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT [org_id],[name],[address],[city],[zip],[state],[phone],[email],[active], [created_date] FROM [dbo].[Organizations] ORDER BY org_id"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            if not rows:
                return []
            
            if cursor.description is None:
                return []
            
            columns = [description[0] for description in cursor.description]
            orgs = []
            for row in rows:
                org_dict = dict(zip(columns, row))
               
                orgs.append(org_dict)
            return orgs
        
        except Exception as e:
            raise Exception(f"Error retrieving organizations: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update_organization(org_id: int, org_data: OrganizationUpdate):
        """Update an existing organization"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query
            update_fields = []
            params = []
            
            if org_data.name is not None:
                update_fields.append("name = ?")
                params.append(org_data.name)
            if org_data.address is not None:
                update_fields.append("address = ?")
                params.append(org_data.address)
            if org_data.city is not None:
                update_fields.append("city = ?")
                params.append(org_data.city)
            if org_data.zip is not None:
                update_fields.append("zip = ?")
                params.append(org_data.zip)
            if org_data.state is not None:
                update_fields.append("state = ?")
                params.append(org_data.state)
            if org_data.phone is not None:
                update_fields.append("phone = ?")
                params.append(org_data.phone)
            if org_data.email is not None:
                update_fields.append("email = ?")
                params.append(org_data.email)
            if org_data.active is not None:
                update_fields.append("active = ?")
                params.append(org_data.active)
            
            if not update_fields:
                raise ValueError("No fields to update")
            
            params.append(org_id)
            query = f"UPDATE [dbo].[Organizations] SET {', '.join(update_fields)} WHERE org_id = ?"
            
            cursor.execute(query, params)
            conn.commit()
            
            if cursor.rowcount == 0:
                return None
            
            # Return updated organization
            return OrganizationCRUD.get_organization(org_id)
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error updating organization: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def delete_organization(org_id: int):
        """Delete an organization"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "DELETE FROM [dbo].[Organizations] WHERE org_id = ?"
            cursor.execute(query, (org_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                return False
            return True
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error deleting organization: {str(e)}")
        finally:
            cursor.close()
            conn.close()
