class ERPException(Exception):
    pass

class AuthenticationError(ERPException):
    pass

class AuthorizationError(ERPException):
    pass

class ValidationError(ERPException):
    pass

class ProductNotFoundError(ERPException):
    pass

class InsufficientStockError(ERPException):
    pass

class SalesError(ERPException):
    pass

class InventoryError(ERPException):
    pass

class PaymentError(ERPException):
    pass

class DatabaseError(ERPException):
    pass
