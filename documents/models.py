"""
Documents app models using AbstractDateTimeCacheModel and AbstractDateTimeModel.
Uses ForeignKey for intra-app relations and IDs for cross-app user references.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from collab_docs.base_models import AbstractDateTimeCacheModel, AbstractDateTimeModel
from .enums import PermissionType, DocumentStatus, DEFAULT_PERMISSION, DEFAULT_DOCUMENT_STATUS
from .validators import (
    validate_permission_type, 
    validate_document_status,
    validate_user_id,
    validate_document_title,
    validate_document_content
)


class Document(AbstractDateTimeCacheModel):

    title = models.CharField(
        max_length=255,
        validators=[validate_document_title]
    )
    content = models.TextField(
        blank=True,
        validators=[validate_document_content]
    )
    owner_id = models.PositiveIntegerField(
        validators=[validate_user_id]
    )
    status = models.CharField(
        max_length=20,
        default=DEFAULT_DOCUMENT_STATUS,
        validators=[validate_document_status]
    )
    is_public = models.BooleanField(
        default=False
    )
    
    class Meta:
        db_table = 'documents_document'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['owner_id']),
            models.Index(fields=['status']),
            models.Index(fields=['is_public']),
        ]
    
    def __str__(self):
        return self.title


class Collaborator(AbstractDateTimeCacheModel):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='collaborators'
    )
    user_id = models.PositiveIntegerField(
        validators=[validate_user_id],
    )
    permission = models.CharField(
        max_length=10,
        default=DEFAULT_PERMISSION,
        validators=[validate_permission_type]
    )
    added_by_user_id = models.PositiveIntegerField(
        validators=[validate_user_id],
    )
    
    class Meta:
        db_table = 'documents_collaborator'
        unique_together = ('document', 'user_id')
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['permission']),
        ]
    
    def __str__(self):
        return f"User {self.user_id} - {self.document.title} ({self.permission})"


class DocumentVersion(AbstractDateTimeCacheModel):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='versions'
    )
    version_number = models.PositiveIntegerField(
    )
    title = models.CharField(
        max_length=255
    )
    content = models.TextField(
        blank=True
    )
    changed_by_user_id = models.PositiveIntegerField(
        validators=[validate_user_id],
    )
    change_summary = models.CharField(
        max_length=500,
        blank=True,
    )
    
    class Meta:
        db_table = 'documents_version'
        unique_together = ('document', 'version_number')
        ordering = ['-version_number']
        indexes = [
            models.Index(fields=['version_number']),
        ]
    
    def __str__(self):
        return f"{self.document_id} v{self.version_number}"
