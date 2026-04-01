from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    role: str = Field(pattern="^(student|instructor)$", description="Role of the user")

class UserCreate(UserBase):
    password: str = Field(min_length=6, description="Password must be at least 6 characters long")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
