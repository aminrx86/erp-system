# 🏢 ERP System - Professional Accounting + POS + Inventory

A production-grade Python desktop ERP system rebuilt from scratch, inspired by Hesabdar but architecturally superior, cleaner, and fully professional.

## 🎯 System Overview

A complete **Point of Sale (POS)**, **Inventory Management**, and **Accounting** system built with:

- **Python 3.13+**
- **PyQt6** - Desktop UI
- **SQLAlchemy** - ORM
- **PostgreSQL/SQLite** - Database
- **JWT** - Authentication
- **Bcrypt** - Password security

---

## 📦 Core Modules

### 1. **Authentication System**
- User login with JWT tokens
- Role-based access control (Admin, Manager, Cashier, Accountant)
- Password hashing with bcrypt
- Session management

### 2. **Product Management**
- Add/Edit/Delete products
- Category management
- Price tracking (purchase & sale)
- Stock management

### 3. **Inventory System**
- Real-time stock tracking
- Inventory logs with audit trail
- Stock validation (no negative stock)
- Low stock alerts
- Adjustment support

### 4. **POS System** (CORE)
- Fast product search
- Shopping cart
- Quick checkout
- Multiple payment methods
- Receipt generation

### 5. **Sales System**
- Complete sales history
- Sale details with items
- Cashier tracking
- Transaction reporting

### 6. **Reporting System**
- Daily sales reports
- Monthly revenue analysis
- Top products
- Inventory status

### 7. **Dashboard**
- Real-time sales metrics
- Today's revenue
- Low stock alerts
- Quick statistics

---

## 🏗️ Architecture

### Strict Layered Architecture

```
┌─────────────────────────────┐
│   UI Layer (PyQt6)          │  ← User Interface
├─────────────────────────────┤
│   Service Layer             │  ← Business Logic
├─────────────────────────────┤
│   Repository Layer          │  ← Data Access
├─────────────────────────────┤
│   Database Layer (SQLAlchemy)│  ← Persistence
└─────────────────────────────┘
```

**Rules:**
- ✅ UI contains NO business logic
- ✅ Services contain ALL business rules
- ✅ Repositories handle ONLY DB operations
- ✅ No direct DB access from UI

---

## 📁 Project Structure

```
erp-system/
├── config/                    # Configuration files
│   ├── settings.py           # App settings
│   ├── database.py           # DB setup
│   └── constants.py          # Enums & constants
├── src/
│   ├── core/                 # Core functionality
│   │   ├── exceptions.py     # Custom exceptions
│   │   └── decorators.py     # Auth decorators
│   ├── database/             # Database layer
│   │   └── models.py         # SQLAlchemy models
│   ├── services/             # Business logic
│   │   ├── auth_service.py
│   │   ├── product_service.py
│   │   ├── inventory_service.py
│   │   ├── pos_service.py
│   │   ├── sales_service.py
│   │   └── receipt_service.py
│   ├── repositories/         # Data access
│   │   ├── base_repository.py
│   │   ├── user_repository.py
│   │   ├── product_repository.py
│   │   ├── inventory_repository.py
│   │   └── sales_repository.py
│   ├── ui/                   # PyQt6 interface
│   └── utils/                # Utilities
├── tests/                     # Unit tests
├── requirements.txt
├── pyproject.toml
├── setup.py
└── main.py
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- pip or poetry

### Installation

1. **Clone repository**
```bash
git clone https://github.com/aminrx86/erp-system.git
cd erp-system
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Initialize database**
```bash
python main.py
```

---

## 🔐 Authentication

### Login

```python
from config.database import SessionLocal
from src.services.auth_service import AuthService

db = SessionLocal()
auth_service = AuthService(db)

# Login
user, token = auth_service.login("cashier1", "password123")
print(f"Welcome {user.full_name}!")
```

### Create User

```python
from config.constants import UserRole

user = auth_service.create_user(
    username="cashier1",
    email="cashier1@shop.com",
    password="secure_password",
    full_name="John Doe",
    role=UserRole.CASHIER
)
```

---

## 📦 Product Management

### Create Product

```python
from src.services.product_service import ProductService

product_service = ProductService(db)

product = product_service.create_product(
    name="iPhone 15",
    sku="APP-IP15-001",
    category_id=1,
    purchase_price=700.0,
    sale_price=999.0,
    description="Latest iPhone model",
    min_stock=5
)
```

### Search Products

```python
# Search by keyword
products = product_service.search_products("iPhone", skip=0, limit=20)

# Get by category
products = product_service.get_products_by_category(category_id=1)

# Get low stock
low_stock = product_service.get_low_stock_products(threshold=10)
```

---

## 📊 Inventory Management

### Increase Stock

```python
from src.services.inventory_service import InventoryService

inventory_service = InventoryService(db)

log = inventory_service.increase_stock(
    product_id=1,
    quantity=50,
    created_by_id=1,
    notes="Purchase order #PO-001"
)
```

