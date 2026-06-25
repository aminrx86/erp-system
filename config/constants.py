from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    CASHIER = "cashier"
    ACCOUNTANT = "accountant"

class PermissionType(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"

class TransactionType(str, Enum):
    SALE = "sale"
    PURCHASE = "purchase"
    RETURN = "return"
    ADJUSTMENT = "adjustment"

class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    CHECK = "check"
    TRANSFER = "transfer"

class InventoryAction(str, Enum):
    INCREASE = "increase"
    DECREASE = "decrease"
    ADJUSTMENT = "adjustment"
    RETURN = "return"

class SalesStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    RETURNED = "returned"
    CANCELED = "canceled"
