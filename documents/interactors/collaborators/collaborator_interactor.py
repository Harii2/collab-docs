from typing import List, Optional
from documents.storage_interface import DocumentStorageInterface, CollaboratorStorageInterface
from documents.storage import DocumentStorage, CollaboratorStorage
from documents.dtos import (
    DocumentDTO, 
    CollaboratorDTO,
    AddCollaboratorDTO,
    UpdateCollaboratorDTO
)
from documents.enums import PermissionType


class CollaboratorCrudInteractor:
    
    def __init__(
        self, 
        document_storage: DocumentStorageInterface = None,
        collaborator_storage: CollaboratorStorageInterface = None
    ):
        # Initialize storage dependencies internally if not provided
        self.document_storage = document_storage or DocumentStorage()
        self.collaborator_storage = collaborator_storage or CollaboratorStorage()
    
    def add_collaborator(self, dto: AddCollaboratorDTO, requesting_user_id: int) -> Optional[CollaboratorDTO]:
        document = self.document_storage.get_document_by_id(dto.document_id)
        if not document:
            return None
        
        if not self._can_manage_collaborators(document, requesting_user_id):
            return None
        
        existing = self.collaborator_storage.get_collaborator(dto.document_id, dto.user_id)
        if existing:
            return None
        
        return self.collaborator_storage.add_collaborator(dto)
    
    def update_collaborator_permission(self, document_id: int, user_id: int, permission: str, requesting_user_id: int) -> Optional[CollaboratorDTO]:
        document = self.document_storage.get_document_by_id(document_id)
        if not document:
            return None
        
        if not self._can_manage_collaborators(document, requesting_user_id):
            return None
        
        return self.collaborator_storage.update_collaborator_permission(document_id, user_id, permission)
    
    def remove_collaborator(self, document_id: int, user_id: int, requesting_user_id: int) -> bool:
        document = self.document_storage.get_document_by_id(document_id)
        if not document:
            return False
        
        if not self._can_manage_collaborators(document, requesting_user_id):
            return False
        
        return self.collaborator_storage.remove_collaborator(document_id, user_id)
    
    def get_document_collaborators(self, document_id: int, requesting_user_id: int) -> List[CollaboratorDTO]:
        document = self.document_storage.get_document_by_id(document_id)
        if not document:
            return []
        
        if document.owner_id != requesting_user_id:
            collaborator = self.collaborator_storage.get_collaborator(document_id, requesting_user_id)
            if not collaborator:
                return []
        
        return self.collaborator_storage.get_document_collaborators(document_id)
    
    def get_user_collaborations(self, user_id: int) -> List[CollaboratorDTO]:
        return self.collaborator_storage.get_user_collaborations(user_id)
    
    def _can_manage_collaborators(self, document: DocumentDTO, user_id: int) -> bool:
        if document.owner_id == user_id:
            return True
        
        collaborator = self.collaborator_storage.get_collaborator(document.id, user_id)
        if not collaborator:
            return False
        
        return collaborator.permission == PermissionType.ADMIN.value
