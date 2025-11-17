from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app import models, schemas

router = APIRouter(tags=["crud"])


# ========== URL CRUD Operations ==========

@router.get("/urls", response_model=List[schemas.URLResponse])
def get_urls(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all urls with pagination"""
    urls = db.query(models.URL).filter(
        models.URL.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return urls


@router.post("/urls", response_model=schemas.URLResponse, status_code=status.HTTP_201_CREATED)
def create_url(
    url: schemas.URLCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new url"""
    db_url = models.URL(
        **url.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


@router.get("/urls/{item_id}", response_model=schemas.URLResponse)
def get_url(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific url"""
    url = db.query(models.URL).filter(
        models.URL.id == item_id,
        models.URL.user_id == current_user["user_id"]
    ).first()

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )
    return url


@router.put("/urls/{item_id}", response_model=schemas.URLResponse)
def update_url(
    item_id: int,
    url_update: schemas.URLUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update url"""
    db_url = db.query(models.URL).filter(
        models.URL.id == item_id,
        models.URL.user_id == current_user["user_id"]
    ).first()

    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )

    update_data = url_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_url, key, value)

    db.commit()
    db.refresh(db_url)
    return db_url


@router.delete("/urls/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_url(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete url"""
    db_url = db.query(models.URL).filter(
        models.URL.id == item_id,
        models.URL.user_id == current_user["user_id"]
    ).first()

    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )

    db.delete(db_url)
    db.commit()


# ========== Click CRUD Operations ==========

@router.get("/clicks", response_model=List[schemas.ClickResponse])
def get_clicks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all clicks with pagination"""
    clicks = db.query(models.Click).filter(
        models.Click.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return clicks


@router.post("/clicks", response_model=schemas.ClickResponse, status_code=status.HTTP_201_CREATED)
def create_click(
    click: schemas.ClickCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new click"""
    db_click = models.Click(
        **click.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_click)
    db.commit()
    db.refresh(db_click)
    return db_click


@router.get("/clicks/{item_id}", response_model=schemas.ClickResponse)
def get_click(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific click"""
    click = db.query(models.Click).filter(
        models.Click.id == item_id,
        models.Click.user_id == current_user["user_id"]
    ).first()

    if not click:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Click not found"
        )
    return click


@router.put("/clicks/{item_id}", response_model=schemas.ClickResponse)
def update_click(
    item_id: int,
    click_update: schemas.ClickUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update click"""
    db_click = db.query(models.Click).filter(
        models.Click.id == item_id,
        models.Click.user_id == current_user["user_id"]
    ).first()

    if not db_click:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Click not found"
        )

    update_data = click_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_click, key, value)

    db.commit()
    db.refresh(db_click)
    return db_click


@router.delete("/clicks/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_click(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete click"""
    db_click = db.query(models.Click).filter(
        models.Click.id == item_id,
        models.Click.user_id == current_user["user_id"]
    ).first()

    if not db_click:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Click not found"
        )

    db.delete(db_click)
    db.commit()


# ========== User CRUD Operations ==========

@router.get("/users", response_model=List[schemas.UserResponse])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all users with pagination"""
    users = db.query(models.User).filter(
        models.User.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return users


@router.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.UserCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new user"""
    db_user = models.User(
        **user.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/users/{item_id}", response_model=schemas.UserResponse)
def get_user(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific user"""
    user = db.query(models.User).filter(
        models.User.id == item_id,
        models.User.user_id == current_user["user_id"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/users/{item_id}", response_model=schemas.UserResponse)
def update_user(
    item_id: int,
    user_update: schemas.UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user"""
    db_user = db.query(models.User).filter(
        models.User.id == item_id,
        models.User.user_id == current_user["user_id"]
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/users/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user"""
    db_user = db.query(models.User).filter(
        models.User.id == item_id,
        models.User.user_id == current_user["user_id"]
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(db_user)
    db.commit()


