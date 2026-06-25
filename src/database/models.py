from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, 
    ForeignKey, Enum, Text, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from config.database import Base
from config.constants import (
    UserRole, TransactionType, PaymentMethod, 
    InventoryAction, SalesStatus
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CASHIER, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sales = relationship("Sale", back_populates="cashier")
    inventory_logs = relationship("InventoryLog", back_populates="created_by_user")

    __table_args__ = (
        Index("idx_user_role", "role"),
        Index("idx_user_is_active", "is_active"),
    )

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    purchase_price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=False)
    current_stock = Column(Integer, default=0, nullable=False)
    min_stock = Column(Integer, default=10, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    inventory_logs = relationship("InventoryLog", back_populates="product")
    sale_items = relationship("SaleItem", back_populates="product")

    __table_args__ = (
        Index("idx_product_sku", "sku"),
        Index("idx_product_category_id", "category_id"),
        Index("idx_product_is_active", "is_active"),
    )

class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    action = Column(Enum(InventoryAction), nullable=False)
    quantity_change = Column(Integer, nullable=False)
    quantity_before = Column(Integer, nullable=False)
    quantity_after = Column(Integer, nullable=False)
    notes = Column(Text)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    product = relationship("Product", back_populates="inventory_logs")
    created_by_user = relationship("User", back_populates="inventory_logs")

    __table_args__ = (
        Index("idx_inventory_log_product_id", "product_id"),
        Index("idx_inventory_log_created_at", "created_at"),
    )

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    sale_number = Column(String(50), unique=True, nullable=False, index=True)
    cashier_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    subtotal = Column(Float, default=0, nullable=False)
    discount = Column(Float, default=0, nullable=False)
    tax = Column(Float, default=0, nullable=False)
    total = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(SalesStatus), default=SalesStatus.COMPLETED, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cashier = relationship("User", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="sale")

    __table_args__ = (
        Index("idx_sale_number", "sale_number"),
        Index("idx_sale_cashier_id", "cashier_id"),
        Index("idx_sale_created_at", "created_at"),
        Index("idx_sale_status", "status"),
    )

class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    discount = Column(Float, default=0)
    subtotal = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", back_populates="sale_items")

    __table_args__ = (
        Index("idx_sale_item_sale_id", "sale_id"),
        Index("idx_sale_item_product_id", "product_id"),
    )

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    reference = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    sale = relationship("Sale", back_populates="payments")

    __table_args__ = (
        Index("idx_payment_sale_id", "sale_id"),
        Index("idx_payment_created_at", "created_at"),
    )
