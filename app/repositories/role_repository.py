from sqlalchemy.orm import Session
from app.models.db_models import Role

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_role_by_name(self, name: str) -> Role | None:
        return self.db.query(Role).filter(Role.Name == name).first()
