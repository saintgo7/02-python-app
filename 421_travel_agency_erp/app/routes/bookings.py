"""Booking management routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Booking, TravelPackage, User, BookingStatus
from app.schemas import BookingCreate, BookingUpdate, BookingResponse
from typing import List

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/", response_model=List[BookingResponse])
async def list_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status_filter: BookingStatus = Query(None),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List user's bookings with filters.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records
        status_filter: Filter by booking status
        current_user: Current user
        db: Database session

    Returns:
        List of bookings
    """
    user_id = int(current_user["user_id"])
    query = db.query(Booking).filter(Booking.customer_id == user_id)

    if status_filter:
        query = query.filter(Booking.status == status_filter)

    bookings = query.offset(skip).limit(limit).all()
    return bookings


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get booking details.

    Args:
        booking_id: Booking ID
        current_user: Current user
        db: Database session

    Returns:
        Booking data

    Raises:
        HTTPException: If booking not found or unauthorized
    """
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    # Check authorization
    if booking.customer_id != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own bookings"
        )

    return booking


@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking_data: BookingCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new booking.

    Args:
        booking_data: Booking creation data
        current_user: Current user
        db: Database session

    Returns:
        Created booking

    Raises:
        HTTPException: If package not found or invalid data
    """
    # Verify package exists
    package = db.query(TravelPackage).filter(
        TravelPackage.id == booking_data.package_id
    ).first()

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )

    # Check availability
    existing_bookings = db.query(Booking).filter(
        Booking.package_id == booking_data.package_id,
        Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.PENDING])
    ).all()

    total_participants = sum(b.number_of_participants for b in existing_bookings)

    if total_participants + booking_data.number_of_participants > package.max_participants:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Package is fully booked"
        )

    # Create booking
    total_price = package.price_per_person * booking_data.number_of_participants
    db_booking = Booking(
        package_id=booking_data.package_id,
        customer_id=int(current_user["user_id"]),
        number_of_participants=booking_data.number_of_participants,
        total_price=total_price,
        special_requests=booking_data.special_requests
    )

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    return db_booking


@router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update booking.

    Args:
        booking_id: Booking ID
        booking_data: Update data
        current_user: Current user
        db: Database session

    Returns:
        Updated booking

    Raises:
        HTTPException: If not found or unauthorized
    """
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    # Check authorization
    if booking.customer_id != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own bookings"
        )

    # Can only update pending bookings
    if booking.status != BookingStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only update pending bookings"
        )

    # Update fields
    update_data = booking_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(booking, field, value)

    db.commit()
    db.refresh(booking)

    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_booking(
    booking_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel a booking.

    Args:
        booking_id: Booking ID
        current_user: Current user
        db: Database session

    Raises:
        HTTPException: If not found or unauthorized
    """
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    # Check authorization
    if booking.customer_id != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only cancel your own bookings"
        )

    # Update status to cancelled
    booking.status = BookingStatus.CANCELLED
    db.commit()
