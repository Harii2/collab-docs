"""
Base enum class and common enums for the collaborative document editing platform.
"""
import enum


class BaseEnumClass(enum.Enum):
    """
    Base enum class with name and value being the same and uppercase.
    """
    
    @classmethod
    def choices(cls):
        """Return Django choices format"""
        return [(item.value, item.value) for item in cls]
    
    @classmethod
    def values(cls):
        """Return list of enum values"""
        return [item.value for item in cls]
    
    def __str__(self):
        return self.value


# Common enums that might be used across multiple apps
class StatusType(BaseEnumClass):
    """Common status types"""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"
    DELETED = "DELETED"
