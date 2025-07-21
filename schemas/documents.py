"""
Schémas pour la gestion des documents
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from .common import BaseSchema, TimestampMixin


class DocumentUploadResponse(BaseSchema):
    """Réponse après upload d'un document"""
    id_document: int
    file_path: str
    mime_type: Optional[str]
    size_bytes: Optional[int]
    checksum: Optional[str]
    upload_url: str  # URL signée pour l'upload


class DocumentResponse(BaseSchema, TimestampMixin):
    """Réponse pour un document"""
    id_document: int
    file_path: str
    mime_type: Optional[str]
    size_bytes: Optional[int]
    checksum: Optional[str]
    uploaded_by: Optional[int]
    download_url: Optional[str]  # URL signée pour le téléchargement
    tags: Optional[List["TagDocumentResponse"]] = None


class DocumentMetadata(BaseSchema):
    """Métadonnées d'un document"""
    id_document: int
    mime_type: Optional[str]
    size_bytes: Optional[int]
    signed_url: str  # URL signée pour accès


class AttachTagRequest(BaseModel):
    """Demande d'attachement de tag"""
    tag_ids: List[int] = Field(..., description="IDs des tags à attacher")


class DocumentFilter(BaseModel):
    """Filtres pour les documents"""
    mime_type: Optional[str] = None
    tag_ids: Optional[List[int]] = None
    uploaded_by: Optional[int] = None
    size_min: Optional[int] = None
    size_max: Optional[int] = None


# Import pour éviter les références circulaires
from .referentiels import TagDocumentResponse
DocumentResponse.model_rebuild() 