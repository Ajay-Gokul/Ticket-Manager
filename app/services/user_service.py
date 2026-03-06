from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.models.schemas import UserCreate, UserLogin, Token

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register_user(self, user_in: UserCreate):
        # Business logic: Check for duplicates
        if self.user_repo.get_user_by_name(user_in.Name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Username already registered"
            )
        if self.user_repo.get_user_by_email(user_in.Email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email already registered"
            )
        
        # Business logic: Delegate persistence
        return self.user_repo.create_user(user_in)

    def authenticate_user(self, user_login: UserLogin) -> Token:
        # Business logic: Verify identity
        user = self.user_repo.get_user_by_name(user_login.Username)
        
        if not user or not AuthService.verify_password(user_login.Password, user.PasswordHash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Business logic: Generate token
        access_token = AuthService.create_access_token(data={"sub": user.Name})
        return Token(access_token=access_token, token_type="bearer")
