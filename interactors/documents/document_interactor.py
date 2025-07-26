from typing import List, Optional
from documents.storage_interface import DocumentStorageInterface, CollaboratorStorageInterface, DocumentVersionStorageInterface
from documents.storage import DocumentStorage, CollaboratorStorage, DocumentVersionStorage
from documents.dtos import (
    DocumentDTO, 
    CreateDocumentDTO,
    UpdateDocumentDTO,
    DocumentListFilterDTO
)
from documents.enums import PermissionType


class DocumentCrudInteractor:
    
    def __init__(
        self, 
        document_storage: DocumentStorageInterface = None,
        collaborator_storage: CollaboratorStorageInterface = None,
        version_storage: DocumentVersionStorageInterface = None
    ):
        # Initialize storage dependencies internally if not provided
        self.document_storage = document_storage or DocumentStorage()
        self.collaborator_storage = collaborator_storage or CollaboratorStorage()
        self.version_storage = version_storage or DocumentVersionStorage()
    
    def create_document(self, dto: CreateDocumentDTO) -> DocumentDTO:
        return self.document_storage.create_document(dto)
    
    def get_document(self, document_id: int, requesting_user_id: int) -> Optional[DocumentDTO]:
        document = self.document_storage.get_document_by_id(document_id)
        if not document:
            return None
        
        if not self._can_view_document(document, requesting_user_id):
            return None
        
        return document
    
    def update_document(self, dto: UpdateDocumentDTO, requesting_user_id: int) -> Optional[DocumentDTO]:
        document = self.document_storage.get_document_by_id(dto.id)
        if not document:
            return None
        
        if not self._can_edit_document(document, requesting_user_id):
            return None
        
        updated_document = self.document_storage.update_document(dto)
        
        if updated_document and (dto.title or dto.content):
            next_version = self.version_storage.get_latest_version_number(dto.id) + 1
            self.version_storage.create_version(
                document_id=dto.id,
                version_number=next_version,
                title=updated_document.title,
                content=updated_document.content,
                changed_by_user_id=requesting_user_id,
                change_summary="Document updated"
            )
        
        return updated_document
    
    def delete_document(self, document_id: int, requesting_user_id: int) -> bool:
        document = self.document_storage.get_document_by_id(document_id)
        if not document:
            return False
        
        if not self._can_delete_document(document, requesting_user_id):
            return False
        
        return self.document_storage.delete_document(document_id)
    
    def list_user_documents(self, user_id: int, filter_dto: DocumentListFilterDTO) -> List[DocumentDTO]:
        if filter_dto.owner_id and filter_dto.owner_id != user_id:
            collaborations = self.collaborator_storage.get_user_collaborations(user_id)
            accessible_docs = []
            for collab in collaborations:
                doc = self.document_storage.get_document_by_id(collab.document_id)
                if doc and (not filter_dto.status or doc.status == filter_dto.status):
                    accessible_docs.append(doc)
            return accessible_docs[:filter_dto.limit]
        
        return self.document_storage.list_documents(filter_dto)
    
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
    
    def _can_delete_document(self, document: DocumentDTO, user_id: int) -> bool:
        if document.owner_id == user_id:
            return True
        
        collaborator = self.collaborator_storage.get_collaborator(document.id, user_id)
        if not collaborator:
            return False
        
        return collaborator.permission == PermissionType.ADMIN.value
