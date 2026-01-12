from utils.database import get_db_connection
from model.rolemodel import RoleCreate, RoleUpdate

class RoleCRUD:
    
    @staticmethod
    def create_role(role_data: RoleCreate):
        """Insert a new role into the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if role with same name exists for this organization
            check_query = "SELECT role_id FROM [dbo].[Roles] WHERE org_id = ? AND name = ?"
            cursor.execute(check_query, (role_data.org_id, role_data.name))
            if cursor.fetchone():
                raise Exception(f"Role with name '{role_data.name}' already exists for this organization")
            
            query = """
            INSERT INTO [dbo].[Roles] 
            (org_id, name)
            VALUES (?, ?)
            """
            cursor.execute(query, (
                role_data.org_id,
                role_data.name
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
            query = "SELECT role_id, org_id, name FROM [dbo].[Roles] WHERE role_id = ?"
            cursor.execute(query, (role_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "role_id": row[0],
                    "org_id": row[1],
                    "name": row[2]
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
            query = "SELECT role_id, org_id, name FROM [dbo].[Roles] WHERE role_id != 1"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            roles = []
            for row in rows:
                roles.append({
                    "role_id": row[0],
                    "org_id": row[1],
                    "name": row[2]
                })
            return roles
        
        except Exception as e:
            raise Exception(f"Error retrieving roles: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_roles_by_org(org_id: int):
        """Retrieve all roles for a specific organization"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT role_id, org_id, name FROM [dbo].[Roles] WHERE org_id = ?"
            cursor.execute(query, (org_id,))
            rows = cursor.fetchall()
            
            roles = []
            for row in rows:
                roles.append({
                    "role_id": row[0],
                    "org_id": row[1],
                    "name": row[2]
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
            # Get current role data
            get_role_query = "SELECT org_id, name FROM [dbo].[Roles] WHERE role_id = ?"
            cursor.execute(get_role_query, (role_id,))
            current_role = cursor.fetchone()
            
            if not current_role:
                raise Exception("Role not found")
            
            current_org_id = current_role[0]
            current_name = current_role[1]
            
            # Determine the org_id and name to use for duplicate check
            org_id_to_check = role_data.org_id if role_data.org_id is not None else current_org_id
            name_to_check = role_data.name if role_data.name is not None else current_name
            
            # Check if another role with same name exists for this organization
            if role_data.name is not None:  # Only check if name is being updated
                check_query = "SELECT role_id FROM [dbo].[Roles] WHERE org_id = ? AND name = ? AND role_id != ?"
                cursor.execute(check_query, (org_id_to_check, name_to_check, role_id))
                if cursor.fetchone():
                    raise Exception(f"Role with name '{name_to_check}' already exists for this organization")
            
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            
            if role_data.org_id is not None:
                update_fields.append("org_id = ?")
                values.append(role_data.org_id)
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
