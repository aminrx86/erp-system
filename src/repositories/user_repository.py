from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.database.models import User
from src.repositories.base_repository import BaseRepository
from src.core.exceptions import DatabaseError
from config.constants import UserRole

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_username(self, username: str) -> Optional[User]:
        try:
            return self.db.query(User).filter(User.username == username).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve user: {str(e)}")

    def get_by_email(self, email: str) -> Optional[User]:
        try:
            return self.db.query(User).filter(User.email == email).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve user: {str(e)}")

    def get_active_users(self, skip: int = 0, limit: int = 100) -> list:
        try:
            return self.db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve active users: {str(e)}")

    def get_by_role(self, role: UserRole) -> list:
        try:
            return self.db.query(User).filter(User.role == role).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve users by role: {str(e)}")

    def deactivate_user(self, user_id: int) -> Optional[User]:
        return self.update(user_id, is_active=False)

    def activate_user(self, user_id: int) -> Optional[User]:
        return self.update(user_id, is_active=True)
