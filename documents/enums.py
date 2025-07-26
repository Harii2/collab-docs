"""
Documents app specific enums.
"""
from common.enums import BaseEnumClass


class PermissionType(BaseEnumClass):
    """
    Permission types for document collaboration
    """
    VIEW = "VIEW"
    EDIT = "EDIT"
    ADMIN = "ADMIN"


class DocumentStatus(BaseEnumClass):
    """
    Document status choices
    """
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class CollaboratorRole(BaseEnumClass):
    """
    Collaborator role choices
    """
    VIEWER = "VIEWER"
    EDITOR = "EDITOR"
    REVIEWER = "REVIEWER"
    ADMIN = "ADMIN"


# Default values
DEFAULT_PERMISSION = PermissionType.VIEW.value
DEFAULT_DOCUMENT_STATUS = DocumentStatus.DRAFT.value
DEFAULT_COLLABORATOR_ROLE = CollaboratorRole.VIEWER.value
