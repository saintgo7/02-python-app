"""Review management routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Review, Booking, User
from app.schemas import ReviewCreate, ReviewUpdate, ReviewResponse
from typing import List

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/", response_model=List[ReviewResponse])
async def list_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    booking_id: int = Query(None),
    min_rating: int = Query(None, ge=1, le=5),
    db: Session = Depends(get_db)
):
    """
    List reviews with filters.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records
        booking_id: Filter by booking ID
        min_rating: Filter by minimum rating
        db: Database session

    Returns:
        List of reviews
    """
    query = db.query(Review)

    if booking_id:
        query = query.filter(Review.booking_id == booking_id)

    if min_rating:
        query = query.filter(Review.rating >= min_rating)

    reviews = query.offset(skip).limit(limit).all()
    return reviews


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: int,
    db: Session = Depends(get_db)
):
    """
    Get review details.

    Args:
        review_id: Review ID
        db: Database session

    Returns:
        Review data

    Raises:
        HTTPException: If review not found
    """
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    return review


@router.post("/", response_model=ReviewResponse)
async def create_review(
    review_data: ReviewCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a review for a booking.

    Args:
        review_data: Review creation data
        current_user: Current user
        db: Database session

    Returns:
        Created review

    Raises:
        HTTPException: If booking not found or unauthorized
    """
    # Verify booking exists and belongs to user
    booking = db.query(Booking).filter(Booking.id == review_data.booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    if booking.customer_id != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only review your own bookings"
        )

    # Check if review already exists
    existing_review = db.query(Review).filter(
        Review.booking_id == review_data.booking_id
    ).first()

    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Review already exists for this booking"
        )

    db_review = Review(
        **review_data.model_dump(),
        author_id=int(current_user["user_id"])
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review


@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update review.

    Args:
        review_id: Review ID
        review_data: Update data
        current_user: Current user
        db: Database session

    Returns:
        Updated review

    Raises:
        HTTPException: If review not found or unauthorized
    """
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    # Check authorization
    if review.author_id != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own reviews"
        )

    update_data = review_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)

    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete review.

    Args:
        review_id: Review ID
        current_user: Current user
        db: Database session

    Raises:
        HTTPException: If review not found or unauthorized
    """
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    # Check authorization
    if review.author_id != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own reviews"
        )

    db.delete(review)
    db.commit()


@router.get("/booking/{booking_id}/review", response_model=ReviewResponse)
async def get_booking_review(
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Get review for a booking.

    Args:
        booking_id: Booking ID
        db: Database session

    Returns:
        Review data

    Raises:
        HTTPException: If review not found
    """
    review = db.query(Review).filter(Review.booking_id == booking_id).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found for this booking"
        )

    return review