### Decrease Stock

```python
log = inventory_service.decrease_stock(
    product_id=1,
    quantity=5,
    created_by_id=1,
    notes="Manual adjustment"
)
```

### Get History

```python
history = inventory_service.get_inventory_history(product_id=1, limit=50)
for log in history:
    print(f"{log.action}: {log.quantity_change} units")
```

---

## 🛒 POS System

### Add to Cart

```python
from src.services.pos_service import POSService

pos_service = POSService(db)

# Add products to cart
pos_service.add_to_cart(product_id=1, quantity=2)
pos_service.add_to_cart(product_id=5, quantity=1)

# View cart
cart = pos_service.get_cart()
print(f"Total items: {cart['total_items']}")
print(f"Subtotal: ${cart['subtotal']:.2f}")
```

### Checkout

```python
from config.constants import PaymentMethod

sale = pos_service.checkout(
    cashier_id=1,
    payment_method=PaymentMethod.CASH,
    discount=10.0,
    tax=5.0,
    notes="Customer: John Smith"
)

print(f"Sale #{sale.sale_number}")
print(f"Total: ${sale.total:.2f}")
```

---

## 📈 Sales Reporting

### Get Sale Details

```python
from src.services.sales_service import SalesService

sales_service = SalesService(db)

# Get sale by ID
sale = sales_service.get_sale(sale_id=1)
details = sales_service.get_sale_details(sale_id=1)

# Get cashier sales
cashier_sales = sales_service.get_cashier_sales(cashier_id=1, limit=50)
```

### Daily Summary

```python
from datetime import datetime

summary = sales_service.get_daily_summary(datetime.utcnow())
print(f"Date: {summary['date']}")
print(f"Total Sales: {summary['total_sales']}")
print(f"Revenue: ${summary['total_revenue']:.2f}")
print(f"Discount: ${summary['total_discount']:.2f}")
```

### Top Products

```python
top_products = sales_service.get_top_products(limit=10, days=30)
for product in top_products:
    print(f"{product['product_name']}: {product['total_quantity']} units")
```

---

## 🧪 Testing

Run unit tests:

```bash
pytest tests/ -v
pytest tests/ --cov=src  # With coverage
```

---

## 📋 Database Models

### User
- `id` - Primary key
- `username` - Unique username
- `email` - User email
- `password_hash` - Hashed password
- `full_name` - Display name
- `role` - User role (Admin/Manager/Cashier/Accountant)
- `is_active` - Active status

### Product
- `id` - Primary key
- `name` - Product name
- `sku` - Unique identifier
- `category_id` - Category reference
- `purchase_price` - Cost price
- `sale_price` - Retail price
- `current_stock` - Current inventory
- `min_stock` - Reorder point
- `is_active` - Active status

### Sale
- `id` - Primary key
- `sale_number` - Unique sale number
- `cashier_id` - Cashier reference
- `subtotal` - Before discount
- `discount` - Discount amount
- `tax` - Tax amount
- `total` - Final total
- `payment_method` - Payment type
- `status` - Sale status

### InventoryLog
- `id` - Primary key
- `product_id` - Product reference
- `action` - Increase/Decrease/Adjustment
- `quantity_change` - Change amount
- `quantity_before` - Stock before
- `quantity_after` - Stock after
- `created_by_id` - User who made change
- `created_at` - Timestamp

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
DB_TYPE=sqlite
DB_SQLITE_PATH=data/erp.db
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
LOG_LEVEL=INFO
CURRENCY=USD
```

---

## 🔒 Security Best Practices

✅ Passwords hashed with bcrypt (12 rounds)
✅ JWT token-based authentication
✅ Role-based access control
✅ Input validation on all operations
✅ SQL injection protection (SQLAlchemy ORM)
✅ Atomic transactions for critical operations

---

## 📚 Development Phases

- ✅ **Phase 1** - Backend Core (Complete)
  - Authentication system
  - Services & Repositories
  - Database models
  - Business logic

- ⏳ **Phase 2** - Database Migrations
- ⏳ **Phase 3** - Inventory + Products refinement
- ⏳ **Phase 4** - POS System completion
- ⏳ **Phase 5** - Receipt generation
- ⏳ **Phase 6** - PyQt6 UI
- ⏳ **Phase 7** - Integration testing
- ⏳ **Phase 8** - Production deployment

---

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/feature-name`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/feature-name`
4. Submit pull request

---

## 📝 License

MIT License - See LICENSE file for details

---

## 👥 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for professional accounting and POS management**

### 🎯 Next Phase: PyQt6 Desktop UI

Stay tuned for Phase 6 where we'll build the complete desktop interface with:
- Modern PyQt6 design
- Real-time dashboard
- Fast cashier workflow
- Intuitive navigation
