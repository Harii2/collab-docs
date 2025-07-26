from typing import List, Optional
from documents.storage_interface import DocumentStorageInterface, CollaboratorStorageInterface, DocumentVersionStorageInterface
from documents.storage import DocumentStorage, CollaboratorStorage, DocumentVersionStorage
from documents.dtos import (
    DocumentDTO, 
    DocumentVersionDTO
)
from documents.enums import PermissionType


class VersionCrudInteractor:
    
    def __init__(
        self, 
        document_storage: DocumentStorageInterface = None,
        collaborator_storage: CollaboratorStorageInterface = None,
        version_storage: DocumentVersionStorageInterface = None
    ):
        # Initialize storage dependencies at class initialization time
        self.document_storage = document_storage if document_storage is not None else DocumentStorage()
        self.collaborator_storage = collaborator_storage if collaborator_storage is not None else CollaboratorStorage()
        self.version_storage = version_storage if version_storage is not None else DocumentVersionStorage()
    
    def get_document_versions(self, document_id: int, requesting_user_id: int) -> List[DocumentVersionDTO]:
        document = self.document_storage.get_document_by_id(document_id)
        if not document:
            return []
        
        # ✅ Inline view permission check to avoid additional storage call
        if document.owner_id == requesting_user_id or document.is_public:
            return self.version_storage.get_document_versions(document_id)
        
        # Only check collaborator if not owner and not public
        collaborator = self.collaborator_storage.get_collaborator(document.id, requesting_user_id)
        if not collaborator:
            return []
        
        return self.version_storage.get_document_versions(document_id)
    
    def get_version_by_number(self, document_id: int, version_number: int, requesting_user_id: int) -> Optional[DocumentVersionDTO]:
        document = self.document_storage.get_document_by_id(document_id)
        if not document:
            return None
        
        # ✅ Inline view permission check to avoid additional storage call
        if document.owner_id == requesting_user_id or document.is_public:
            return self.version_storage.get_version_by_number(document_id, version_number)
        
        # Only check collaborator if not owner and not public
        collaborator = self.collaborator_storage.get_collaborator(document.id, requesting_user_id)
        if not collaborator:
            return None
        
        return self.version_storage.get_version_by_number(document_id, version_number)
    
    def create_version(self, document_id: int, changed_by_user_id: int, change_summary: str = "") -> Optional[DocumentVersionDTO]:
        document = self.document_storage.get_document_by_id(document_id)
        if not document:
            return None
        
        if not self._can_edit_document(document, changed_by_user_id):
            return None
        
        next_version = self.version_storage.get_latest_version_number(document_id) + 1
        
        return self.version_storage.create_version(
            document_id=document_id,
            version_number=next_version,
            title=document.title,
            content=document.content,
            changed_by_user_id=changed_by_user_id,
            change_summary=change_summary
        )
    
    def _can_view_document(self, document: DocumentDTO, user_id: int) -> bool:
        if document.owner_id == user_id:
            return True
        
        if document.is_public:
            return True
        
        collaborator = self.collaborator_storage.get_collaborator(document.id, user_id)
        return collaborator is not None
    
    def _can_edit_document(self, document: DocumentDTO, user_id: int) -> bool:
        if document.owner_id == user_id:
            return True
        
        collaborator = self.collaborator_storage.get_collaborator(document.id, user_id)
        if not collaborator:
            return False
        
        return collaborator.permission in [PermissionType.EDIT.value, PermissionType.ADMIN.value]
