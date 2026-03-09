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

class TicketBase(BaseModel):
    Title: str
    Description: str
    StatusUID: UUID
    Priority: str

class TicketCreate(TicketBase):
    CreatorUID: UUID

class TicketUpdate(BaseModel):
    Title: str | None = None
    Description: str | None = None
    StatusUID: UUID | None = None
    Priority: str | None = None
    AssigneeUID: UUID | None = None

class TicketResponse(TicketBase):
    UID: UUID
    CreatorUID: UUID
    AssigneeUID: UUID | None = None
    CreatedAt: datetime
    UpdatedAt: datetime

    class Config:
        from_attributes = True
