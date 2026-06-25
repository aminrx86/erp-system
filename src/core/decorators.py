from functools import wraps
from typing import Callable, Any
from src.core.exceptions import AuthenticationError, AuthorizationError
from config.constants import UserRole

def require_auth(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        current_user = kwargs.get("current_user")
        if not current_user:
            raise AuthenticationError("Authentication required")
        return func(*args, **kwargs)
    return wrapper

def require_role(*roles: UserRole) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_user = kwargs.get("current_user")
            if not current_user:
                raise AuthenticationError("Authentication required")
            if current_user.role not in roles:
                raise AuthorizationError(
                    f"User role {current_user.role} not authorized for this operation"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator
