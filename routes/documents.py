"""
Routes pour la gestion des documents
"""
import os
import hashlib
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from dependencies import require_authenticated_user, get_current_user_id
from schemas.documents import *
from schemas.common import ResponseMessage
from models.documents import Document
from models.referentiels import TagDocument
from config import settings

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])


@router.post("/", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Upload d'un fichier (multipart/form-data)
    """
    # Vérifier la taille du fichier
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {settings.max_file_size} bytes"
        )
    
    # Calculer le checksum
    checksum = hashlib.md5(file_content).hexdigest()
    
    # Créer le répertoire d'upload s'il n'existe pas
    os.makedirs(settings.upload_dir, exist_ok=True)
    
    # Générer un nom de fichier unique
    filename = f"{checksum}_{file.filename}"
    file_path = os.path.join(settings.upload_dir, filename)
    
    # Sauvegarder le fichier
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    # Créer l'enregistrement en base
    document = Document(
        file_path=file_path,
        mime_type=file.content_type,
        size_bytes=file_size,
        checksum=checksum,
        uploaded_by=current_user_id
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return DocumentUploadResponse(
        id_document=document.id_document,
        file_path=document.file_path,
        mime_type=document.mime_type,
        size_bytes=document.size_bytes,
        checksum=document.checksum,
        upload_url=f"/api/v1/documents/{document.id_document}"
    )


@router.get("/{document_id}", response_model=DocumentMetadata)
async def get_document_metadata(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """
    Métadonnées et URL signée pour un document
    """
    document = db.query(Document).filter(Document.id_document == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # TODO: Générer une URL signée pour l'accès sécurisé
    signed_url = f"/api/v1/documents/{document_id}/download"
    
    return DocumentMetadata(
        id_document=document.id_document,
        mime_type=document.mime_type,
        size_bytes=document.size_bytes,
        signed_url=signed_url
    )


@router.delete("/{document_id}", response_model=ResponseMessage)
async def delete_document(
    document_id: int,
    force: bool = False,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """
    Suppression (soft delete par défaut, hard delete avec ?force=true)
    """
    document = db.query(Document).filter(Document.id_document == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if force:
        # Hard delete - supprimer le fichier et l'enregistrement
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        db.delete(document)
    else:
        # Soft delete - marquer comme supprimé
        # TODO: Ajouter un champ deleted_at dans le modèle
        pass
    
    db.commit()
    
    return ResponseMessage(
        message=f"Document {document_id} deleted successfully",
        success=True
    )


@router.post("/{document_id}/tags", response_model=ResponseMessage)
async def attach_tags(
    document_id: int,
    tag_request: AttachTagRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """
    Attacher des tags à un document
    """
    document = db.query(Document).filter(Document.id_document == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Vérifier que tous les tags existent
    tags = db.query(TagDocument).filter(TagDocument.id_tag.in_(tag_request.tag_ids)).all()
    if len(tags) != len(tag_request.tag_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more tags not found"
        )
    
    # Attacher les tags
    for tag in tags:
        if tag not in document.tags:
            document.tags.append(tag)
    
    db.commit()
    
    return ResponseMessage(
        message=f"Tags attached to document {document_id}",
        success=True
    )


@router.delete("/{document_id}/tags/{tag_id}", response_model=ResponseMessage)
async def detach_tag(
    document_id: int,
    tag_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)
):
    """
    Détacher un tag d'un document
    """
    document = db.query(Document).filter(Document.id_document == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    tag = db.query(TagDocument).filter(TagDocument.id_tag == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    if tag in document.tags:
        document.tags.remove(tag)
        db.commit()
    
    return ResponseMessage(
        message=f"Tag {tag_id} detached from document {document_id}",
        success=True
    ) 