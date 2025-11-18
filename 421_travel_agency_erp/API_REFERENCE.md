# 📚 API 레퍼런스

Travel Agency ERP System의 완전한 API 문서입니다.

## 🔐 인증

모든 보호된 엔드포인트는 JWT 토큰을 필요로 합니다.

### 토큰 획득
```
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}

Response (200 OK):
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 인증된 요청
```
GET /protected-endpoint
Authorization: Bearer {access_token}
```

---

## 👤 인증 엔드포인트

### 회원가입
```
POST /auth/register
Content-Type: application/json

Request:
{
  "email": "user@example.com",
  "username": "john_doe",
  "password": "SecurePassword123!",
  "full_name": "John Doe",
  "phone": "+1-234-567-8900",
  "role": "customer"
}

Response (200 OK):
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "phone": "+1-234-567-8900",
  "role": "customer",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 로그인
```
POST /auth/login
Content-Type: application/json

Request:
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}

Response (200 OK):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 현재 사용자 정보
```
GET /auth/me
Authorization: Bearer {token}

Response (200 OK):
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "phone": "+1-234-567-8900",
  "role": "customer",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

---

## 🌍 여행 패키지 엔드포인트

### 패키지 목록
```
GET /packages/
Query Parameters:
  - skip: integer (default: 0)
  - limit: integer (default: 10, max: 100)
  - destination: string (optional)
  - active_only: boolean (default: true)

Response (200 OK):
[
  {
    "id": 1,
    "name": "Paris Summer Package",
    "description": "Experience the beauty of Paris...",
    "destination": "Paris, France",
    "duration_days": 7,
    "price_per_person": 1500.00,
    "max_participants": 30,
    "included_services": "Hotel, Food, Transport, Guide",
    "itinerary": "Day 1: Arrival...",
    "difficulty_level": "easy",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### 패키지 상세
```
GET /packages/{package_id}

Response (200 OK):
{
  "id": 1,
  "name": "Paris Summer Package",
  ...
}

Errors:
- 404 Not Found: Package not found
```

### 패키지 생성 (관리자 전용)
```
POST /packages/
Authorization: Bearer {admin_token}
Content-Type: application/json

Request:
{
  "name": "Tokyo Winter Package",
  "description": "Explore Tokyo in winter...",
  "destination": "Tokyo, Japan",
  "duration_days": 10,
  "price_per_person": 2000.00,
  "max_participants": 25,
  "included_services": "Hotel, Food, Transport, Guide",
  "itinerary": "Day 1: Arrival...",
  "difficulty_level": "moderate",
  "start_date": "2024-12-01T00:00:00Z",
  "end_date": "2024-12-10T00:00:00Z"
}

Response (200 OK):
{
  "id": 2,
  "name": "Tokyo Winter Package",
  ...
}

Errors:
- 403 Forbidden: Admin access required
```

### 패키지 수정 (관리자 전용)
```
PUT /packages/{package_id}
Authorization: Bearer {admin_token}
Content-Type: application/json

Request:
{
  "name": "Tokyo Winter Package - Updated",
  "price_per_person": 2100.00
}

Response (200 OK):
{
  "id": 2,
  "name": "Tokyo Winter Package - Updated",
  ...
}
```

### 패키지 삭제 (관리자 전용)
```
DELETE /packages/{package_id}
Authorization: Bearer {admin_token}

Response (204 No Content)

Errors:
- 404 Not Found
- 403 Forbidden
```

---

## 📅 예약 엔드포인트

### 예약 목록
```
GET /bookings/
Authorization: Bearer {token}
Query Parameters:
  - skip: integer (default: 0)
  - limit: integer (default: 10, max: 100)
  - status: string (pending, confirmed, completed, cancelled)

