from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, MetaData
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.ext.declarative import declarative_base

# Defining schemas as mentioned in SQL Plan
metadata = MetaData(schema="data")
config_metadata = MetaData(schema="config")

Base = declarative_base()

class Role(Base):
    __tablename__ = "Roles"
    __table_args__ = {"schema": "config"}
    
    UID = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    Name = Column(String(50), nullable=False, unique=True)

class Status(Base):
    __tablename__ = "Statuses"
    __table_args__ = {"schema": "config"}
    
    UID = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    Name = Column(String(50), nullable=False, unique=True)

from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "Users"
    __table_args__ = {"schema": "data"}
    
    UID = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    Name = Column(String(100), nullable=False, unique=True)
    Email = Column(String(255), nullable=False, unique=True)
    PasswordHash = Column(String, nullable=False)
    RoleUID = Column(UNIQUEIDENTIFIER, ForeignKey("config.Roles.UID"), nullable=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    role = relationship("Role")

class Ticket(Base):
    __tablename__ = "Tickets"
    __table_args__ = {"schema": "data"}
    
    UID = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    Title = Column(String(255), nullable=False)
    Description = Column(String, nullable=False)
    StatusUID = Column(UNIQUEIDENTIFIER, ForeignKey("config.Statuses.UID"), nullable=False)
    Priority = Column(String(50), nullable=False)
    CreatorUID = Column(UNIQUEIDENTIFIER, ForeignKey("data.Users.UID"), nullable=False)
    AssigneeUID = Column(UNIQUEIDENTIFIER, ForeignKey("data.Users.UID"), nullable=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow, nullable=False)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
