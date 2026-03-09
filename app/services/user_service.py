from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.models.schemas import UserCreate, UserLogin, Token
from app.core.exceptions import ConflictException, UnauthorizedException

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register_user(self, user_in: UserCreate):
        if self.user_repo.get_user_by_name(user_in.Name):
            raise ConflictException("Username already registered")
        
        if self.user_repo.get_user_by_email(user_in.Email):
            raise ConflictException("Email already registered")
        
        return self.user_repo.create_user(user_in)

    def authenticate_user(self, user_login: UserLogin) -> Token:
        user = self.user_repo.get_user_by_name(user_login.Username)
        
        if not user or not AuthService.verify_password(user_login.Password, user.PasswordHash):
            raise UnauthorizedException("Incorrect username or password")
        
        access_token = AuthService.create_access_token(data={"sub": user.Name})
        return Token(access_token=access_token, token_type="bearer")
