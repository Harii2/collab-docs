from typing import List, Optional, Tuple

from .dtos import (
    DocumentDTO,
    CollaboratorDTO,
    DocumentVersionDTO,
    CreateDocumentDTO,
    UpdateDocumentDTO,
    AddCollaboratorDTO,
    DocumentListFilterDTO
)
from .models import Document, Collaborator, DocumentVersion
from .storage_interface import DocumentStorageInterface, CollaboratorStorageInterface, DocumentVersionStorageInterface


class DocumentStorage(DocumentStorageInterface):
    
    def create_document(self, dto: CreateDocumentDTO) -> DocumentDTO:
        document = Document.objects.create(
            title=dto.title,
            content=dto.content,
            owner_id=dto.owner_id,
            status=dto.status,
            is_public=dto.is_public
        )
        return self._model_to_dto(document)
    
    def get_document_by_id(self, document_id: int) -> Optional[DocumentDTO]:
        try:
            document = Document.objects.get(pk=document_id)
            return self._model_to_dto(document)
        except Document.DoesNotExist:
            return None
    
    def update_document(self, dto: UpdateDocumentDTO) -> Optional[DocumentDTO]:
        try:
            document = Document.objects.get(id=dto.id)
            if dto.title is not None:
                document.title = dto.title
            if dto.content is not None:
                document.content = dto.content
            if dto.status is not None:
                document.status = dto.status
            if dto.is_public is not None:
                document.is_public = dto.is_public
            document.save()
            return self._model_to_dto(document)
        except Document.DoesNotExist:
            return None
    
    def delete_document(self, document_id: int) -> bool:
        try:
            document = Document.objects.get(id=document_id)
            document.delete()
            return True
        except Document.DoesNotExist:
            return False
    
    def list_documents(self, filter_dto: DocumentListFilterDTO) -> List[DocumentDTO]:
        queryset = Document.objects.cached().all()
        
        if filter_dto.owner_id:
            queryset = queryset.filter(owner_id=filter_dto.owner_id)
        if filter_dto.status:
            queryset = queryset.filter(status=filter_dto.status)
        if filter_dto.is_public is not None:
            queryset = queryset.filter(is_public=filter_dto.is_public)
        
        documents = queryset[filter_dto.offset:filter_dto.offset + filter_dto.limit]
        return [self._to_document_dto(doc) for doc in documents]
    
    def get_documents_by_ids(self, document_ids: List[int]) -> List[DocumentDTO]:
        """Bulk operation to get multiple documents by IDs to avoid N+1 queries"""
        if not document_ids:
            return []
        
        documents = Document.objects.cached().filter(id__in=document_ids)
        return [self._to_document_dto(doc) for doc in documents]
    
    def get_documents_by_owner(self, owner_id: int) -> List[DocumentDTO]:
        documents = Document.objects.filter(owner_id=owner_id)
        return self._bulk_model_to_dto(documents)
    
    @staticmethod
    def _model_to_dto(document: Document) -> DocumentDTO:
        return DocumentDTO(
            id=document.pk,
            title=document.title,
            content=document.content,
            owner_id=document.owner_id,
            status=document.status,
            is_public=document.is_public,
            created_at=document.created_at,
            updated_at=document.updated_at
        )
    
    def _bulk_model_to_dto(self, documents: List[Document]) -> List[DocumentDTO]:
        return [
            self._model_to_dto(document=doc) for doc in documents
        ]


