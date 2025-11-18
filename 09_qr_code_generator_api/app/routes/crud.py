from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app import models, schemas

router = APIRouter(tags=["crud"])


# ========== QRCode CRUD Operations ==========

@router.get("/qrcodes", response_model=List[schemas.QRCodeResponse])
def get_qrcodes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all qrcodes with pagination"""
    qrcodes = db.query(models.QRCode).filter(
        models.QRCode.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return qrcodes


@router.post("/qrcodes", response_model=schemas.QRCodeResponse, status_code=status.HTTP_201_CREATED)
def create_qrcode(
    qrcode: schemas.QRCodeCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new qrcode"""
    db_qrcode = models.QRCode(
        **qrcode.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_qrcode)
    db.commit()
    db.refresh(db_qrcode)
    return db_qrcode


@router.get("/qrcodes/{item_id}", response_model=schemas.QRCodeResponse)
def get_qrcode(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific qrcode"""
    qrcode = db.query(models.QRCode).filter(
        models.QRCode.id == item_id,
        models.QRCode.user_id == current_user["user_id"]
    ).first()

    if not qrcode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QRCode not found"
        )
    return qrcode


@router.put("/qrcodes/{item_id}", response_model=schemas.QRCodeResponse)
def update_qrcode(
    item_id: int,
    qrcode_update: schemas.QRCodeUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update qrcode"""
    db_qrcode = db.query(models.QRCode).filter(
        models.QRCode.id == item_id,
        models.QRCode.user_id == current_user["user_id"]
    ).first()

    if not db_qrcode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QRCode not found"
        )

    update_data = qrcode_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_qrcode, key, value)

    db.commit()
    db.refresh(db_qrcode)
    return db_qrcode


@router.delete("/qrcodes/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_qrcode(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete qrcode"""
    db_qrcode = db.query(models.QRCode).filter(
        models.QRCode.id == item_id,
        models.QRCode.user_id == current_user["user_id"]
    ).first()

    if not db_qrcode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QRCode not found"
        )

    db.delete(db_qrcode)
    db.commit()


# ========== Scan CRUD Operations ==========

@router.get("/scans", response_model=List[schemas.ScanResponse])
def get_scans(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all scans with pagination"""
    scans = db.query(models.Scan).filter(
        models.Scan.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return scans


@router.post("/scans", response_model=schemas.ScanResponse, status_code=status.HTTP_201_CREATED)
def create_scan(
    scan: schemas.ScanCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new scan"""
    db_scan = models.Scan(
        **scan.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan


@router.get("/scans/{item_id}", response_model=schemas.ScanResponse)
def get_scan(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific scan"""
    scan = db.query(models.Scan).filter(
        models.Scan.id == item_id,
        models.Scan.user_id == current_user["user_id"]
    ).first()

    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    return scan


@router.put("/scans/{item_id}", response_model=schemas.ScanResponse)
def update_scan(
    item_id: int,
    scan_update: schemas.ScanUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update scan"""
    db_scan = db.query(models.Scan).filter(
        models.Scan.id == item_id,
        models.Scan.user_id == current_user["user_id"]
    ).first()

    if not db_scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )

    update_data = scan_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_scan, key, value)

    db.commit()
    db.refresh(db_scan)
    return db_scan


@router.delete("/scans/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scan(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete scan"""
    db_scan = db.query(models.Scan).filter(
        models.Scan.id == item_id,
        models.Scan.user_id == current_user["user_id"]
    ).first()

    if not db_scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )

    db.delete(db_scan)
    db.commit()


# ========== Campaign CRUD Operations ==========

@router.get("/campaigns", response_model=List[schemas.CampaignResponse])
def get_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all campaigns with pagination"""
    campaigns = db.query(models.Campaign).filter(
        models.Campaign.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return campaigns


@router.post("/campaigns", response_model=schemas.CampaignResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(
    campaign: schemas.CampaignCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new campaign"""
    db_campaign = models.Campaign(
        **campaign.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign


@router.get("/campaigns/{item_id}", response_model=schemas.CampaignResponse)
def get_campaign(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific campaign"""
    campaign = db.query(models.Campaign).filter(
        models.Campaign.id == item_id,
        models.Campaign.user_id == current_user["user_id"]
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    return campaign


@router.put("/campaigns/{item_id}", response_model=schemas.CampaignResponse)
def update_campaign(
    item_id: int,
    campaign_update: schemas.CampaignUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update campaign"""
    db_campaign = db.query(models.Campaign).filter(
        models.Campaign.id == item_id,
        models.Campaign.user_id == current_user["user_id"]
    ).first()

    if not db_campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    update_data = campaign_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_campaign, key, value)

    db.commit()
    db.refresh(db_campaign)
    return db_campaign


@router.delete("/campaigns/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete campaign"""
    db_campaign = db.query(models.Campaign).filter(
        models.Campaign.id == item_id,
        models.Campaign.user_id == current_user["user_id"]
    ).first()

    if not db_campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    db.delete(db_campaign)
    db.commit()


