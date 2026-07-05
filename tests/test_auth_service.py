import pytest
from config.database import SessionLocal, init_db
from src.services.auth_service import AuthService
from src.services.product_service import ProductService, CategoryService
from src.core.exceptions import ValidationError, AuthenticationError
from config.constants import UserRole

@pytest.fixture
def db():
    """Create test database session"""
    init_db()
    db = SessionLocal()
    yield db
    db.close()

class TestAuthService:
    def test_create_user(self, db):
        auth_service = AuthService(db)
        user = auth_service.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            full_name="Test User",
            role=UserRole.CASHIER
        )
        assert user.username == "testuser"
        assert user.is_active

    def test_login(self, db):
        auth_service = AuthService(db)
        auth_service.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            full_name="Test User"
        )
        user, token = auth_service.login("testuser", "password123")
        assert user.username == "testuser"
        assert token is not None

    def test_invalid_login(self, db):
        auth_service = AuthService(db)
        with pytest.raises(AuthenticationError):
            auth_service.login("nonexistent", "password")

    def test_duplicate_username(self, db):
        auth_service = AuthService(db)
        auth_service.create_user(
            username="testuser",
            email="test1@example.com",
            password="password123",
            full_name="Test User"
        )
        with pytest.raises(ValidationError):
            auth_service.create_user(
                username="testuser",
                email="test2@example.com",
                password="password123",
                full_name="Another User"
            )

class TestProductService:
    def test_create_category(self, db):
        category_service = CategoryService(db)
        category = category_service.create_category(
            name="Electronics",
            description="Electronic devices"
        )
        assert category.name == "Electronics"

    def test_create_product(self, db):
        category_service = CategoryService(db)
        product_service = ProductService(db)
        
        category = category_service.create_category("Electronics")
        product = product_service.create_product(
            name="iPhone 15",
            sku="APP-IP15-001",
            category_id=category.id,
            purchase_price=700.0,
            sale_price=999.0
        )
        assert product.name == "iPhone 15"
        assert product.sale_price > product.purchase_price

    def test_invalid_price(self, db):
        category_service = CategoryService(db)
        product_service = ProductService(db)
        
        category = category_service.create_category("Electronics")
        with pytest.raises(ValidationError):
            product_service.create_product(
                name="Invalid Product",
                sku="INV-001",
                category_id=category.id,
                purchase_price=1000.0,
                sale_price=500.0  # Sale price less than purchase price
            )
