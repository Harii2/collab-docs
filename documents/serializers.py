from rest_framework import serializers
from .dtos import DocumentDTO, CollaboratorDTO, DocumentVersionDTO
from .enums import PermissionType, DocumentStatus


class DocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    content = serializers.CharField(allow_blank=True)
    owner_id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(max_length=20)
    is_public = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class CreateDocumentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField(allow_blank=True, default="")
    status = serializers.CharField(max_length=20, default="DRAFT")
    is_public = serializers.BooleanField(default=False)


class UpdateDocumentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    content = serializers.CharField(allow_blank=True, required=False)
    status = serializers.CharField(max_length=20, required=False)
    is_public = serializers.BooleanField(required=False)


class CollaboratorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    document_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    permission = serializers.CharField(max_length=10)
    added_by_user_id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class AddCollaboratorSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    permission = serializers.CharField(max_length=10, default="VIEW")


class UpdateCollaboratorSerializer(serializers.Serializer):
    permission = serializers.CharField(max_length=10)


class DocumentVersionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    document_id = serializers.IntegerField(read_only=True)
    version_number = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255, read_only=True)
    content = serializers.CharField(read_only=True)
    changed_by_user_id = serializers.IntegerField(read_only=True)
    change_summary = serializers.CharField(max_length=500, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
