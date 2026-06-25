from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from src.database.models import Sale, SaleItem, Payment
from src.repositories.base_repository import BaseRepository
from src.core.exceptions import DatabaseError
from config.constants import SalesStatus
from sqlalchemy import func

class SalesRepository(BaseRepository[Sale]):
    def __init__(self, db: Session):
        super().__init__(db, Sale)

    def get_by_number(self, sale_number: str) -> Optional[Sale]:
        try:
            return self.db.query(Sale).filter(Sale.sale_number == sale_number).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve sale: {str(e)}")

    def get_by_cashier(self, cashier_id: int, skip: int = 0, limit: int = 100) -> List[Sale]:
        try:
            return self.db.query(Sale).filter(
                Sale.cashier_id == cashier_id
            ).order_by(Sale.created_at.desc()).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve sales: {str(e)}")

    def get_by_date_range(self, start_date: datetime, end_date: datetime, 
                          skip: int = 0, limit: int = 1000) -> List[Sale]:
        try:
            return self.db.query(Sale).filter(
                Sale.created_at >= start_date,
                Sale.created_at <= end_date,
                Sale.status == SalesStatus.COMPLETED
            ).order_by(Sale.created_at.desc()).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve sales: {str(e)}")

    def get_today_sales(self) -> List[Sale]:
        try:
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            return self.get_by_date_range(today_start, today_end)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve today's sales: {str(e)}")

    def get_daily_revenue(self, date: datetime) -> float:
        try:
            start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
            result = self.db.query(func.sum(Sale.total)).filter(
                Sale.created_at >= start,
                Sale.created_at <= end,
                Sale.status == SalesStatus.COMPLETED
            ).scalar()
            return result or 0.0
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to calculate revenue: {str(e)}")

    def get_monthly_revenue(self, year: int, month: int) -> float:
        try:
            start = datetime(year, month, 1)
            if month == 12:
                end = datetime(year + 1, 1, 1)
            else:
                end = datetime(year, month + 1, 1)
            
            result = self.db.query(func.sum(Sale.total)).filter(
                Sale.created_at >= start,
                Sale.created_at < end,
                Sale.status == SalesStatus.COMPLETED
            ).scalar()
            return result or 0.0
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to calculate monthly revenue: {str(e)}")

    def generate_sale_number(self) -> str:
        try:
            count = self.db.query(Sale).count()
            return f"SAL-{datetime.utcnow().strftime('%Y%m%d')}-{count + 1:06d}"
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to generate sale number: {str(e)}")

class SaleItemRepository(BaseRepository[SaleItem]):
    def __init__(self, db: Session):
        super().__init__(db, SaleItem)

    def get_by_sale(self, sale_id: int) -> List[SaleItem]:
        try:
            return self.db.query(SaleItem).filter(SaleItem.sale_id == sale_id).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve sale items: {str(e)}")

class PaymentRepository(BaseRepository[Payment]):
    def __init__(self, db: Session):
        super().__init__(db, Payment)

    def get_by_sale(self, sale_id: int) -> List[Payment]:
        try:
            return self.db.query(Payment).filter(Payment.sale_id == sale_id).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve payments: {str(e)}")
