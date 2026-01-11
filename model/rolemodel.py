from pydantic import BaseModel, Field
from typing import Optional

class RoleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Role name")

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)

class Role(RoleBase):
    role_id: int

    class Config:
        from_attributes = True
