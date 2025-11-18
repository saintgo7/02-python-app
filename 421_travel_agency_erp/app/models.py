"""Database models for Travel Agency ERP System"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base
import enum


class UserRole(str, enum.Enum):
    """User roles in the system"""
    ADMIN = "admin"
    STAFF = "staff"
    GUIDE = "guide"
    CUSTOMER = "customer"


class BookingStatus(str, enum.Enum):
    """Booking status"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus(str, enum.Enum):
    """Payment status"""
    UNPAID = "unpaid"
    PARTIAL = "partial"
    PAID = "paid"
    REFUNDED = "refunded"


class User(Base):
    """User model for customers, staff, and guides"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    bookings = relationship("Booking", back_populates="customer", foreign_keys="Booking.customer_id")
    guide_schedule = relationship("GuideSchedule", back_populates="guide")
    reviews = relationship("Review", back_populates="author")


class TravelPackage(Base):
    """Travel package offered by the agency"""
    __tablename__ = "travel_packages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    destination = Column(String(255), nullable=False, index=True)
    duration_days = Column(Integer, nullable=False)
    price_per_person = Column(Float, nullable=False)
    max_participants = Column(Integer, default=30)
    included_services = Column(Text)  # JSON string of included services
    itinerary = Column(Text)  # Detailed day-by-day itinerary
    difficulty_level = Column(String(50), default="moderate")  # easy, moderate, hard
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    bookings = relationship("Booking", back_populates="package")
    expenses = relationship("Expense", back_populates="package")


class Booking(Base):
    """Booking/Reservation for travel packages"""
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    package_id = Column(Integer, ForeignKey("travel_packages.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    number_of_participants = Column(Integer, default=1)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    special_requests = Column(Text)
    booking_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    confirmation_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    package = relationship("TravelPackage", back_populates="bookings")
    customer = relationship("User", back_populates="bookings", foreign_keys=[customer_id])
    payments = relationship("Payment", back_populates="booking")


class Payment(Base):
    """Payment records for bookings"""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50))  # credit_card, bank_transfer, cash, etc.
    status = Column(Enum(PaymentStatus), default=PaymentStatus.UNPAID)
    transaction_id = Column(String(255), nullable=True)
    payment_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    booking = relationship("Booking", back_populates="payments")


class GuideSchedule(Base):
    """Guide assignment to travel packages"""
    __tablename__ = "guide_schedules"

    id = Column(Integer, primary_key=True, index=True)
    guide_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    package_id = Column(Integer, ForeignKey("travel_packages.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    daily_rate = Column(Float, nullable=False)
    status = Column(String(50), default="scheduled")  # scheduled, completed, cancelled
    notes = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    guide = relationship("User", back_populates="guide_schedule")


class Expense(Base):
    """Expense tracking for packages"""
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    package_id = Column(Integer, ForeignKey("travel_packages.id"), nullable=False)
    category = Column(String(100), nullable=False)  # accommodation, transport, meals, permits, etc.
    description = Column(Text)
    amount = Column(Float, nullable=False)
    vendor = Column(String(255), nullable=True)
    expense_date = Column(DateTime, nullable=False)
    receipt_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    package = relationship("TravelPackage", back_populates="expenses")


class Review(Base):
    """Customer reviews and ratings"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    title = Column(String(255), nullable=False)
    content = Column(Text)
    guide_rating = Column(Integer, nullable=True)  # Separate rating for guide
    would_recommend = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    author = relationship("User", back_populates="reviews")
