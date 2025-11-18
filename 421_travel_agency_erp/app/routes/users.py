"""User management routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, UserRole
from app.schemas import UserResponse, UserUpdate
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


def check_admin(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Check if user is admin"""
    user = db.query(User).filter(User.id == int(current_user["user_id"])).first()
    if not user or user.role not in [UserRole.ADMIN, UserRole.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can manage users"
        )
    return user


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    role: UserRole = Query(None),
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    List all users (admin only).

    Args:
        skip: Number of records to skip
        limit: Maximum number of records
        role: Filter by user role
        admin: Admin verification
        db: Database session

    Returns:
        List of users
    """
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)

    users = query.offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user details.

    Args:
        user_id: User ID
        current_user: Current user
        db: Database session

    Returns:
        User data

    Raises:
        HTTPException: If user not found or unauthorized
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Users can only view their own profile unless admin
    current_user_id = int(current_user["user_id"])
    current_user_obj = db.query(User).filter(User.id == current_user_id).first()

    if current_user_id != user_id and current_user_obj.role not in [UserRole.ADMIN, UserRole.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own profile"
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile.

    Args:
        user_id: User ID
        user_data: Update data
        current_user: Current user
        db: Database session

    Returns:
        Updated user

    Raises:
        HTTPException: If user not found or unauthorized
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Users can only update their own profile unless admin
    current_user_id = int(current_user["user_id"])
    current_user_obj = db.query(User).filter(User.id == current_user_id).first()

    if current_user_id != user_id and current_user_obj.role not in [UserRole.ADMIN, UserRole.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )

    # Update fields
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


@router.get("/guides/list", response_model=List[UserResponse])
async def list_guides(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    List all guides.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records
        db: Database session

    Returns:
        List of guides
    """
    guides = db.query(User).filter(
        User.role == UserRole.GUIDE,
        User.is_active == True
    ).offset(skip).limit(limit).all()

    return guides


@router.patch("/{user_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
    user_id: int,
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Deactivate user (admin only).

    Args:
        user_id: User ID
        admin: Admin verification
        db: Database session

    Raises:
        HTTPException: If user not found
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.is_active = False
    db.commit()
