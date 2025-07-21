"""
Modèles pour la gestion des documents
"""
from sqlalchemy import Column, String, Text, BigInteger, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base
from .base import TimestampMixin


# Table d'association pour les tags de documents
document_tag_association = Table(
    'document_tag',
    Base.metadata,
    Column('id_document', BigInteger, ForeignKey('document.id_document'), primary_key=True),
    Column('id_tag', BigInteger, ForeignKey('tag_document.id_tag'), primary_key=True)
)


class Document(Base, TimestampMixin):
    """Modèle pour les documents/fichiers"""
    __tablename__ = "document"
    
    id_document = Column(BigInteger, primary_key=True, autoincrement=True)
    file_path = Column(Text, nullable=False)
    mime_type = Column(Text)
    checksum = Column(Text)
    size_bytes = Column(BigInteger)
    uploaded_by = Column(BigInteger, ForeignKey('employe.id_employe'))
    
    # Relations
    uploader = relationship("Employe", back_populates="uploaded_documents")
    tags = relationship("TagDocument", secondary=document_tag_association, back_populates="documents") 