from enum import Enum

class UserRole(str, Enum):
    """Valid user roles for Kirikou."""
    ADMIN = "admin"
    READER = "reader"


