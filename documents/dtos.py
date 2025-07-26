from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class DocumentDTO:
    id: Optional[int] = None
    title: str = ""
    content: str = ""
    owner_id: int = 0
    status: str = ""
    is_public: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CollaboratorDTO:
    id: Optional[int] = None
    document_id: int = 0
    user_id: int = 0
    permission: str = ""
    added_by_user_id: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class DocumentVersionDTO:
    id: Optional[int] = None
    document_id: int = 0
    version_number: int = 0
    title: str = ""
    content: str = ""
    changed_by_user_id: int = 0
    change_summary: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CreateDocumentDTO:
    title: str
    content: str
    owner_id: int
    status: str
    is_public: bool = False


@dataclass
class UpdateDocumentDTO:
    id: int
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    is_public: Optional[bool] = None


@dataclass
class AddCollaboratorDTO:
    document_id: int
    user_id: int
    permission: str
    added_by_user_id: int


@dataclass
class DocumentListFilterDTO:
    owner_id: Optional[int] = None
    user_id: Optional[int] = None
    status: Optional[str] = None
    is_public: Optional[bool] = None
    limit: int = 20
    offset: int = 0
