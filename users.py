from fastapi import APIRouter, HTTPException, status
from typing import List
from pydantic import BaseModel, Field, field_validator
from model.usermodel import User, UserCreate, UserUpdate
from services.usercrud import UserCRUD
from utils.validation_helper import ValidationHelper
import jwt
from datetime import datetime, timedelta
from typing import Optional

# Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ============== REQUEST/RESPONSE MODELS ==============
class LoginRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=150, description="Email address")
    password: str = Field(..., min_length=1, description="Password")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format"""
        is_valid, error_msg = ValidationHelper.is_valid_email(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., min_length=1, description="Current password")
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")

class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=150, description="Email address")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format"""
        is_valid, error_msg = ValidationHelper.is_valid_email(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user_id: int
    email: str

router = APIRouter(prefix="/users", tags=["users"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Create a new user with auto-generated password.
    
    - **org_id**: Organization ID (required)
    - **role_id**: Role ID (required)
    - **email**: Email address (required)
    - **phone**: Phone number (optional)
    - **active**: User status (required)
    
    A random 12-character password will be generated, hashed with SHA256, 
    and sent to the user's email. User must change password on first login.
    """
    try:
        result = UserCRUD.create_user(user)
        return result
    except Exception as e:
        error_msg = str(e)
        # Check if it's a duplicate email error
        if "already registered" in error_msg:
            raise HTTPException(status_code=409, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)

# ============== GET ENDPOINTS ==============
@router.get("/organization/{org_id}", response_model=List[User])
async def get_users_by_organization(org_id: int):
    """
    Retrieve all users for a specific organization.
    """
    try:
        users = UserCRUD.get_users_by_org(org_id)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/email/{email}", response_model=User)
async def get_user_by_email(email: str):
    """
    Retrieve a user by email address.
    """
    try:
        user = UserCRUD.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[User])
async def get_all_users():
    """
    Retrieve all users.
    """
    try:
        users = UserCRUD.get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """
    Retrieve a single user by ID.
    """
    try:
        user = UserCRUD.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: int, user: UserUpdate):
    """
    Update an existing user.
    
    - **user_id**: User ID (required in URL)
    - All other fields are optional
    """
    try:
        result = UserCRUD.update_user(user_id, user)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== UPDATE LAST LOGIN ==============
@router.put("/{user_id}/last-login", response_model=dict)
async def update_last_login(user_id: int):
    """
    Update the last login timestamp for a user.
    """
    try:
        result = UserCRUD.update_last_login(user_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{user_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_user(user_id: int):
    """
    Delete a user by ID.
    """
    try:
        result = UserCRUD.delete_user(user_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

# ============== FORGOT PASSWORD ENDPOINT ==============
@router.post("/forgot-password", response_model=dict)
async def forgot_password(request: ForgotPasswordRequest):
    """
    Forgot password - send temporary password to email.
    
    Validates that the email exists in the user table before sending reset email.
    
    - **email**: User email address (required)
    
    A temporary password will be generated and sent to the email address.
    User can then use this password to log in and change it immediately.
    """
    try:
        # Check if email exists in the user table
        if not UserCRUD.email_exists(request.email):
            raise HTTPException(
                status_code=404,
                detail="User with this email address not found"
            )
        
        result = UserCRUD.forgot_password(request.email)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== CHANGE PASSWORD ENDPOINT ==============
@router.put("/change-password/{email}", response_model=dict)
async def change_password(email: str, change_password_data: ChangePasswordRequest):
    """
    Change user password using email. Requires correct old password.
    
    - **email**: User email address (required in URL)
    - **old_password**: Current password in plain text (required)
    - **new_password**: New password in plain text (minimum 8 characters) (required)
    """
    try:
        result = UserCRUD.change_password(email, change_password_data.old_password, change_password_data.new_password)
        return result
    except HTTPException:
        raise
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        if "incorrect" in str(e).lower() or "invalid" in str(e).lower():
            raise HTTPException(status_code=401, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== AUTHENTICATION ENDPOINT ==============
@router.post("/authenticate/login", response_model=TokenResponse)
async def authenticate_user(login_data: LoginRequest):
    """
    Authenticate user with email and password. Returns JWT token if credentials are valid.
    
    - **email**: User email address (required)
    - **password**: User password in plain text (will be hashed and compared with SHA256) (required)
    """
    try:
        # Verify credentials
        user = UserCRUD.verify_user_credentials(login_data.email, login_data.password)
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        if not user['active']:
            raise HTTPException(status_code=403, detail="User account is inactive")
        
        # Create JWT token
        expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "user_id": user['user_id'],
            "email": user['email'],
            "org_id": user['org_id'],
            "role_id": user['role_id'],
            "role_name": user.get('role_name'),
            "exp": expiration_time,
            "iat": datetime.utcnow()
        }
        
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        
        # Update last login timestamp
        UserCRUD.update_last_login(user['user_id'])
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # in seconds
            "user_id": user['user_id'],
            "email": user['email']
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")

