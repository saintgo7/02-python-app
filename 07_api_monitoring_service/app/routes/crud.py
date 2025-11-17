from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app import models, schemas

router = APIRouter(tags=["crud"])


# ========== Endpoint CRUD Operations ==========

@router.get("/endpoints", response_model=List[schemas.EndpointResponse])
def get_endpoints(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all endpoints with pagination"""
    endpoints = db.query(models.Endpoint).filter(
        models.Endpoint.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return endpoints


@router.post("/endpoints", response_model=schemas.EndpointResponse, status_code=status.HTTP_201_CREATED)
def create_endpoint(
    endpoint: schemas.EndpointCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new endpoint"""
    db_endpoint = models.Endpoint(
        **endpoint.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_endpoint)
    db.commit()
    db.refresh(db_endpoint)
    return db_endpoint


@router.get("/endpoints/{item_id}", response_model=schemas.EndpointResponse)
def get_endpoint(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific endpoint"""
    endpoint = db.query(models.Endpoint).filter(
        models.Endpoint.id == item_id,
        models.Endpoint.user_id == current_user["user_id"]
    ).first()

    if not endpoint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found"
        )
    return endpoint


@router.put("/endpoints/{item_id}", response_model=schemas.EndpointResponse)
def update_endpoint(
    item_id: int,
    endpoint_update: schemas.EndpointUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update endpoint"""
    db_endpoint = db.query(models.Endpoint).filter(
        models.Endpoint.id == item_id,
        models.Endpoint.user_id == current_user["user_id"]
    ).first()

    if not db_endpoint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found"
        )

    update_data = endpoint_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_endpoint, key, value)

    db.commit()
    db.refresh(db_endpoint)
    return db_endpoint


@router.delete("/endpoints/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_endpoint(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete endpoint"""
    db_endpoint = db.query(models.Endpoint).filter(
        models.Endpoint.id == item_id,
        models.Endpoint.user_id == current_user["user_id"]
    ).first()

    if not db_endpoint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found"
        )

    db.delete(db_endpoint)
    db.commit()


# ========== Check CRUD Operations ==========

@router.get("/checks", response_model=List[schemas.CheckResponse])
def get_checks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all checks with pagination"""
    checks = db.query(models.Check).filter(
        models.Check.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return checks


@router.post("/checks", response_model=schemas.CheckResponse, status_code=status.HTTP_201_CREATED)
def create_check(
    check: schemas.CheckCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new check"""
    db_check = models.Check(
        **check.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_check)
    db.commit()
    db.refresh(db_check)
    return db_check


@router.get("/checks/{item_id}", response_model=schemas.CheckResponse)
def get_check(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific check"""
    check = db.query(models.Check).filter(
        models.Check.id == item_id,
        models.Check.user_id == current_user["user_id"]
    ).first()

    if not check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Check not found"
        )
    return check


@router.put("/checks/{item_id}", response_model=schemas.CheckResponse)
def update_check(
    item_id: int,
    check_update: schemas.CheckUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update check"""
    db_check = db.query(models.Check).filter(
        models.Check.id == item_id,
        models.Check.user_id == current_user["user_id"]
    ).first()

    if not db_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Check not found"
        )

    update_data = check_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_check, key, value)

    db.commit()
    db.refresh(db_check)
    return db_check


@router.delete("/checks/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_check(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete check"""
    db_check = db.query(models.Check).filter(
        models.Check.id == item_id,
        models.Check.user_id == current_user["user_id"]
    ).first()

    if not db_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Check not found"
        )

    db.delete(db_check)
    db.commit()


# ========== Alert CRUD Operations ==========

@router.get("/alerts", response_model=List[schemas.AlertResponse])
def get_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all alerts with pagination"""
    alerts = db.query(models.Alert).filter(
        models.Alert.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return alerts


@router.post("/alerts", response_model=schemas.AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(
    alert: schemas.AlertCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new alert"""
    db_alert = models.Alert(
        **alert.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.get("/alerts/{item_id}", response_model=schemas.AlertResponse)
def get_alert(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific alert"""
    alert = db.query(models.Alert).filter(
        models.Alert.id == item_id,
        models.Alert.user_id == current_user["user_id"]
    ).first()

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    return alert


@router.put("/alerts/{item_id}", response_model=schemas.AlertResponse)
def update_alert(
    item_id: int,
    alert_update: schemas.AlertUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update alert"""
    db_alert = db.query(models.Alert).filter(
        models.Alert.id == item_id,
        models.Alert.user_id == current_user["user_id"]
    ).first()

    if not db_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )

    update_data = alert_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_alert, key, value)

    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.delete("/alerts/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete alert"""
    db_alert = db.query(models.Alert).filter(
        models.Alert.id == item_id,
        models.Alert.user_id == current_user["user_id"]
    ).first()

    if not db_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )

    db.delete(db_alert)
    db.commit()


