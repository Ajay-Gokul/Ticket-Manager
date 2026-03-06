from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    Name: str
    Email: EmailStr

class UserCreate(UserBase):
    Password: str
    RoleUID: UUID

class UserLogin(BaseModel):
    Username: str # Name in database
    Password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
