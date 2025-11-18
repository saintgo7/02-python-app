"""Travel package business logic service"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import TravelPackage, Booking, Review, BookingStatus, PaymentStatus, Payment, Expense
from fastapi import HTTPException, status


class PackageService:
    """Service for travel package operations"""

    @staticmethod
    def get_package_by_id(db: Session, package_id: int) -> TravelPackage:
        """Get package by ID"""
        return db.query(TravelPackage).filter(TravelPackage.id == package_id).first()

    @staticmethod
    def get_all_packages(
        db: Session,
        active_only: bool = True,
        destination: str = None,
        skip: int = 0,
        limit: int = 10
    ):
        """Get packages with filters"""
        query = db.query(TravelPackage)

        if active_only:
            query = query.filter(TravelPackage.is_active == True)

        if destination:
            query = query.filter(TravelPackage.destination.ilike(f"%{destination}%"))

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_package_statistics(db: Session, package_id: int) -> dict:
        """Get detailed statistics for a package"""
        package = PackageService.get_package_by_id(db, package_id)

        if not package:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Package not found"
            )

        # Booking statistics
        bookings = db.query(Booking).filter(Booking.package_id == package_id).all()
        confirmed_bookings = [b for b in bookings if b.status == BookingStatus.CONFIRMED]
        total_participants = sum(b.number_of_participants for b in bookings)
        confirmed_participants = sum(b.number_of_participants for b in confirmed_bookings)
        occupancy_rate = (confirmed_participants / package.max_participants * 100) if package.max_participants > 0 else 0

        # Revenue statistics
        revenue = db.query(func.sum(Payment.amount)).join(
            Booking
        ).filter(
            Booking.package_id == package_id,
            Payment.status == PaymentStatus.PAID
        ).scalar() or 0

        # Expense statistics
        expenses = db.query(func.sum(Expense.amount)).filter(
            Expense.package_id == package_id
        ).scalar() or 0

        # Rating statistics
        avg_rating = db.query(func.avg(Review.rating)).join(
            Booking
        ).filter(
            Booking.package_id == package_id
        ).scalar()

        review_count = db.query(func.count(Review.id)).join(
            Booking
        ).filter(
            Booking.package_id == package_id
        ).scalar() or 0

        return {
            "package_id": package_id,
            "package_name": package.name,
            "total_bookings": len(bookings),
            "confirmed_bookings": len(confirmed_bookings),
            "total_participants": total_participants,
            "confirmed_participants": confirmed_participants,
            "occupancy_rate": occupancy_rate,
            "revenue": float(revenue),
            "expenses": float(expenses),
            "profit": float(revenue - expenses),
            "profit_margin": ((revenue - expenses) / revenue * 100) if revenue > 0 else 0,
            "average_rating": float(avg_rating) if avg_rating else None,
            "review_count": review_count
        }

    @staticmethod
    def search_packages(
        db: Session,
        destination: str = None,
        min_price: float = None,
        max_price: float = None,
        duration_min: int = None,
        duration_max: int = None
    ):
        """Search packages by criteria"""
        query = db.query(TravelPackage).filter(TravelPackage.is_active == True)

        if destination:
            query = query.filter(TravelPackage.destination.ilike(f"%{destination}%"))

        if min_price:
            query = query.filter(TravelPackage.price_per_person >= min_price)

        if max_price:
            query = query.filter(TravelPackage.price_per_person <= max_price)

        if duration_min:
            query = query.filter(TravelPackage.duration_days >= duration_min)

        if duration_max:
            query = query.filter(TravelPackage.duration_days <= duration_max)

        return query.all()

    @staticmethod
    def get_popular_packages(db: Session, limit: int = 10):
        """Get most popular packages by booking count"""
        return db.query(TravelPackage).join(
            Booking
        ).group_by(
            TravelPackage.id
        ).order_by(
            func.count(Booking.id).desc()
        ).limit(limit).all()

    @staticmethod
    def get_top_rated_packages(db: Session, limit: int = 10):
        """Get highest rated packages"""
        return db.query(TravelPackage).join(
            Booking
        ).join(
            Review
        ).group_by(
            TravelPackage.id
        ).order_by(
            func.avg(Review.rating).desc()
        ).limit(limit).all()
