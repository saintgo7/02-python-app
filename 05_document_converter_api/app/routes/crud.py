from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app import models, schemas

router = APIRouter(tags=["crud"])


# ========== Document CRUD Operations ==========

@router.get("/documents", response_model=List[schemas.DocumentResponse])
def get_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all documents with pagination"""
    documents = db.query(models.Document).filter(
        models.Document.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return documents


@router.post("/documents", response_model=schemas.DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document(
    document: schemas.DocumentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new document"""
    db_document = models.Document(
        **document.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


@router.get("/documents/{item_id}", response_model=schemas.DocumentResponse)
def get_document(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific document"""
    document = db.query(models.Document).filter(
        models.Document.id == item_id,
        models.Document.user_id == current_user["user_id"]
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return document


@router.put("/documents/{item_id}", response_model=schemas.DocumentResponse)
def update_document(
    item_id: int,
    document_update: schemas.DocumentUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update document"""
    db_document = db.query(models.Document).filter(
        models.Document.id == item_id,
        models.Document.user_id == current_user["user_id"]
    ).first()

    if not db_document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    update_data = document_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_document, key, value)

    db.commit()
    db.refresh(db_document)
    return db_document


@router.delete("/documents/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete document"""
    db_document = db.query(models.Document).filter(
        models.Document.id == item_id,
        models.Document.user_id == current_user["user_id"]
    ).first()

    if not db_document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    db.delete(db_document)
    db.commit()


# ========== Conversion CRUD Operations ==========

@router.get("/conversions", response_model=List[schemas.ConversionResponse])
def get_conversions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all conversions with pagination"""
    conversions = db.query(models.Conversion).filter(
        models.Conversion.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return conversions


@router.post("/conversions", response_model=schemas.ConversionResponse, status_code=status.HTTP_201_CREATED)
def create_conversion(
    conversion: schemas.ConversionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new conversion"""
    db_conversion = models.Conversion(
        **conversion.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_conversion)
    db.commit()
    db.refresh(db_conversion)
    return db_conversion


@router.get("/conversions/{item_id}", response_model=schemas.ConversionResponse)
def get_conversion(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific conversion"""
    conversion = db.query(models.Conversion).filter(
        models.Conversion.id == item_id,
        models.Conversion.user_id == current_user["user_id"]
    ).first()

    if not conversion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversion not found"
        )
    return conversion


@router.put("/conversions/{item_id}", response_model=schemas.ConversionResponse)
def update_conversion(
    item_id: int,
    conversion_update: schemas.ConversionUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update conversion"""
    db_conversion = db.query(models.Conversion).filter(
        models.Conversion.id == item_id,
        models.Conversion.user_id == current_user["user_id"]
    ).first()

    if not db_conversion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversion not found"
        )

    update_data = conversion_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_conversion, key, value)

    db.commit()
    db.refresh(db_conversion)
    return db_conversion


@router.delete("/conversions/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversion(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete conversion"""
    db_conversion = db.query(models.Conversion).filter(
        models.Conversion.id == item_id,
        models.Conversion.user_id == current_user["user_id"]
    ).first()

    if not db_conversion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversion not found"
        )

    db.delete(db_conversion)
    db.commit()


# ========== Template CRUD Operations ==========

@router.get("/templates", response_model=List[schemas.TemplateResponse])
def get_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all templates with pagination"""
    templates = db.query(models.Template).filter(
        models.Template.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return templates


@router.post("/templates", response_model=schemas.TemplateResponse, status_code=status.HTTP_201_CREATED)
def create_template(
    template: schemas.TemplateCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new template"""
    db_template = models.Template(
        **template.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


@router.get("/templates/{item_id}", response_model=schemas.TemplateResponse)
def get_template(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific template"""
    template = db.query(models.Template).filter(
        models.Template.id == item_id,
        models.Template.user_id == current_user["user_id"]
    ).first()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    return template


@router.put("/templates/{item_id}", response_model=schemas.TemplateResponse)
def update_template(
    item_id: int,
    template_update: schemas.TemplateUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update template"""
    db_template = db.query(models.Template).filter(
        models.Template.id == item_id,
        models.Template.user_id == current_user["user_id"]
    ).first()

    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    update_data = template_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_template, key, value)

    db.commit()
    db.refresh(db_template)
    return db_template


@router.delete("/templates/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete template"""
    db_template = db.query(models.Template).filter(
        models.Template.id == item_id,
        models.Template.user_id == current_user["user_id"]
    ).first()

    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    db.delete(db_template)
    db.commit()


