from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.database.models import Product, Category
from src.repositories.base_repository import BaseRepository
from src.core.exceptions import DatabaseError

class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: Session):
        super().__init__(db, Product)

    def get_by_sku(self, sku: str) -> Optional[Product]:
        try:
            return self.db.query(Product).filter(Product.sku == sku).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve product: {str(e)}")

    def get_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
        try:
            return self.db.query(Product).filter(
                Product.category_id == category_id,
                Product.is_active == True
            ).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve products: {str(e)}")

    def search_products(self, keyword: str, skip: int = 0, limit: int = 100) -> List[Product]:
        try:
            return self.db.query(Product).filter(
                (Product.name.ilike(f"%{keyword}%") | Product.sku.ilike(f"%{keyword}%")),
                Product.is_active == True
            ).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to search products: {str(e)}")

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        try:
            return self.db.query(Product).filter(
                Product.current_stock <= threshold,
                Product.is_active == True
            ).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve low stock products: {str(e)}")

    def get_active_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        try:
            return self.db.query(Product).filter(
                Product.is_active == True
            ).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve active products: {str(e)}")

class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session):
        super().__init__(db, Category)

    def get_by_name(self, name: str) -> Optional[Category]:
        try:
            return self.db.query(Category).filter(Category.name == name).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve category: {str(e)}")

    def get_active_categories(self) -> List[Category]:
        try:
            return self.db.query(Category).filter(Category.is_active == True).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve categories: {str(e)}")
