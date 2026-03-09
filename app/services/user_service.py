from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.services.auth_service import AuthService
from app.models.schemas import UserCreate, UserLogin, Token
from app.core.exceptions import ConflictException, UnauthorizedException, ServerErrorException

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)

    def register_user(self, user_in: UserCreate):
        if self.user_repo.get_user_by_name(user_in.Name):
            raise ConflictException("Username already registered")
        
        if self.user_repo.get_user_by_email(user_in.Email):
            raise ConflictException("Email already registered")
        
        # Security: Automatically assign 'User' role to everyone registering via API
        user_role = self.role_repo.get_role_by_name("User")
        if not user_role:
            raise ServerErrorException("Default User role not found in database")
            
        return self.user_repo.create_user(user_in, user_role.UID)

    def authenticate_user(self, user_login: UserLogin) -> Token:
        user = self.user_repo.get_user_by_email(user_login.Email)
        
        if not user or not AuthService.verify_password(user_login.Password, user.PasswordHash):
            raise UnauthorizedException("Incorrect email or password")
        
        access_token = AuthService.create_access_token(data={"sub": user.Email})
        return Token(access_token=access_token, token_type="bearer")