Response (200 OK):
[
  {
    "id": 1,
    "package_id": 1,
    "customer_id": 1,
    "number_of_participants": 2,
    "total_price": 3000.00,
    "status": "confirmed",
    "special_requests": "Window seat preferred",
    "booking_date": "2024-01-15T10:30:00Z",
    "confirmation_date": "2024-01-15T11:00:00Z",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
  }
]
```

### 예약 상세
```
GET /bookings/{booking_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "id": 1,
  ...
}

Errors:
- 404 Not Found
- 403 Forbidden: Can only view own bookings
```

### 예약 생성
```
POST /bookings/
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "package_id": 1,
  "number_of_participants": 2,
  "special_requests": "Window seat preferred"
}

Response (200 OK):
{
  "id": 1,
  "package_id": 1,
  "customer_id": 1,
  "number_of_participants": 2,
  "total_price": 3000.00,
  "status": "pending",
  ...
}

Errors:
- 400 Bad Request: Package is fully booked
- 404 Not Found: Package not found
```

### 예약 수정
```
PUT /bookings/{booking_id}
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "number_of_participants": 3,
  "special_requests": "Window seat and vegetarian meals"
}

Response (200 OK):
{
  "id": 1,
  ...
}

Errors:
- 400 Bad Request: Can only update pending bookings
- 403 Forbidden
```

### 예약 취소
```
DELETE /bookings/{booking_id}
Authorization: Bearer {token}

Response (204 No Content)
```

---

## 💳 결제 엔드포인트

### 결제 목록
```
GET /payments/
Authorization: Bearer {token}
Query Parameters:
  - skip: integer
  - limit: integer
  - booking_id: integer

Response (200 OK):
[
  {
    "id": 1,
    "booking_id": 1,
    "amount": 1000.00,
    "payment_method": "credit_card",
    "status": "paid",
    "transaction_id": "txn_123456",
    "payment_date": "2024-01-16T00:00:00Z",
    "due_date": "2024-02-01T00:00:00Z",
    "notes": "Payment received",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-16T10:30:00Z"
  }
]
```

### 결제 생성
```
POST /payments/
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "booking_id": 1,
  "amount": 1000.00,
  "payment_method": "credit_card",
  "due_date": "2024-02-01T00:00:00Z",
  "notes": "First payment"
}

Response (200 OK):
{
  "id": 1,
  ...
}

Errors:
- 404 Not Found: Booking not found
- 403 Forbidden: Can only pay for own bookings
```

---

## 💰 비용 엔드포인트

### 비용 목록 (관리자 전용)
```
GET /expenses/
Authorization: Bearer {admin_token}
Query Parameters:
  - skip: integer
  - limit: integer
  - package_id: integer
  - category: string

