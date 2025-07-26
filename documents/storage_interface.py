from abc import ABC, abstractmethod
from typing import List, Optional
from .dtos import (
    DocumentDTO, 
    CollaboratorDTO, 
    DocumentVersionDTO,
    CreateDocumentDTO,
    UpdateDocumentDTO,
    AddCollaboratorDTO,
    DocumentListFilterDTO
)


class DocumentStorageInterface(ABC):
    
    @abstractmethod
    def create_document(self, dto: CreateDocumentDTO) -> DocumentDTO:
        pass
    
    @abstractmethod
    def get_document_by_id(self, document_id: int) -> Optional[DocumentDTO]:
        pass
    
    @abstractmethod
    def update_document(self, dto: UpdateDocumentDTO) -> Optional[DocumentDTO]:
        pass
    
    @abstractmethod
    def delete_document(self, document_id: int) -> bool:
        pass
    
    @abstractmethod
    def list_documents(self, filter_dto: DocumentListFilterDTO) -> List[DocumentDTO]:
        pass
    
    @abstractmethod
    def get_documents_by_ids(self, document_ids: List[int]) -> List[DocumentDTO]:
        """Bulk operation to get multiple documents by IDs to avoid N+1 queries"""
        pass
    
    @abstractmethod
    def get_documents_by_owner(self, owner_id: int) -> List[DocumentDTO]:
        pass


class CollaboratorStorageInterface(ABC):
    
    @abstractmethod
    def add_collaborator(self, dto: AddCollaboratorDTO) -> CollaboratorDTO:
        pass
    
    @abstractmethod
    def get_collaborator(self, document_id: int, user_id: int) -> Optional[CollaboratorDTO]:
        pass
    
    @abstractmethod
    def get_document_collaborators(self, document_id: int) -> List[CollaboratorDTO]:
        pass
    
    @abstractmethod
    def update_collaborator_permission(self, document_id: int, user_id: int, permission: str) -> Optional[CollaboratorDTO]:
        pass
    
    @abstractmethod
    def remove_collaborator(self, document_id: int, user_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_user_collaborations(self, user_id: int) -> List[CollaboratorDTO]:
        pass


class DocumentVersionStorageInterface(ABC):
    
    @abstractmethod
    def create_version(self, document_id: int, version_number: int, title: str, content: str, changed_by_user_id: int, change_summary: str) -> DocumentVersionDTO:
        pass
    
    @abstractmethod
    def get_document_versions(self, document_id: int) -> List[DocumentVersionDTO]:
        pass
    
    @abstractmethod
    def get_version_by_number(self, document_id: int, version_number: int) -> Optional[DocumentVersionDTO]:
        pass
    
    @abstractmethod
    def get_latest_version_number(self, document_id: int) -> int:
        pass
    
    @abstractmethod
    def create_version_auto_increment(self, document_id: int, title: str, content: str, changed_by_user_id: int, change_summary: str = "") -> DocumentVersionDTO:
        """Create version with auto-incremented version number to avoid extra storage call"""
        pass
