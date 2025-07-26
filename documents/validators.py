"""
Custom validators for the documents app.
"""
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .enums import PermissionType, DocumentStatus, CollaboratorRole


def validate_permission_type(value):
    if value not in PermissionType.values():
        raise ValidationError(
            _('Invalid permission type. Must be one of: %(valid_choices)s'),
            params={'valid_choices': ', '.join(PermissionType.values())},
        )


def validate_document_status(value):
    if value not in DocumentStatus.values():
        raise ValidationError(
            _('Invalid document status. Must be one of: %(valid_choices)s'),
            params={'valid_choices': ', '.join(DocumentStatus.values())},
        )


def validate_collaborator_role(value):
    if value not in CollaboratorRole.values():
        raise ValidationError(
            _('Invalid collaborator role. Must be one of: %(valid_choices)s'),
            params={'valid_choices': ', '.join(CollaboratorRole.values())},
        )


def validate_user_id(value):
    if not isinstance(value, int) or value <= 0:
        raise ValidationError(
            _('User ID must be a positive integer'),
        )


def validate_document_title(value):
    if not value or not value.strip():
        raise ValidationError(
            _('Document title cannot be empty'),
        )
    
    if len(value.strip()) < 3:
        raise ValidationError(
            _('Document title must be at least 3 characters long'),
        )
    
    if len(value) > 255:
        raise ValidationError(
            _('Document title cannot exceed 255 characters'),
        )


def validate_document_content(value):
    pass 