class CollaboratorStorage(CollaboratorStorageInterface):
    
    def add_collaborator(self, dto: AddCollaboratorDTO) -> CollaboratorDTO:
        collaborator = Collaborator.objects.create(
            document_id=dto.document_id,
            user_id=dto.user_id,
            permission=dto.permission,
            added_by_user_id=dto.added_by_user_id
        )
        return self._model_to_dto(collaborator)
    
    def get_collaborator(self, document_id: int, user_id: int) -> Optional[CollaboratorDTO]:
        try:
            collaborator = Collaborator.objects.get(document_id=document_id, user_id=user_id)
            return self._model_to_dto(collaborator)
        except Collaborator.DoesNotExist:
            return None
    
    def get_document_collaborators(self, document_id: int) -> List[CollaboratorDTO]:
        collaborators = Collaborator.objects.filter(document_id=document_id)
        return self._bulk_model_to_dto(collaborators)
    
    def update_collaborator_permission(self, document_id: int, user_id: int, permission: str) -> Optional[CollaboratorDTO]:
        try:
            collaborator = Collaborator.objects.get(document_id=document_id, user_id=user_id)
            collaborator.permission = permission
            collaborator.save()
            return self._model_to_dto(collaborator)
        except Collaborator.DoesNotExist:
            return None
    
    def remove_collaborator(self, document_id: int, user_id: int) -> bool:
        try:
            collaborator = Collaborator.objects.get(document_id=document_id, user_id=user_id)
            collaborator.delete()
            return True
        except Collaborator.DoesNotExist:
            return False
    
    def get_user_collaborations(self, user_id: int) -> List[CollaboratorDTO]:
        collaborators = Collaborator.objects.cached().filter(user_id=user_id)
        return [self._to_collaborator_dto(collab) for collab in collaborators]
    
    @staticmethod
    def _model_to_dto(collaborator: Collaborator) -> CollaboratorDTO:
        return CollaboratorDTO(
            id=collaborator.pk,
            document_id= collaborator.document_id,
            user_id=collaborator.user_id,
            permission=collaborator.permission,
            added_by_user_id=collaborator.added_by_user_id,
            created_at=collaborator.created_at,
            updated_at=collaborator.updated_at
        )
    
    def _bulk_model_to_dto(self, collaborators: List[Collaborator]) -> List[CollaboratorDTO]:
        return [
            self._model_to_dto(
                collaborator=collab
            ) for collab in collaborators
        ]


class DocumentVersionStorage(DocumentVersionStorageInterface):
    
    def create_version(self, document_id: int, version_number: int, title: str, content: str, changed_by_user_id: int, change_summary: str) -> DocumentVersionDTO:
        version = DocumentVersion.objects.create(
            document_id=document_id,
            version_number=version_number,
            title=title,
            content=content,
            changed_by_user_id=changed_by_user_id,
            change_summary=change_summary
        )
        return self._model_to_dto(version)
    
    def get_document_versions(self, document_id: int) -> List[DocumentVersionDTO]:
        versions = DocumentVersion.objects.filter(document_id=document_id)
        return self._bulk_model_to_dto(versions)
    
    def get_version_by_number(self, document_id: int, version_number: int) -> Optional[DocumentVersionDTO]:
        try:
            version = DocumentVersion.objects.get(document_id=document_id, version_number=version_number)
            return self._model_to_dto(version)
        except DocumentVersion.DoesNotExist:
            return None
    
    def get_latest_version_number(self, document_id: int) -> int:
        latest_version = DocumentVersion.objects.cached().filter(document_id=document_id).order_by('-version_number').first()
        return latest_version.version_number if latest_version else 0
    
    def create_version_auto_increment(self, document_id: int, title: str, content: str, changed_by_user_id: int, change_summary: str = "") -> DocumentVersionDTO:
        """Create version with auto-incremented version number to avoid extra storage call"""
        # Get latest version number and increment in single operation
        latest_version_number = self.get_latest_version_number(document_id)
        next_version_number = latest_version_number + 1
        
        # Create new version with auto-incremented number
        version = DocumentVersion.objects.create(
            document_id=document_id,
            version_number=next_version_number,
            title=title,
            content=content,
            changed_by_user_id=changed_by_user_id,
            change_summary=change_summary
        )
        
        return self._model_to_dto(version)
    
    @staticmethod
    def _model_to_dto(version: DocumentVersion) -> DocumentVersionDTO:
        return DocumentVersionDTO(
            id=version.pk,
            document_id=version.document_id,
            version_number=version.version_number,
            title=version.title,
            content=version.content,
            changed_by_user_id=version.changed_by_user_id,
            change_summary=version.change_summary,
            created_at=version.created_at,
            updated_at=version.updated_at
        )
    
    def _bulk_model_to_dto(self, versions: List[DocumentVersion]) -> List[DocumentVersionDTO]:
        return [
            self._model_to_dto(
                version=version
            ) for version in versions
        ]
