from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.models import Product, Category
from src.repositories.product_repository import ProductRepository, CategoryRepository
from src.core.exceptions import ValidationError, ProductNotFoundError
from config.constants import UserRole

class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.product_repo = ProductRepository(db)
        self.category_repo = CategoryRepository(db)

    def create_product(self, name: str, sku: str, category_id: int,
                       purchase_price: float, sale_price: float,
                       description: str = None, min_stock: int = 10) -> Product:
        if not name or len(name) < 2:
            raise ValidationError("Product name must be at least 2 characters")
        
        if not sku or len(sku) < 2:
            raise ValidationError("SKU must be at least 2 characters")
        
        if self.product_repo.get_by_sku(sku):
            raise ValidationError("SKU already exists")
        
        if purchase_price < 0 or sale_price < 0:
            raise ValidationError("Prices cannot be negative")
        
        if sale_price <= purchase_price:
            raise ValidationError("Sale price must be greater than purchase price")
        
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise ValidationError("Category not found")
        
        product = self.product_repo.create(
            name=name,
            sku=sku,
            category_id=category_id,
            purchase_price=purchase_price,
            sale_price=sale_price,
            description=description,
            min_stock=min_stock
        )
        return product

    def get_product(self, product_id: int) -> Product:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError("Product not found")
        return product

    def get_product_by_sku(self, sku: str) -> Product:
        product = self.product_repo.get_by_sku(sku)
        if not product:
            raise ProductNotFoundError("Product not found")
        return product

    def search_products(self, keyword: str, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.product_repo.search_products(keyword, skip, limit)

    def get_products_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise ValidationError("Category not found")
        return self.product_repo.get_by_category(category_id, skip, limit)

    def get_all_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.product_repo.get_active_products(skip, limit)

    def update_product(self, product_id: int, **kwargs) -> Product:
        product = self.get_product(product_id)
        
        if "sku" in kwargs and kwargs["sku"] != product.sku:
            if self.product_repo.get_by_sku(kwargs["sku"]):
                raise ValidationError("SKU already exists")
        
        if "sale_price" in kwargs and "purchase_price" in kwargs:
            if kwargs["sale_price"] <= kwargs["purchase_price"]:
                raise ValidationError("Sale price must be greater than purchase price")
        
        updated = self.product_repo.update(product_id, **kwargs)
        return updated

    def deactivate_product(self, product_id: int) -> Product:
        return self.update_product(product_id, is_active=False)

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        return self.product_repo.get_low_stock_products(threshold)

class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repo = CategoryRepository(db)

    def create_category(self, name: str, description: str = None) -> Category:
        if not name or len(name) < 2:
            raise ValidationError("Category name must be at least 2 characters")
        
        if self.category_repo.get_by_name(name):
            raise ValidationError("Category already exists")
        
        return self.category_repo.create(name=name, description=description)

    def get_category(self, category_id: int) -> Category:
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise ValidationError("Category not found")
        return category

    def get_all_categories(self) -> List[Category]:
        return self.category_repo.get_active_categories()

    def update_category(self, category_id: int, **kwargs) -> Category:
        return self.category_repo.update(category_id, **kwargs)

    def delete_category(self, category_id: int) -> bool:
        return self.category_repo.delete(category_id)
