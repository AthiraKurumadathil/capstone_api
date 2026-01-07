from fastapi import APIRouter, HTTPException, status
from typing import List
from pydantic import BaseModel, Field
from model.usermodel import User, UserCreate, UserUpdate
from services.usercrud import UserCRUD
import jwt
from datetime import datetime, timedelta
from typing import Optional

# Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ============== REQUEST/RESPONSE MODELS ==============
class LoginRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=150)
    password: str = Field(..., min_length=1)

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
    Create a new user. Requires JWT authentication.
    
    - **org_id**: Organization ID (required)
    - **role_id**: Role ID (required)
    - **email**: Email address (required)
    - **phone**: Phone number (optional)
    - **password_hash**: Hashed password (optional)
    - **active**: User status (required)
    """
    try:
        result = UserCRUD.create_user(user)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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

