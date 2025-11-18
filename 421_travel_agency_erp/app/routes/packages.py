"""Travel package management routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import TravelPackage, User, UserRole
from app.schemas import TravelPackageCreate, TravelPackageUpdate, TravelPackageResponse
from typing import List

router = APIRouter(prefix="/packages", tags=["travel packages"])


def check_admin(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Check if user is admin"""
    user = db.query(User).filter(User.id == int(current_user["user_id"])).first()
    if not user or user.role not in [UserRole.ADMIN, UserRole.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can manage packages"
        )
    return user


@router.get("/", response_model=List[TravelPackageResponse])
async def list_packages(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    destination: str = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """
    List travel packages with pagination and filters.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        destination: Filter by destination
        active_only: Only return active packages
        db: Database session

    Returns:
        List of packages
    """
    query = db.query(TravelPackage)

    if active_only:
        query = query.filter(TravelPackage.is_active == True)

    if destination:
        query = query.filter(TravelPackage.destination.ilike(f"%{destination}%"))

    packages = query.offset(skip).limit(limit).all()
    return packages


@router.get("/{package_id}", response_model=TravelPackageResponse)
async def get_package(package_id: int, db: Session = Depends(get_db)):
    """
    Get package details by ID.

    Args:
        package_id: Package ID
        db: Database session

    Returns:
        Package data

    Raises:
        HTTPException: If package not found
    """
    package = db.query(TravelPackage).filter(TravelPackage.id == package_id).first()

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )

    return package


@router.post("/", response_model=TravelPackageResponse)
async def create_package(
    package_data: TravelPackageCreate,
    current_user: dict = Depends(get_current_user),
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Create a new travel package (admin only).

    Args:
        package_data: Package creation data
        current_user: Current user
        admin: Admin verification
        db: Database session

    Returns:
        Created package
    """
    db_package = TravelPackage(**package_data.model_dump())
    db.add(db_package)
    db.commit()
    db.refresh(db_package)

    return db_package


@router.put("/{package_id}", response_model=TravelPackageResponse)
async def update_package(
    package_id: int,
    package_data: TravelPackageUpdate,
    current_user: dict = Depends(get_current_user),
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Update travel package (admin only).

    Args:
        package_id: Package ID
        package_data: Update data
        current_user: Current user
        admin: Admin verification
        db: Database session

    Returns:
        Updated package

    Raises:
        HTTPException: If package not found
    """
    package = db.query(TravelPackage).filter(TravelPackage.id == package_id).first()

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )

    # Update only provided fields
    update_data = package_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(package, field, value)

    db.commit()
    db.refresh(package)

    return package


@router.delete("/{package_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_package(
    package_id: int,
    current_user: dict = Depends(get_current_user),
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Delete travel package (admin only).

    Args:
        package_id: Package ID
        current_user: Current user
        admin: Admin verification
        db: Database session

    Raises:
        HTTPException: If package not found
    """
    package = db.query(TravelPackage).filter(TravelPackage.id == package_id).first()

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )

    db.delete(package)
    db.commit()
