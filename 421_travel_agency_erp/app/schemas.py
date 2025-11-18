"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from app.models import UserRole, BookingStatus, PaymentStatus


# ============== User Schemas ==============

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=255)
    phone: Optional[str] = None
    role: UserRole = UserRole.CUSTOMER


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserResponse(UserBase):
    """User response schema"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============== Travel Package Schemas ==============

class TravelPackageBase(BaseModel):
    """Base travel package schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    destination: str = Field(..., min_length=1, max_length=255)
    duration_days: int = Field(..., gt=0)
    price_per_person: float = Field(..., gt=0)
    max_participants: int = Field(default=30, gt=0)
    included_services: Optional[str] = None
    itinerary: Optional[str] = None
    difficulty_level: str = "moderate"


class TravelPackageCreate(TravelPackageBase):
    """Create travel package schema"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class TravelPackageUpdate(BaseModel):
    """Update travel package schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    destination: Optional[str] = None
    duration_days: Optional[int] = None
    price_per_person: Optional[float] = None
    max_participants: Optional[int] = None
    is_active: Optional[bool] = None


class TravelPackageResponse(TravelPackageBase):
    """Travel package response schema"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============== Booking Schemas ==============

class BookingBase(BaseModel):
    """Base booking schema"""
    package_id: int
    number_of_participants: int = Field(default=1, gt=0)
    special_requests: Optional[str] = None


class BookingCreate(BookingBase):
    """Create booking schema"""
    pass


class BookingUpdate(BaseModel):
    """Update booking schema"""
    number_of_participants: Optional[int] = None
    special_requests: Optional[str] = None
    status: Optional[BookingStatus] = None


class BookingResponse(BookingBase):
    """Booking response schema"""
    id: int
    customer_id: int
    total_price: float
    status: BookingStatus
    booking_date: datetime
    confirmation_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============== Payment Schemas ==============

class PaymentBase(BaseModel):
    """Base payment schema"""
    booking_id: int
    amount: float = Field(..., gt=0)
    payment_method: str
    due_date: Optional[datetime] = None
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    """Create payment schema"""
    pass


class PaymentUpdate(BaseModel):
    """Update payment schema"""
    status: Optional[PaymentStatus] = None
    transaction_id: Optional[str] = None
    notes: Optional[str] = None


class PaymentResponse(PaymentBase):
    """Payment response schema"""
    id: int
    status: PaymentStatus
    transaction_id: Optional[str]
    payment_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============== Guide Schedule Schemas ==============

class GuideScheduleBase(BaseModel):
    """Base guide schedule schema"""
    guide_id: int
    package_id: int
    start_date: datetime
    end_date: datetime
    daily_rate: float = Field(..., gt=0)
    notes: Optional[str] = None


class GuideScheduleCreate(GuideScheduleBase):
    """Create guide schedule schema"""
    pass


class GuideScheduleUpdate(BaseModel):
    """Update guide schedule schema"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    daily_rate: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class GuideScheduleResponse(GuideScheduleBase):
    """Guide schedule response schema"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============== Expense Schemas ==============

class ExpenseBase(BaseModel):
    """Base expense schema"""
    package_id: int
    category: str
    description: Optional[str] = None
    amount: float = Field(..., gt=0)
    vendor: Optional[str] = None
    expense_date: datetime
    receipt_url: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    """Create expense schema"""
    pass


class ExpenseUpdate(BaseModel):
    """Update expense schema"""
    category: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    vendor: Optional[str] = None
    receipt_url: Optional[str] = None


class ExpenseResponse(ExpenseBase):
    """Expense response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============== Review Schemas ==============

class ReviewBase(BaseModel):
    """Base review schema"""
    booking_id: int
    rating: int = Field(..., ge=1, le=5)
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = None
    guide_rating: Optional[int] = Field(None, ge=1, le=5)
    would_recommend: bool = True


class ReviewCreate(ReviewBase):
    """Create review schema"""
    pass


class ReviewUpdate(BaseModel):
    """Update review schema"""
    rating: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    guide_rating: Optional[int] = None
    would_recommend: Optional[bool] = None


class ReviewResponse(ReviewBase):
    """Review response schema"""
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============== Authentication Schemas ==============

class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


# ============== Analytics Schemas ==============

class PackageAnalytics(BaseModel):
    """Package analytics"""
    package_id: int
    package_name: str
    total_revenue: float
    total_bookings: int
    total_participants: int
    average_rating: Optional[float]
    occupancy_rate: float
    profitability: float


class FinancialReport(BaseModel):
    """Financial report"""
    period_start: datetime
    period_end: datetime
    total_revenue: float
    total_expenses: float
    gross_profit: float
    profit_margin: float
    bookings_count: int
    average_booking_value: float