Response (200 OK):
[
  {
    "id": 1,
    "package_id": 1,
    "category": "accommodation",
    "description": "Hotel stay",
    "amount": 5000.00,
    "vendor": "Hilton Hotel",
    "expense_date": "2024-01-01T00:00:00Z",
    "receipt_url": "https://...",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### 비용 생성 (관리자 전용)
```
POST /expenses/
Authorization: Bearer {admin_token}
Content-Type: application/json

Request:
{
  "package_id": 1,
  "category": "accommodation",
  "description": "Hotel stay",
  "amount": 5000.00,
  "vendor": "Hilton Hotel",
  "expense_date": "2024-01-01T00:00:00Z",
  "receipt_url": "https://..."
}

Response (200 OK):
{
  "id": 1,
  ...
}
```

### 패키지 비용 요약 (관리자 전용)
```
GET /expenses/package/{package_id}/summary
Authorization: Bearer {admin_token}

Response (200 OK):
{
  "package_id": 1,
  "total_expenses": 15000.00,
  "by_category": {
    "accommodation": 5000.00,
    "food": 4000.00,
    "transport": 3000.00,
    "permits": 2000.00,
    "other": 1000.00
  },
  "expense_count": 15
}
```

---

## 👨‍🏫 가이드 엔드포인트

### 가이드 일정 목록 (관리자 전용)
```
GET /guides/schedules
Authorization: Bearer {admin_token}
Query Parameters:
  - skip: integer
  - limit: integer
  - guide_id: integer
  - status: string

Response (200 OK):
[
  {
    "id": 1,
    "guide_id": 5,
    "package_id": 1,
    "start_date": "2024-01-01T00:00:00Z",
    "end_date": "2024-01-10T00:00:00Z",
    "daily_rate": 200.00,
    "status": "scheduled",
    "notes": "French-speaking guide",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### 가이드 일정 생성 (관리자 전용)
```
POST /guides/schedules
Authorization: Bearer {admin_token}
Content-Type: application/json

Request:
{
  "guide_id": 5,
  "package_id": 1,
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-01-10T00:00:00Z",
  "daily_rate": 200.00,
  "notes": "French-speaking guide"
}

Response (200 OK):
{
  "id": 1,
  ...
}
```

### 내 일정 조회 (가이드용)
```
GET /guides/{guide_id}/my-schedules
Authorization: Bearer {guide_token}

Response (200 OK):
[
  {
    "id": 1,
    ...
  }
]
```

---

## ⭐ 리뷰 엔드포인트

### 리뷰 목록
```
GET /reviews/
Query Parameters:
  - skip: integer
  - limit: integer
  - booking_id: integer
  - min_rating: integer (1-5)

Response (200 OK):
[
  {
    "id": 1,
    "booking_id": 1,
    "author_id": 1,
    "rating": 5,
    "title": "Amazing experience!",
    "content": "Great package and wonderful guide...",
    "guide_rating": 5,
    "would_recommend": true,
    "created_at": "2024-01-20T00:00:00Z",
    "updated_at": "2024-01-20T00:00:00Z"
  }
]
```

### 리뷰 작성
```
POST /reviews/
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "booking_id": 1,
  "rating": 5,
  "title": "Amazing experience!",
  "content": "Great package and wonderful guide...",
  "guide_rating": 5,
  "would_recommend": true
}

Response (200 OK):
{
  "id": 1,
  ...
}

Errors:
- 400 Bad Request: Review already exists
- 403 Forbidden: Can only review own bookings
```

---

## 📊 분석 엔드포인트

### 패키지 분석 (관리자 전용)
```
GET /analytics/packages/{package_id}
Authorization: Bearer {admin_token}

Response (200 OK):
{
  "package_id": 1,
  "package_name": "Paris Summer Package",
  "total_revenue": 45000.00,
  "total_bookings": 15,
  "total_participants": 30,
  "average_rating": 4.8,
  "occupancy_rate": 100.0,
  "profitability": 15000.00
}
```

### 재정 리포트 (관리자 전용)
```
GET /analytics/financial-report
Authorization: Bearer {admin_token}
Query Parameters:
  - period_days: integer (default: 30, max: 365)

Response (200 OK):
{
  "period_start": "2023-12-19T00:00:00Z",
  "period_end": "2024-01-18T00:00:00Z",
  "total_revenue": 100000.00,
  "total_expenses": 65000.00,
  "gross_profit": 35000.00,
  "profit_margin": 35.0,
  "bookings_count": 20,
  "average_booking_value": 5000.00
}
```

### 대시보드 요약 (관리자 전용)
```
GET /analytics/dashboard-summary
Authorization: Bearer {admin_token}

Response (200 OK):
{
  "total_revenue": 500000.00,
  "total_bookings": 100,
  "pending_payments": 50000.00,
  "total_packages": 10,
  "active_bookings": 25,
  "timestamp": "2024-01-18T10:30:00Z"
}
```

---

## ❌ 에러 응답

### 400 Bad Request
```json
{
  "detail": "Validation error or invalid input"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 409 Conflict
```json
{
  "detail": "Email already registered"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

**마지막 업데이트**: 2024년 11월 18일
**버전**: 1.0.0
