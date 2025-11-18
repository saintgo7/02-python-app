"""Payment management routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Payment, Booking, User, PaymentStatus
from app.schemas import PaymentCreate, PaymentUpdate, PaymentResponse
from typing import List

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("/", response_model=List[PaymentResponse])
async def list_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    booking_id: int = Query(None),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List payments for user's bookings.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records
        booking_id: Filter by booking ID
        current_user: Current user
        db: Database session

    Returns:
        List of payments
    """
    user_id = int(current_user["user_id"])

    # Get user's bookings
    bookings = db.query(Booking.id).filter(Booking.customer_id == user_id).all()
    booking_ids = [b.id for b in bookings]

    query = db.query(Payment).filter(Payment.booking_id.in_(booking_ids))

    if booking_id:
        query = query.filter(Payment.booking_id == booking_id)

    payments = query.offset(skip).limit(limit).all()
    return payments


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get payment details.

    Args:
        payment_id: Payment ID
        current_user: Current user
        db: Database session

    Returns:
        Payment data

    Raises:
        HTTPException: If payment not found or unauthorized
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    # Check authorization - user must own the booking
    booking = db.query(Booking).filter(Booking.id == payment.booking_id).first()
    if booking.customer_id != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized"
        )

    return payment


@router.post("/", response_model=PaymentResponse)
async def create_payment(
    payment_data: PaymentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a payment record.

    Args:
        payment_data: Payment creation data
        current_user: Current user
        db: Database session

    Returns:
        Created payment

    Raises:
        HTTPException: If booking not found or unauthorized
    """
    # Verify booking exists and belongs to user
    booking = db.query(Booking).filter(Booking.id == payment_data.booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    if booking.customer_id != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only pay for your own bookings"
        )

    # Create payment
    db_payment = Payment(
        booking_id=payment_data.booking_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
        due_date=payment_data.due_date,
        notes=payment_data.notes,
        status=PaymentStatus.UNPAID
    )

    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    return db_payment


@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update payment record (admin only).

    Args:
        payment_id: Payment ID
        payment_data: Update data
        current_user: Current user
        db: Database session

    Returns:
        Updated payment

    Raises:
        HTTPException: If not found or unauthorized
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    # Only allow updates to own bookings
    booking = db.query(Booking).filter(Booking.id == payment.booking_id).first()
    if booking.customer_id != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized"
        )

    # Update fields
    update_data = payment_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "status" and value == PaymentStatus.PAID:
            update_data["payment_date"] = datetime.now(timezone.utc)
        setattr(payment, field, value)

    db.commit()
    db.refresh(payment)

    return payment
