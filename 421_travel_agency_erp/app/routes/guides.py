"""Guide schedule management routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import GuideSchedule, User, UserRole, TravelPackage
from app.schemas import GuideScheduleCreate, GuideScheduleUpdate, GuideScheduleResponse
from typing import List

router = APIRouter(prefix="/guides", tags=["guides"])


def check_admin(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Check if user is admin"""
    user = db.query(User).filter(User.id == int(current_user["user_id"])).first()
    if not user or user.role not in [UserRole.ADMIN, UserRole.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can manage guides"
        )
    return user


@router.get("/schedules", response_model=List[GuideScheduleResponse])
async def list_guide_schedules(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    guide_id: int = Query(None),
    status_filter: str = Query(None),
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    List guide schedules (admin only).

    Args:
        skip: Number of records to skip
        limit: Maximum number of records
        guide_id: Filter by guide ID
        status_filter: Filter by status
        admin: Admin verification
        db: Database session

    Returns:
        List of guide schedules
    """
    query = db.query(GuideSchedule)

    if guide_id:
        query = query.filter(GuideSchedule.guide_id == guide_id)

    if status_filter:
        query = query.filter(GuideSchedule.status == status_filter)

    schedules = query.offset(skip).limit(limit).all()
    return schedules


@router.get("/schedules/{schedule_id}", response_model=GuideScheduleResponse)
async def get_guide_schedule(
    schedule_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get guide schedule details.

    Args:
        schedule_id: Schedule ID
        current_user: Current user
        db: Database session

    Returns:
        Schedule data

    Raises:
        HTTPException: If schedule not found
    """
    schedule = db.query(GuideSchedule).filter(GuideSchedule.id == schedule_id).first()

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    return schedule


@router.post("/schedules", response_model=GuideScheduleResponse)
async def create_guide_schedule(
    schedule_data: GuideScheduleCreate,
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Create guide schedule (admin only).

    Args:
        schedule_data: Schedule creation data
        admin: Admin verification
        db: Database session

    Returns:
        Created schedule

    Raises:
        HTTPException: If guide or package not found
    """
    # Verify guide exists and is a guide
    guide = db.query(User).filter(
        User.id == schedule_data.guide_id,
        User.role == UserRole.GUIDE
    ).first()

    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guide not found"
        )

    # Verify package exists
    package = db.query(TravelPackage).filter(
        TravelPackage.id == schedule_data.package_id
    ).first()

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )

    # Validate dates
    if schedule_data.start_date >= schedule_data.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date"
        )

    db_schedule = GuideSchedule(**schedule_data.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)

    return db_schedule


@router.put("/schedules/{schedule_id}", response_model=GuideScheduleResponse)
async def update_guide_schedule(
    schedule_id: int,
    schedule_data: GuideScheduleUpdate,
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Update guide schedule (admin only).

    Args:
        schedule_id: Schedule ID
        schedule_data: Update data
        admin: Admin verification
        db: Database session

    Returns:
        Updated schedule

    Raises:
        HTTPException: If schedule not found
    """
    schedule = db.query(GuideSchedule).filter(GuideSchedule.id == schedule_id).first()

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    update_data = schedule_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(schedule, field, value)

    db.commit()
    db.refresh(schedule)

    return schedule


@router.delete("/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guide_schedule(
    schedule_id: int,
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Delete guide schedule (admin only).

    Args:
        schedule_id: Schedule ID
        admin: Admin verification
        db: Database session

    Raises:
        HTTPException: If schedule not found
    """
    schedule = db.query(GuideSchedule).filter(GuideSchedule.id == schedule_id).first()

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    db.delete(schedule)
    db.commit()


@router.get("/{guide_id}/my-schedules", response_model=List[GuideScheduleResponse])
async def get_my_schedules(
    guide_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get guide's own schedules.

    Args:
        guide_id: Guide ID
        current_user: Current user
        db: Database session

    Returns:
        List of schedules

    Raises:
        HTTPException: If unauthorized
    """
    current_user_id = int(current_user["user_id"])

    if current_user_id != guide_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own schedules"
        )

    schedules = db.query(GuideSchedule).filter(
        GuideSchedule.guide_id == guide_id
    ).all()

    return schedules
