from utils.database import get_db_connection
from model.usermodel import UserCreate, UserUpdate
from datetime import datetime
import hashlib

class UserCRUD:
    """CRUD operations for Users table"""

    @staticmethod
    def create_user(user_data: UserCreate):
        """Create a new user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if email already exists
            check_query = "SELECT user_id FROM [dbo].[Users] WHERE email = ?"
            cursor.execute(check_query, (user_data.email,))
            if cursor.fetchone():
                raise Exception(f"Email '{user_data.email}' is already registered")
            
            # Hash the password if provided
            hashed_password = None
            if user_data.password_hash:
                hashed_password = hashlib.sha256(user_data.password_hash.encode()).hexdigest()
            
            # Insert the user
            query = """
            INSERT INTO [dbo].[Users] (org_id, role_id, email, phone, password_hash, active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                user_data.org_id,
                user_data.role_id,
                user_data.email,
                user_data.phone,
                hashed_password,
                user_data.active,
                datetime.now()
            ))
            conn.commit()
            
            user_id=None
            # Get the newly inserted user_id
            cursor.execute("SELECT @@IDENTITY")
            user_id = cursor.fetchone()[0]
            
            return {"message": "User created successfully", "user_id": user_id}
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating user: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_user(user_id: int):
        """Retrieve a single user by ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
            SELECT user_id, org_id, role_id, email, phone, password_hash, active, created_at, last_login_at
            FROM [dbo].[Users]
            WHERE user_id = ?
            """
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "user_id": row[0],
                    "org_id": row[1],
                    "role_id": row[2],
                    "email": row[3],
                    "phone": row[4],
                    "password_hash": row[5],
                    "active": row[6],
                    "created_at": row[7],
                    "last_login_at": row[8]
                }
            return None
        except Exception as e:
            raise Exception(f"Error retrieving user: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_users():
        """Retrieve all users"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
            SELECT user_id, org_id, role_id, email, phone, password_hash, active, created_at, last_login_at
            FROM [dbo].[Users]
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            
            users = []
            for row in rows:
                users.append({
                    "user_id": row[0],
                    "org_id": row[1],
                    "role_id": row[2],
                    "email": row[3],
                    "phone": row[4],
                    "password_hash": row[5],
                    "active": row[6],
                    "created_at": row[7],
                    "last_login_at": row[8]
                })
            return users
        except Exception as e:
            raise Exception(f"Error retrieving users: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_users_by_org(org_id: int):
        """Retrieve all users for a specific organization"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
            SELECT user_id, org_id, role_id, email, phone, password_hash, active, created_at, last_login_at
            FROM [dbo].[Users]
            WHERE org_id = ?
            """
            cursor.execute(query, (org_id,))
            rows = cursor.fetchall()
            
            users = []
            for row in rows:
                users.append({
                    "user_id": row[0],
                    "org_id": row[1],
                    "role_id": row[2],
                    "email": row[3],
                    "phone": row[4],
                    "password_hash": row[5],
                    "active": row[6],
                    "created_at": row[7],
                    "last_login_at": row[8]
                })
            return users
        except Exception as e:
            raise Exception(f"Error retrieving users by organization: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_user_by_email(email: str):
        """Retrieve a user by email"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
            SELECT user_id, org_id, role_id, email, phone, password_hash, active, created_at, last_login_at
            FROM [dbo].[Users]
            WHERE email = ?
            """
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "user_id": row[0],
                    "org_id": row[1],
                    "role_id": row[2],
                    "email": row[3],
                    "phone": row[4],
                    "password_hash": row[5],
                    "active": row[6],
                    "created_at": row[7],
                    "last_login_at": row[8]
                }
            return None
        except Exception as e:
            raise Exception(f"Error retrieving user by email: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate):
        """Update an existing user (only provided fields)"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Build dynamic update query
            updates = []
            params = []
            
            if user_data.org_id is not None:
                updates.append("org_id = ?")
                params.append(user_data.org_id)
            if user_data.role_id is not None:
                updates.append("role_id = ?")
                params.append(user_data.role_id)
            if user_data.email is not None:
                updates.append("email = ?")
                params.append(user_data.email)
            if user_data.phone is not None:
                updates.append("phone = ?")
                params.append(user_data.phone)
            if user_data.password_hash is not None:
                updates.append("password_hash = ?")
                params.append(user_data.password_hash)
            if user_data.active is not None:
                updates.append("active = ?")
                params.append(user_data.active)
            
            if not updates:
                return {"message": "No fields to update"}
            
            params.append(user_id)
            query = f"UPDATE [dbo].[Users] SET {', '.join(updates)} WHERE user_id = ?"
            
            cursor.execute(query, params)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("User not found")
            
            return {"message": "User updated successfully"}
        except Exception as e:
            raise Exception(f"Error updating user: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_user(user_id: int):
        """Delete a user"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM [dbo].[Users] WHERE user_id = ?"
            cursor.execute(query, (user_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("User not found")
            
            return {"message": "User deleted successfully"}
        except Exception as e:
            raise Exception(f"Error deleting user: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_last_login(user_id: int):
        """Update last_login_at timestamp for a user"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "UPDATE [dbo].[Users] SET last_login_at = ? WHERE user_id = ?"
            cursor.execute(query, (datetime.now(), user_id))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise Exception("User not found")
            
            return {"message": "Last login updated successfully"}
        except Exception as e:
            raise Exception(f"Error updating last login: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def verify_user_credentials(email: str, password: str):
        """Verify user email and password. Returns user data if valid, None otherwise."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
            SELECT user_id, org_id, role_id, email, phone, password_hash, active, created_at, last_login_at
            FROM [dbo].[Users]
            WHERE email = ?
            """
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            # Hash the provided password using SHA256
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            # Compare hashes
            if row[5] == hashed_password:  # row[5] is password_hash
                return {
                    "user_id": row[0],
                    "org_id": row[1],
                    "role_id": row[2],
                    "email": row[3],
                    "phone": row[4],
                    "active": row[6],
                    "created_at": row[7],
                    "last_login_at": row[8]
                }
            return None
        except Exception as e:
            raise Exception(f"Error verifying user credentials: {str(e)}")
        finally:
            cursor.close()
            conn.close()
