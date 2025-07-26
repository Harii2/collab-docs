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
        # Initialize storage dependencies at class initialization time
        self.document_storage = document_storage if document_storage is not None else DocumentStorage()
        self.collaborator_storage = collaborator_storage if collaborator_storage is not None else CollaboratorStorage()
        self.version_storage = version_storage if version_storage is not None else DocumentVersionStorage()
    
    def create_document(self, dto: CreateDocumentDTO) -> DocumentDTO:
        return self.document_storage.create_document(dto)
    
    def get_document(self, document_id: int, requesting_user_id: int) -> Optional[DocumentDTO]:
        document = self.document_storage.get_document_by_id(document_id)
        if not document:
            return None
        
        # ✅ Inline permission check to avoid additional storage call
        if document.owner_id == requesting_user_id or document.is_public:
            return document
        
        # Only check collaborator if not owner and not public
        collaborator = self.collaborator_storage.get_collaborator(document.id, requesting_user_id)
        if collaborator:
            return document
        
        return None
    
    def update_document(self, dto: UpdateDocumentDTO, requesting_user_id: int) -> Optional[DocumentDTO]:
        document = self.document_storage.get_document_by_id(dto.id)
        if not document:
            return None
        
        # ✅ Inline edit permission check to avoid additional storage call
        if document.owner_id != requesting_user_id:
            collaborator = self.collaborator_storage.get_collaborator(document.id, requesting_user_id)
            if not collaborator or collaborator.permission not in [PermissionType.EDIT.value, PermissionType.ADMIN.value]:
                return None
        
        updated_document = self.document_storage.update_document(dto)
        
        # ✅ Create version only if content actually changed (reduces storage calls)
        if updated_document and (dto.title or dto.content):
            # ✅ Let version storage handle version number internally to avoid extra call
            self.version_storage.create_version_auto_increment(
                document_id=dto.id,
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
        
        # ✅ Inline delete permission check to avoid additional storage call
        if document.owner_id != requesting_user_id:
            collaborator = self.collaborator_storage.get_collaborator(document.id, requesting_user_id)
            if not collaborator or collaborator.permission != PermissionType.ADMIN.value:
                return False
        
        return self.document_storage.delete_document(document_id)
    
    def list_user_documents(self, user_id: int, filter_dto: DocumentListFilterDTO) -> List[DocumentDTO]:
        if filter_dto.owner_id and filter_dto.owner_id != user_id:
            # ✅ Single call to get user collaborations
            collaborations = self.collaborator_storage.get_user_collaborations(user_id)
            
            # ✅ Extract document IDs and use bulk operation instead of loop
            document_ids = [collab.document_id for collab in collaborations]
            if not document_ids:
                return []
            
            # ✅ Single bulk call instead of N individual calls
            accessible_docs = self.document_storage.get_documents_by_ids(document_ids)
            
            # Filter by status if needed
            if filter_dto.status:
                accessible_docs = [doc for doc in accessible_docs if doc.status == filter_dto.status]
            
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
