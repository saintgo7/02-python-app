from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app import models, schemas

router = APIRouter(tags=["crud"])


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


# ========== Token CRUD Operations ==========

@router.get("/tokens", response_model=List[schemas.TokenResponse])
def get_tokens(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all tokens with pagination"""
    tokens = db.query(models.Token).filter(
        models.Token.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return tokens


@router.post("/tokens", response_model=schemas.TokenResponse, status_code=status.HTTP_201_CREATED)
def create_token(
    token: schemas.TokenCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new token"""
    db_token = models.Token(
        **token.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


@router.get("/tokens/{item_id}", response_model=schemas.TokenResponse)
def get_token(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific token"""
    token = db.query(models.Token).filter(
        models.Token.id == item_id,
        models.Token.user_id == current_user["user_id"]
    ).first()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found"
        )
    return token


@router.put("/tokens/{item_id}", response_model=schemas.TokenResponse)
def update_token(
    item_id: int,
    token_update: schemas.TokenUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update token"""
    db_token = db.query(models.Token).filter(
        models.Token.id == item_id,
        models.Token.user_id == current_user["user_id"]
    ).first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found"
        )

    update_data = token_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_token, key, value)

    db.commit()
    db.refresh(db_token)
    return db_token


@router.delete("/tokens/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_token(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete token"""
    db_token = db.query(models.Token).filter(
        models.Token.id == item_id,
        models.Token.user_id == current_user["user_id"]
    ).first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found"
        )

    db.delete(db_token)
    db.commit()


# ========== Permission CRUD Operations ==========

@router.get("/permissions", response_model=List[schemas.PermissionResponse])
def get_permissions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all permissions with pagination"""
    permissions = db.query(models.Permission).filter(
        models.Permission.user_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    return permissions


@router.post("/permissions", response_model=schemas.PermissionResponse, status_code=status.HTTP_201_CREATED)
def create_permission(
    permission: schemas.PermissionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new permission"""
    db_permission = models.Permission(
        **permission.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


@router.get("/permissions/{item_id}", response_model=schemas.PermissionResponse)
def get_permission(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific permission"""
    permission = db.query(models.Permission).filter(
        models.Permission.id == item_id,
        models.Permission.user_id == current_user["user_id"]
    ).first()

    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    return permission


@router.put("/permissions/{item_id}", response_model=schemas.PermissionResponse)
def update_permission(
    item_id: int,
    permission_update: schemas.PermissionUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update permission"""
    db_permission = db.query(models.Permission).filter(
        models.Permission.id == item_id,
        models.Permission.user_id == current_user["user_id"]
    ).first()

    if not db_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )

    update_data = permission_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_permission, key, value)

    db.commit()
    db.refresh(db_permission)
    return db_permission


@router.delete("/permissions/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete permission"""
    db_permission = db.query(models.Permission).filter(
        models.Permission.id == item_id,
        models.Permission.user_id == current_user["user_id"]
    ).first()

    if not db_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )

    db.delete(db_permission)
    db.commit()


