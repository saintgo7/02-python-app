"""Payment business logic service"""

from sqlalchemy.orm import Session
from app.models import Payment, Booking, PaymentStatus
from app.schemas import PaymentCreate
from datetime import datetime, timezone
from fastapi import HTTPException, status


class PaymentService:
    """Service for payment operations"""

    @staticmethod
    def get_payment_by_id(db: Session, payment_id: int) -> Payment:
        """Get payment by ID"""
        return db.query(Payment).filter(Payment.id == payment_id).first()

    @staticmethod
    def get_booking_payments(db: Session, booking_id: int):
        """Get all payments for a booking"""
        return db.query(Payment).filter(Payment.booking_id == booking_id).all()

    @staticmethod
    def create_payment(db: Session, payment_data: PaymentCreate) -> Payment:
        """Create new payment"""
        # Verify booking exists
        booking = db.query(Booking).filter(
            Booking.id == payment_data.booking_id
        ).first()

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )

        # Validate payment amount
        if payment_data.amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment amount must be greater than 0"
            )

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

    @staticmethod
    def mark_paid(db: Session, payment_id: int, transaction_id: str = None) -> Payment:
        """Mark payment as paid"""
        payment = PaymentService.get_payment_by_id(db, payment_id)

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )

        payment.status = PaymentStatus.PAID
        payment.payment_date = datetime.now(timezone.utc)
        if transaction_id:
            payment.transaction_id = transaction_id

        db.commit()
        db.refresh(payment)

        return payment

    @staticmethod
    def get_booking_total_paid(db: Session, booking_id: int) -> float:
        """Get total paid amount for a booking"""
        payments = PaymentService.get_booking_payments(db, booking_id)
        return sum(
            p.amount for p in payments
            if p.status in [PaymentStatus.PAID, PaymentStatus.PARTIAL]
        )

    @staticmethod
    def get_booking_balance(db: Session, booking_id: int) -> float:
        """Get remaining balance for a booking"""
        booking = db.query(Booking).filter(Booking.id == booking_id).first()

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )

        total_paid = PaymentService.get_booking_total_paid(db, booking_id)
        return booking.total_price - total_paid

    @staticmethod
    def get_overdue_payments(db: Session):
        """Get all overdue payments"""
        from sqlalchemy import and_
        now = datetime.now(timezone.utc)

        return db.query(Payment).filter(
            and_(
                Payment.due_date < now,
                Payment.status.in_([PaymentStatus.UNPAID, PaymentStatus.PARTIAL])
            )
        ).all()
