import jwt
from datetime import datetime, timedelta
from typing import Optional, Tuple
import bcrypt
from config.settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS, BCRYPT_ROUNDS
from src.database.models import User
from src.repositories.user_repository import UserRepository
from src.core.exceptions import AuthenticationError, ValidationError
from config.constants import UserRole
from sqlalchemy.orm import Session

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def hash_password(self, password: str) -> str:
        if not password or len(password) < 6:
            raise ValidationError("Password must be at least 6 characters")
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(BCRYPT_ROUNDS)).decode()

    def verify_password(self, password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())

    def create_user(self, username: str, email: str, password: str, 
                    full_name: str, role: UserRole = UserRole.CASHIER) -> User:
        if not username or len(username) < 3:
            raise ValidationError("Username must be at least 3 characters")
        
        if self.user_repo.get_by_username(username):
            raise ValidationError("Username already exists")
        
        if self.user_repo.get_by_email(email):
            raise ValidationError("Email already exists")
        
        password_hash = self.hash_password(password)
        user = self.user_repo.create(
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            role=role
        )
        return user

    def login(self, username: str, password: str) -> Tuple[User, str]:
        user = self.user_repo.get_by_username(username)
        if not user:
            raise AuthenticationError("Invalid username or password")
        
        if not self.verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid username or password")
        
        if not user.is_active:
            raise AuthenticationError("User account is deactivated")
        
        token = self.generate_token(user)
        return user, token

    def generate_token(self, user: User) -> str:
        payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role.value,
            "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    def verify_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")

    def get_current_user(self, token: str) -> Optional[User]:
        payload = self.verify_token(token)
        user = self.user_repo.get_by_id(payload["user_id"])
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        return user

    def change_password(self, user_id: int, old_password: str, new_password: str) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValidationError("User not found")
        
        if not self.verify_password(old_password, user.password_hash):
            raise AuthenticationError("Current password is incorrect")
        
        new_hash = self.hash_password(new_password)
        return self.user_repo.update(user_id, password_hash=new_hash)

    def check_permission(self, user: User, required_role: UserRole) -> bool:
        return user.role == required_role or user.role == UserRole.ADMIN
