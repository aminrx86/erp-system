from typing import TypeVar, Generic, List, Optional, Type
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.core.exceptions import DatabaseError

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def create(self, **kwargs) -> T:
        try:
            instance = self.model(**kwargs)
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create record: {str(e)}")

    def get_by_id(self, id: int) -> Optional[T]:
        try:
            return self.db.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve record: {str(e)}")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        try:
            return self.db.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve records: {str(e)}")

    def update(self, id: int, **kwargs) -> Optional[T]:
        try:
            instance = self.get_by_id(id)
            if not instance:
                return None
            
            for key, value in kwargs.items():
                setattr(instance, key, value)
            
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to update record: {str(e)}")

    def delete(self, id: int) -> bool:
        try:
            instance = self.get_by_id(id)
            if not instance:
                return False
            
            self.db.delete(instance)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to delete record: {str(e)}")

    def exists(self, **kwargs) -> bool:
        try:
            query = self.db.query(self.model)
            for key, value in kwargs.items():
                query = query.filter(getattr(self.model, key) == value)
            return query.first() is not None
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to check existence: {str(e)}")

    def count(self) -> int:
        try:
            return self.db.query(self.model).count()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to count records: {str(e)}")
