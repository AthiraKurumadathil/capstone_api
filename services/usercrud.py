from utils.database import get_db_connection
from model.usermodel import UserCreate, UserUpdate
from datetime import datetime
from utils.password_helper import PasswordHelper
from utils.email_helper import EmailHelper
import os

class UserCRUD:
    """CRUD operations for Users table"""

    @staticmethod
    def create_user(user_data: UserCreate):
        """Create a new user with auto-generated password"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if email already exists
            check_query = "SELECT user_id FROM [dbo].[Users] WHERE email = ?"
            cursor.execute(check_query, (user_data.email,))
            if cursor.fetchone():
                raise Exception(f"Email '{user_data.email}' is already registered")
            
            # Generate random password and hash it
            plain_password, hashed_password = PasswordHelper.generate_and_hash_password()
            
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
            
            user_id = None
            # Get the newly inserted user_id
            cursor.execute("SELECT @@IDENTITY")
            user_id = cursor.fetchone()[0]
            
            # Send welcome email with password
            try:
                email_helper = EmailHelper()
                base_app_url = os.getenv("BASE_APP_URL", "http://localhost:3000")
                change_password_link = f"{base_app_url}/users/change-password?email={user_data.email}"
                
                html_body = f"""
                <html>
                    <body style="font-family: Arial, sans-serif;">
                        <h2>Welcome to Our System!</h2>
                        <p>Dear User,</p>
                        <p>Your account has been successfully created. Here are your login credentials:</p>
                        <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p><strong>Email:</strong> {user_data.email}</p>
                            <p><strong>Temporary Password:</strong> <code style="background-color: #e0e0e0; padding: 5px;">{plain_password}</code></p>
                        </div>
                        <p style="color: #d9534f; font-weight: bold;">⚠️ IMPORTANT: Please change this password immediately after your first login for security purposes.</p>
                        <p>You can change your password using the link below:</p>
                        <div style="text-align: center; margin: 20px 0;">
                            <a href="{change_password_link}" style="display: inline-block; background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Change Password</a>
                        </div>
                        <p>Or follow these steps:</p>
                        <ol>
                            <li>Log in with the credentials above</li>
                            <li>Go to <code>{change_password_link}</code></li>
                            <li>Enter your old password and new password</li>
                            <li>Click "Update Password"</li>
                        </ol>
                        <p>If you did not create this account or have any questions, please contact our support team.</p>
                        <p>Best regards,<br>System Administration Team</p>
                    </body>
                </html>
                """
                
                email_helper.send_html_email(
                    recipient_email=user_data.email,
                    subject="Welcome! Your Account Credentials",
                    html_body=html_body
                )
            except Exception as email_error:
                # Log email error but don't fail user creation
                print(f"Warning: Could not send welcome email to {user_data.email}: {str(email_error)}")
            
            return {
                "message": "User created successfully. Welcome email sent with temporary password.",
                "user_id": user_id,
                "email": user_data.email,
                "note": "User must change password on first login"
            }
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
        """Retrieve all users with organization and role names"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
            SELECT u.user_id, u.org_id, u.role_id, u.email, u.phone, u.password_hash, u.active, u.created_at, u.last_login_at,
                   o.name as organization_name, r.name as role_name
            FROM [dbo].[Users] u
            LEFT JOIN [dbo].[Organizations] o ON u.org_id = o.org_id
            LEFT JOIN [dbo].[Roles] r ON u.role_id = r.role_id
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
                    "last_login_at": row[8],
                    "organization_name": row[9],
                    "role_name": row[10]
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
    def email_exists(email: str) -> bool:
        """
        Check if an email exists in the users table.
        
        Args:
            email: Email address to check
        
        Returns:
            True if email exists, False otherwise
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT user_id FROM [dbo].[Users] WHERE email = ?"
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            
            return row is not None
        except Exception as e:
            raise Exception(f"Error checking email existence: {str(e)}")
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
            
            # Verify password using PasswordHelper
            if PasswordHelper.verify_password(password, row[5]):  # row[5] is password_hash
                # Fetch role name
                role_query = "SELECT name FROM [dbo].[Roles] WHERE role_id = ?"
                cursor.execute(role_query, (row[2],))  # row[2] is role_id
                role_row = cursor.fetchone()
                role_name = role_row[0] if role_row else None
                
                return {
                    "user_id": row[0],
                    "org_id": row[1],
                    "role_id": row[2],
                    "role_name": role_name,
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
    @staticmethod
    def change_password(email: str, old_password: str, new_password: str):
        """
        Change user password. Requires correct old password.
        
        Args:
            email: User email address
            old_password: Current password in plain text
            new_password: New password in plain text
        
        Returns:
            Dictionary with success message
        
        Raises:
            Exception: If user not found or old password is incorrect
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Get current password hash and user_id
            query = "SELECT user_id, password_hash FROM [dbo].[Users] WHERE email = ?"
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            
            if not row:
                raise Exception("User not found")
            
            user_id = row[0]
            current_hash = row[1]
            
            # Verify old password
            if not PasswordHelper.verify_password(old_password, current_hash):
                raise Exception("Old password is incorrect")
            
            # Validate new password length
            if len(new_password) < 8:
                raise Exception("New password must be at least 8 characters long")
            
            # Hash new password
            new_hash = PasswordHelper.hash_password(new_password)
            
            # Update password
            update_query = "UPDATE [dbo].[Users] SET password_hash = ? WHERE email = ?"
            cursor.execute(update_query, (new_hash, email))
            conn.commit()
            
            # Send password change notification email
            try:
                email_helper = EmailHelper()
                html_body = f"""
                <html>
                    <body style="font-family: Arial, sans-serif;">
                        <h2>Password Changed Successfully</h2>
                        <p>Dear User,</p>
                        <p>Your password has been successfully changed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.</p>
                        <div style="background-color: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #28a745;">
                            <p><strong style="color: #155724;">✓ Password changed successfully</strong></p>
                        </div>
                        <p>If you did not make this change, please <strong>contact our support team immediately</strong>.</p>
                        <p>Best regards,<br>System Administration Team</p>
                    </body>
                </html>
                """
                
                email_helper.send_html_email(
                    recipient_email=email,
                    subject="Your Password Has Been Changed",
                    html_body=html_body
                )
            except Exception as email_error:
                # Log email error but don't fail password change
                print(f"Warning: Could not send password change notification to {email}: {str(email_error)}")
            
            return {
                "message": "Password changed successfully",
                "email": email,
                "note": "Confirmation email sent to your registered email address"
            }
        
        except Exception as e:
            conn.rollback()
            raise Exception(str(e))
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def forgot_password(email: str):
        """
        Forgot password - generate and send temporary password.
        
        Args:
            email: User email address
        
        Returns:
            Dictionary with success message
        
        Raises:
            Exception: If user not found
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if user exists
            query = "SELECT user_id FROM [dbo].[Users] WHERE email = ?"
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            
            if not row:
                raise Exception("User with this email address not found")
            
            # Generate temporary password
            temp_password, hashed_password = PasswordHelper.generate_and_hash_password()
            
            # Update password in database
            update_query = "UPDATE [dbo].[Users] SET password_hash = ? WHERE email = ?"
            cursor.execute(update_query, (hashed_password, email))
            conn.commit()
            
            # Send password reset email
            try:
                email_helper = EmailHelper()
                base_app_url = os.getenv("BASE_APP_URL", "http://localhost:3000")
                change_password_link = f"{base_app_url}/users/change-password?email={email}"
                
                html_body = f"""
                <html>
                    <body style="font-family: Arial, sans-serif;">
                        <h2>Password Reset Request</h2>
                        <p>Dear User,</p>
                        <p>We received a request to reset your password. Your temporary password is provided below:</p>
                        <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #ffc107;">
                            <p><strong>Temporary Password:</strong></p>
                            <p style="font-size: 16px; font-family: monospace; background-color: #fffacd; padding: 10px; border-radius: 3px;">{temp_password}</p>
                        </div>
                        <p style="color: #d9534f; font-weight: bold;">⚠️ IMPORTANT SECURITY NOTICE:</p>
                        <ul>
                            <li>This temporary password is valid for one-time login only</li>
                            <li>You must change this password immediately after logging in</li>
                            <li>If you did not request this password reset, please ignore this email</li>
                        </ul>
                        <p>To reset your password, follow these steps:</p>
                        <ol>
                            <li>Log in using the temporary password above</li>
                            <li>Click the link below to change your password</li>
                            <li>Enter your new secure password</li>
                        </ol>
                        <div style="text-align: center; margin: 20px 0;">
                            <a href="{change_password_link}" style="display: inline-block; background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Change Password</a>
                        </div>
                        <p>Or visit: <code>{change_password_link}</code></p>
                        <p>If you have any questions or did not request this reset, please contact our support team immediately.</p>
                        <p style="color: #666; font-size: 12px; margin-top: 30px;">
                            This is an automated email. Please do not reply to this message.
                        </p>
                        <p>Best regards,<br>System Administration Team</p>
                    </body>
                </html>
                """
                
                email_helper.send_html_email(
                    recipient_email=email,
                    subject="Password Reset - Temporary Password Provided",
                    html_body=html_body
                )
            except Exception as email_error:
                # Log email error but don't fail password reset
                print(f"Warning: Could not send password reset email to {email}: {str(email_error)}")
            
            return {
                "message": "Password reset email sent successfully",
                "email": email,
                "note": "Check your email for temporary password and password reset link"
            }
        
        except Exception as e:
            conn.rollback()
            raise Exception(str(e))
        finally:
            cursor.close()
            conn.close()
