from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from src.database.models import InventoryLog, Product
from src.repositories.base_repository import BaseRepository
from src.core.exceptions import DatabaseError
from config.constants import InventoryAction

class InventoryRepository(BaseRepository[InventoryLog]):
    def __init__(self, db: Session):
        super().__init__(db, InventoryLog)

    def get_by_product(self, product_id: int, skip: int = 0, limit: int = 100) -> List[InventoryLog]:
        try:
            return self.db.query(InventoryLog).filter(
                InventoryLog.product_id == product_id
            ).order_by(InventoryLog.created_at.desc()).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve inventory logs: {str(e)}")

    def get_recent_logs(self, days: int = 30, skip: int = 0, limit: int = 100) -> List[InventoryLog]:
        try:
            date_threshold = datetime.utcnow() - timedelta(days=days)
            return self.db.query(InventoryLog).filter(
                InventoryLog.created_at >= date_threshold
            ).order_by(InventoryLog.created_at.desc()).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve recent logs: {str(e)}")

    def get_by_action(self, action: InventoryAction, skip: int = 0, limit: int = 100) -> List[InventoryLog]:
        try:
            return self.db.query(InventoryLog).filter(
                InventoryLog.action == action
            ).order_by(InventoryLog.created_at.desc()).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve logs by action: {str(e)}")

    def create_log(self, product_id: int, action: InventoryAction, 
                   quantity_change: int, quantity_before: int, 
                   created_by_id: int, notes: str = None) -> InventoryLog:
        try:
            quantity_after = quantity_before + quantity_change
            log = InventoryLog(
                product_id=product_id,
                action=action,
                quantity_change=quantity_change,
                quantity_before=quantity_before,
                quantity_after=quantity_after,
                notes=notes,
                created_by_id=created_by_id
            )
            self.db.add(log)
            self.db.commit()
            self.db.refresh(log)
            return log
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create inventory log: {str(e)}")
