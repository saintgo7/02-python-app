from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app import models, schemas

router = APIRouter(tags=["crud"])


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


# ========== Subscriber CRUD Operations ==========

@router.get("/subscribers", response_model=List[schemas.SubscriberResponse])
def get_subscribers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all subscribers with pagination"""
    subscribers = db.query(models.Subscriber).filter(
        models.Subscriber.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return subscribers


@router.post("/subscribers", response_model=schemas.SubscriberResponse, status_code=status.HTTP_201_CREATED)
def create_subscriber(
    subscriber: schemas.SubscriberCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new subscriber"""
    db_subscriber = models.Subscriber(
        **subscriber.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_subscriber)
    db.commit()
    db.refresh(db_subscriber)
    return db_subscriber


@router.get("/subscribers/{item_id}", response_model=schemas.SubscriberResponse)
def get_subscriber(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific subscriber"""
    subscriber = db.query(models.Subscriber).filter(
        models.Subscriber.id == item_id,
        models.Subscriber.user_id == current_user["user_id"]
    ).first()

    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscriber not found"
        )
    return subscriber


@router.put("/subscribers/{item_id}", response_model=schemas.SubscriberResponse)
def update_subscriber(
    item_id: int,
    subscriber_update: schemas.SubscriberUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update subscriber"""
    db_subscriber = db.query(models.Subscriber).filter(
        models.Subscriber.id == item_id,
        models.Subscriber.user_id == current_user["user_id"]
    ).first()

    if not db_subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscriber not found"
        )

    update_data = subscriber_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_subscriber, key, value)

    db.commit()
    db.refresh(db_subscriber)
    return db_subscriber


@router.delete("/subscribers/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscriber(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete subscriber"""
    db_subscriber = db.query(models.Subscriber).filter(
        models.Subscriber.id == item_id,
        models.Subscriber.user_id == current_user["user_id"]
    ).first()

    if not db_subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscriber not found"
        )

    db.delete(db_subscriber)
    db.commit()


# ========== Email CRUD Operations ==========

@router.get("/emails", response_model=List[schemas.EmailResponse])
def get_emails(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all emails with pagination"""
    emails = db.query(models.Email).filter(
        models.Email.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return emails


@router.post("/emails", response_model=schemas.EmailResponse, status_code=status.HTTP_201_CREATED)
def create_email(
    email: schemas.EmailCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new email"""
    db_email = models.Email(
        **email.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email


@router.get("/emails/{item_id}", response_model=schemas.EmailResponse)
def get_email(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific email"""
    email = db.query(models.Email).filter(
        models.Email.id == item_id,
        models.Email.user_id == current_user["user_id"]
    ).first()

    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    return email


@router.put("/emails/{item_id}", response_model=schemas.EmailResponse)
def update_email(
    item_id: int,
    email_update: schemas.EmailUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update email"""
    db_email = db.query(models.Email).filter(
        models.Email.id == item_id,
        models.Email.user_id == current_user["user_id"]
    ).first()

    if not db_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )

    update_data = email_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_email, key, value)

    db.commit()
    db.refresh(db_email)
    return db_email


@router.delete("/emails/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_email(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete email"""
    db_email = db.query(models.Email).filter(
        models.Email.id == item_id,
        models.Email.user_id == current_user["user_id"]
    ).first()

    if not db_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )

    db.delete(db_email)
    db.commit()


