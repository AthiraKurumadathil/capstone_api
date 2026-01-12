from pydantic import BaseModel, Field
from typing import Optional

class RoleBase(BaseModel):
    org_id: int = Field(..., description="Organization ID")
    name: str = Field(..., min_length=1, max_length=50, description="Role name")

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    org_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=50)

class Role(RoleBase):
    role_id: int

    class Config:
        from_attributes = True
