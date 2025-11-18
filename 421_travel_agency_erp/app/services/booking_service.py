"""Booking business logic service"""

from sqlalchemy.orm import Session
from app.models import Booking, TravelPackage, User, BookingStatus, Payment, PaymentStatus
from app.schemas import BookingCreate
from fastapi import HTTPException, status
from sqlalchemy import func


class BookingService:
    """Service for booking operations"""

    @staticmethod
    def check_availability(db: Session, package_id: int, participants: int) -> bool:
        """Check if package has available spots"""
        package = db.query(TravelPackage).filter(
            TravelPackage.id == package_id
        ).first()

        if not package:
            return False

        # Get confirmed/pending bookings
        existing_bookings = db.query(Booking).filter(
            Booking.package_id == package_id,
            Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.PENDING])
        ).all()

        total_participants = sum(b.number_of_participants for b in existing_bookings)

        return total_participants + participants <= package.max_participants

    @staticmethod
    def create_booking(db: Session, booking_data: BookingCreate, customer_id: int) -> Booking:
        """Create new booking"""
        # Check package exists
        package = db.query(TravelPackage).filter(
            TravelPackage.id == booking_data.package_id
        ).first()

        if not package:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Package not found"
            )

        # Check availability
        if not BookingService.check_availability(
            db,
            booking_data.package_id,
            booking_data.number_of_participants
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Package is fully booked"
            )

        # Calculate price
        total_price = package.price_per_person * booking_data.number_of_participants

        # Create booking
        db_booking = Booking(
            package_id=booking_data.package_id,
            customer_id=customer_id,
            number_of_participants=booking_data.number_of_participants,
            total_price=total_price,
            special_requests=booking_data.special_requests,
            status=BookingStatus.PENDING
        )

        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)

        return db_booking

    @staticmethod
    def get_booking_by_id(db: Session, booking_id: int) -> Booking:
        """Get booking by ID"""
        return db.query(Booking).filter(Booking.id == booking_id).first()

    @staticmethod
    def get_user_bookings(db: Session, user_id: int, status_filter=None, skip=0, limit=10):
        """Get all bookings for a user"""
        query = db.query(Booking).filter(Booking.customer_id == user_id)

        if status_filter:
            query = query.filter(Booking.status == status_filter)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def cancel_booking(db: Session, booking_id: int) -> Booking:
        """Cancel a booking"""
        booking = BookingService.get_booking_by_id(db, booking_id)

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )

        if booking.status == BookingStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking is already cancelled"
            )

        booking.status = BookingStatus.CANCELLED
        db.commit()
        db.refresh(booking)

        return booking

    @staticmethod
    def confirm_booking(db: Session, booking_id: int) -> Booking:
        """Confirm a pending booking"""
        booking = BookingService.get_booking_by_id(db, booking_id)

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )

        if booking.status != BookingStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending bookings can be confirmed"
            )

        booking.status = BookingStatus.CONFIRMED
        db.commit()
        db.refresh(booking)

        return booking

    @staticmethod
    def get_package_occupancy(db: Session, package_id: int) -> float:
        """Get package occupancy rate"""
        package = db.query(TravelPackage).filter(
            TravelPackage.id == package_id
        ).first()

        if not package or package.max_participants == 0:
            return 0.0

        bookings = db.query(Booking).filter(
            Booking.package_id == package_id,
            Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.PENDING])
        ).all()

        total_participants = sum(b.number_of_participants for b in bookings)

        return (total_participants / package.max_participants) * 100
