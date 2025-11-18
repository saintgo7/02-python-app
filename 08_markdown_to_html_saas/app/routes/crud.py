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


# ========== Version CRUD Operations ==========

@router.get("/versions", response_model=List[schemas.VersionResponse])
def get_versions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all versions with pagination"""
    versions = db.query(models.Version).filter(
        models.Version.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return versions


@router.post("/versions", response_model=schemas.VersionResponse, status_code=status.HTTP_201_CREATED)
def create_version(
    version: schemas.VersionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new version"""
    db_version = models.Version(
        **version.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version


@router.get("/versions/{item_id}", response_model=schemas.VersionResponse)
def get_version(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific version"""
    version = db.query(models.Version).filter(
        models.Version.id == item_id,
        models.Version.user_id == current_user["user_id"]
    ).first()

    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Version not found"
        )
    return version


@router.put("/versions/{item_id}", response_model=schemas.VersionResponse)
def update_version(
    item_id: int,
    version_update: schemas.VersionUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update version"""
    db_version = db.query(models.Version).filter(
        models.Version.id == item_id,
        models.Version.user_id == current_user["user_id"]
    ).first()

    if not db_version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Version not found"
        )

    update_data = version_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_version, key, value)

    db.commit()
    db.refresh(db_version)
    return db_version


@router.delete("/versions/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_version(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete version"""
    db_version = db.query(models.Version).filter(
        models.Version.id == item_id,
        models.Version.user_id == current_user["user_id"]
    ).first()

    if not db_version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Version not found"
        )

    db.delete(db_version)
    db.commit()


# ========== Share CRUD Operations ==========

@router.get("/shares", response_model=List[schemas.ShareResponse])
def get_shares(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all shares with pagination"""
    shares = db.query(models.Share).filter(
        models.Share.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return shares


@router.post("/shares", response_model=schemas.ShareResponse, status_code=status.HTTP_201_CREATED)
def create_share(
    share: schemas.ShareCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new share"""
    db_share = models.Share(
        **share.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share


@router.get("/shares/{item_id}", response_model=schemas.ShareResponse)
def get_share(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific share"""
    share = db.query(models.Share).filter(
        models.Share.id == item_id,
        models.Share.user_id == current_user["user_id"]
    ).first()

    if not share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share not found"
        )
    return share


@router.put("/shares/{item_id}", response_model=schemas.ShareResponse)
def update_share(
    item_id: int,
    share_update: schemas.ShareUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update share"""
    db_share = db.query(models.Share).filter(
        models.Share.id == item_id,
        models.Share.user_id == current_user["user_id"]
    ).first()

    if not db_share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share not found"
        )

    update_data = share_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_share, key, value)

    db.commit()
    db.refresh(db_share)
    return db_share


@router.delete("/shares/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_share(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete share"""
    db_share = db.query(models.Share).filter(
        models.Share.id == item_id,
        models.Share.user_id == current_user["user_id"]
    ).first()

    if not db_share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share not found"
        )

    db.delete(db_share)
    db.commit()


