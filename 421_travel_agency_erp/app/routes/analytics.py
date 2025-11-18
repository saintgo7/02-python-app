"""Analytics and reporting routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone, timedelta
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import (
    Booking, Payment, TravelPackage, Expense, Review,
    User, UserRole, BookingStatus, PaymentStatus
)
from app.schemas import PackageAnalytics, FinancialReport

router = APIRouter(prefix="/analytics", tags=["analytics"])


def check_admin(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Check if user is admin"""
    user = db.query(User).filter(User.id == int(current_user["user_id"])).first()
    if not user or user.role not in [UserRole.ADMIN, UserRole.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view analytics"
        )
    return user


@router.get("/packages/{package_id}", response_model=PackageAnalytics)
async def get_package_analytics(
    package_id: int,
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Get analytics for a specific package.

    Args:
        package_id: Package ID
        admin: Admin verification
        db: Database session

    Returns:
        Package analytics data

    Raises:
        HTTPException: If package not found
    """
    package = db.query(TravelPackage).filter(TravelPackage.id == package_id).first()

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )

    # Get booking statistics
    bookings = db.query(Booking).filter(Booking.package_id == package_id).all()
    total_bookings = len(bookings)
    total_participants = sum(b.number_of_participants for b in bookings)
    occupancy_rate = (total_participants / package.max_participants) if package.max_participants > 0 else 0

    # Calculate revenue
    paid_amount = db.query(func.sum(Payment.amount)).join(
        Booking
    ).filter(
        Booking.package_id == package_id,
        Payment.status == PaymentStatus.PAID
    ).scalar() or 0

    # Calculate expenses
    total_expenses = db.query(func.sum(Expense.amount)).filter(
        Expense.package_id == package_id
    ).scalar() or 0

    # Calculate profitability
    profitability = paid_amount - total_expenses

    # Get average rating
    avg_rating = db.query(func.avg(Review.rating)).join(
        Booking
    ).filter(
        Booking.package_id == package_id
    ).scalar() or 0

    return PackageAnalytics(
        package_id=package_id,
        package_name=package.name,
        total_revenue=float(paid_amount),
        total_bookings=total_bookings,
        total_participants=total_participants,
        average_rating=float(avg_rating) if avg_rating else None,
        occupancy_rate=float(occupancy_rate),
        profitability=float(profitability)
    )


@router.get("/financial-report", response_model=FinancialReport)
async def get_financial_report(
    period_days: int = Query(30, ge=1, le=365),
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Get financial report for a period.

    Args:
        period_days: Number of days to include in report
        admin: Admin verification
        db: Database session

    Returns:
        Financial report data
    """
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=period_days)

    # Calculate revenue
    total_revenue = db.query(func.sum(Payment.amount)).filter(
        Payment.payment_date >= start_date,
        Payment.payment_date <= end_date,
        Payment.status == PaymentStatus.PAID
    ).scalar() or 0

    # Calculate expenses
    total_expenses = db.query(func.sum(Expense.amount)).filter(
        Expense.expense_date >= start_date,
        Expense.expense_date <= end_date
    ).scalar() or 0

    # Get booking statistics
    bookings = db.query(Booking).filter(
        Booking.booking_date >= start_date,
        Booking.booking_date <= end_date
    ).all()

    bookings_count = len(bookings)
    total_booking_value = sum(b.total_price for b in bookings)
    avg_booking_value = (total_booking_value / bookings_count) if bookings_count > 0 else 0

    # Calculate profit
    gross_profit = total_revenue - total_expenses
    profit_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0

    return FinancialReport(
        period_start=start_date,
        period_end=end_date,
        total_revenue=float(total_revenue),
        total_expenses=float(total_expenses),
        gross_profit=float(gross_profit),
        profit_margin=float(profit_margin),
        bookings_count=bookings_count,
        average_booking_value=float(avg_booking_value)
    )


@router.get("/dashboard-summary")
async def get_dashboard_summary(
    admin: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """
    Get dashboard summary for admin.

    Args:
        admin: Admin verification
        db: Database session

    Returns:
        Dashboard summary data
    """
    # Total revenue
    total_revenue = db.query(func.sum(Payment.amount)).filter(
        Payment.status == PaymentStatus.PAID
    ).scalar() or 0

    # Total bookings
    total_bookings = db.query(func.count(Booking.id)).scalar() or 0

    # Pending payments
    pending_payments = db.query(func.sum(Payment.amount)).filter(
        Payment.status == PaymentStatus.UNPAID
    ).scalar() or 0

    # Total packages
    total_packages = db.query(func.count(TravelPackage.id)).scalar() or 0

    # Active bookings
    active_bookings = db.query(func.count(Booking.id)).filter(
        Booking.status == BookingStatus.CONFIRMED
    ).scalar() or 0

    return {
        "total_revenue": float(total_revenue),
        "total_bookings": total_bookings,
        "pending_payments": float(pending_payments),
        "total_packages": total_packages,
        "active_bookings": active_bookings,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
