from pydantic import BaseModel, EmailStr, Field, ConfigDict

class SignupRequest(BaseModel):
    name : str = Field(min_length=1, max_length=100)
    email : EmailStr
    password : str = Field(min_length=8, max_length=255)

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    email: EmailStr
    role: str
    is_verified: bool