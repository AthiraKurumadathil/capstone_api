from utils.database import get_db_connection
from model.rolemodel import RoleCreate, RoleUpdate

class RoleCRUD:
    
    @staticmethod
    def create_role(role_data: RoleCreate):
        """Insert a new role into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO [dbo].[Roles] 
            (name)
            VALUES (?)
            """
            cursor.execute(query, (
                role_data.name,
            ))
            conn.commit()
            
            # Get the inserted role_id
            cursor.execute("SELECT @@IDENTITY")
            role_id = cursor.fetchone()[0]
            
            return {"role_id": role_id, **role_data.dict()}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating role: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_role(role_id: int):
        """Retrieve a single role by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT role_id, name FROM [dbo].[Roles] WHERE role_id = ?"
            cursor.execute(query, (role_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "role_id": row[0],
                    "name": row[1]
                }
            return None
        
        except Exception as e:
            raise Exception(f"Error retrieving role: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_roles():
        """Retrieve all roles"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT role_id, name FROM [dbo].[Roles] WHERE role_id != 1"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            roles = []
            for row in rows:
                roles.append({
                    "role_id": row[0],
                    "name": row[1]
                })
            return roles
        
        except Exception as e:
            raise Exception(f"Error retrieving roles: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_roles_by_org(org_id: int):
        """Retrieve all roles"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT role_id, name FROM [dbo].[Roles]"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            roles = []
            for row in rows:
                roles.append({
                    "role_id": row[0],
                    "name": row[1]
                })
            return roles
        
        except Exception as e:
            raise Exception(f"Error retrieving roles: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_role(role_id: int, role_data: RoleUpdate):
        """Update an existing role"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if role_data.name is not None:
                update_fields.append("name = ?")
                values.append(role_data.name)
            
            if not update_fields:
                raise Exception("No fields to update")
            
            values.append(role_id)
            
            query = f"UPDATE [dbo].[Roles] SET {', '.join(update_fields)} WHERE role_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Role not found")
            
            return {"message": "Role updated successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error updating role: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_role(role_id: int):
        """Delete a role"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "DELETE FROM [dbo].[Roles] WHERE role_id = ?"
            cursor.execute(query, (role_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("Role not found")
            
            return {"message": "Role deleted successfully"}
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error deleting role: {str(e)}")
        finally:
            cursor.close()
            conn.close()
