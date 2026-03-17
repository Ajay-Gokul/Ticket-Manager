from uuid import UUID
from sqlalchemy.orm import Session
from app.models.db_models import User
from app.models.schemas import UserCreate
from app.services.auth_service import AuthService

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_name(self, name: str) -> User | None:
        return self.db.query(User).filter(User.Name == name).first()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.Email == email).first()

    def get_user_by_uid(self, uid: UUID) -> User | None:
        return self.db.query(User).filter(User.UID == uid).first()

    def create_user(self, user_in: UserCreate, role_uid: UUID) -> User:
        hashed_password = AuthService.get_password_hash(user_in.Password)
        db_user = User(
            Name=user_in.Name,
            Email=user_in.Email,
            PasswordHash=hashed_password,
            RoleUID=role_uid
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
