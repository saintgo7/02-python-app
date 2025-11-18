# 🌍 Travel Agency ERP System

완전한 기능을 갖춘 여행사 관리 ERP 시스템입니다. FastAPI와 SQLAlchemy를 기반으로 만들어졌습니다.

## 📋 목차

- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [프로젝트 구조](#프로젝트-구조)
- [설치 및 실행](#설치-및-실행)
- [API 엔드포인트](#api-엔드포인트)
- [데이터베이스 모델](#데이터베이스-모델)
- [인증 및 보안](#인증-및-보안)
- [사용 예시](#사용-예시)
- [개발](#개발)
- [라이센스](#라이센스)

---

## 🎯 주요 기능

### 👥 사용자 관리
- 회원가입 및 로그인
- 역할 기반 접근 제어 (RBAC)
  - 관리자 (Admin)
  - 직원 (Staff)
  - 가이드 (Guide)
  - 고객 (Customer)
- 사용자 프로필 관리
- 계정 비활성화

### 🌍 여행 패키지 관리
- 패키지 생성, 수정, 삭제
- 목적지별 분류
- 가격 설정
- 최대 참가자 수 관리
- 일정 및 포함 서비스 상세 정보
- 난이도 레벨 설정 (쉬움, 중간, 어려움)

### 📅 예약 시스템
- 실시간 가용성 확인
- 예약 생성 및 수정
- 예약 상태 추적
  - 대기중 (Pending)
  - 확정됨 (Confirmed)
  - 완료됨 (Completed)
  - 취소됨 (Cancelled)
- 특별 요청사항 기록

### 💳 결제 관리
- 다양한 결제 수단 지원
  - 신용카드
  - 은행 이체
  - 현금
- 부분 결제 처리
- 결제 상태 추적
- 거래 ID 관리
- 미수금 추적

### 👨‍🏫 가이드 관리
- 가이드 일정 관리
- 일일 요금 설정
- 가이드별 성능 추적
- 가이드 평가 시스템

### 💰 비용 추적
- 비용 카테고리 분류
  - 숙박
  - 식사
  - 교통
  - 허가서
  - 기타
- 영수증 관리
- 공급업체 정보 기록
- 수익성 분석

### ⭐ 리뷰 및 평가
- 고객 리뷰
- 별점 평가 (1-5점)
- 가이드별 별도 평가
- 추천 여부 기록

### 📊 분석 및 리포팅
- 패키지별 매출 분석
- 점유율 계산
- 재정 리포트
  - 수익
  - 비용
  - 수익성
  - 이윤율
- 대시보드 요약

---

## 🛠️ 기술 스택

### 백엔드
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **ORM**: SQLAlchemy 2.0.23
- **Validation**: Pydantic 2.5.0

### 데이터베이스
- **Production**: PostgreSQL
- **Development**: SQLite

### 인증 & 보안
- **Password Hashing**: Bcrypt
- **Token**: JWT (Python-Jose)
- **Password Context**: Passlib

### 테스트
- **Framework**: Pytest 7.4.3
- **HTTP Client**: HTTPx 0.25.2

### 옵션 기능
- **Caching**: Redis
- **Monitoring**: Prometheus
- **Logging**: Python-JSON-Logger

---

## 📂 프로젝트 구조

```
421_travel_agency_erp/
├── main.py                          # 애플리케이션 진입점
├── config.py                        # 설정 관리 (개선된 보안)
├── requirements.txt                 # 의존성
├── .env.example                     # 환경변수 예제
├── alembic.ini                      # 데이터베이스 마이그레이션 설정
│
├── app/
│   ├── __init__.py
│   ├── config.py                    # 설정 모듈 재내보내기
│   ├── models.py                    # SQLAlchemy 모델 (8개)
│   ├── schemas.py                   # Pydantic 검증 스키마
│   │
│   ├── core/
│   │   ├── database.py              # 데이터베이스 설정
│   │   ├── security.py              # 인증 & 보안 (개선됨)
│   │   ├── logging.py               # 로깅 설정
│   │   ├── middleware.py            # 요청/응답 미들웨어
│   │   └── errors.py                # 커스텀 예외
│   │
│   ├── services/                    # 비즈니스 로직 (Service 레이어)
│   │   ├── user_service.py
│   │   ├── booking_service.py
│   │   ├── payment_service.py
│   │   └── package_service.py
│   │
│   ├── routes/                      # API 엔드포인트
│   │   ├── auth.py                  # 인증
│   │   ├── users.py                 # 사용자 관리
│   │   ├── packages.py              # 패키지 관리
│   │   ├── bookings.py              # 예약 관리
│   │   ├── payments.py              # 결제 관리
│   │   ├── expenses.py              # 비용 추적
│   │   ├── guides.py                # 가이드 관리
│   │   ├── reviews.py               # 리뷰 관리
│   │   └── analytics.py             # 분석 & 리포팅
│   │
│   └── utils/
│       ├── validators.py             # 검증 유틸리티
│       └── helpers.py                # 헬퍼 함수
│
├── tests/
│   ├── conftest.py                  # 테스트 설정
│   ├── test_auth.py                 # 인증 테스트
│   └── test_packages.py             # 패키지 테스트
│
├── migrations/
│   └── versions/                    # 데이터베이스 마이그레이션
│
└── README.md                        # 이 파일
```

---

## 🚀 설치 및 실행

### 필수 요구사항
- Python 3.8+
- PostgreSQL (또는 SQLite for 개발)
- pip 또는 pipenv

### 1. 저장소 클론
```bash
git clone https://github.com/yourusername/travel-agency-erp.git
cd 421_travel_agency_erp
```

### 2. 가상 환경 생성
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정
```bash
cp .env.example .env
```

`.env` 파일을 열어서 다음 항목을 설정하세요:

```env
# 필수 (운영 환경)
SECRET_KEY=your-secret-key-here-minimum-32-chars
DATABASE_URL=postgresql://user:password@localhost:5432/travel_erp

# 옵션
REDIS_URL=redis://localhost:6379
AWS_REGION=us-east-1
STRIPE_API_KEY=sk_test_xxxxx
```

### 5. 데이터베이스 마이그레이션
```bash
# Alembic을 사용한 마이그레이션
alembic upgrade head
```

### 6. 애플리케이션 실행
```bash
# 개발 모드
python main.py

# 또는 uvicorn 사용
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. API 문서 접속
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 📡 API 엔드포인트

### 인증 (Authentication)
```
POST   /auth/register          # 회원가입
POST   /auth/login             # 로그인
GET    /auth/me                # 현재 사용자 정보
```

### 사용자 (Users)
```
GET    /users/                 # 사용자 목록 (관리자)
GET    /users/{user_id}        # 사용자 상세
PUT    /users/{user_id}        # 사용자 수정
GET    /users/guides/list      # 가이드 목록
PATCH  /users/{user_id}/deactivate  # 사용자 비활성화 (관리자)
```

### 여행 패키지 (Travel Packages)
```
GET    /packages/              # 패키지 목록
GET    /packages/{package_id}  # 패키지 상세
POST   /packages/              # 패키지 생성 (관리자)
PUT    /packages/{package_id}  # 패키지 수정 (관리자)
DELETE /packages/{package_id}  # 패키지 삭제 (관리자)
```

### 예약 (Bookings)
```
GET    /bookings/              # 내 예약 목록
GET    /bookings/{booking_id}  # 예약 상세
POST   /bookings/              # 예약 생성
PUT    /bookings/{booking_id}  # 예약 수정
DELETE /bookings/{booking_id}  # 예약 취소
```

### 결제 (Payments)
```
GET    /payments/              # 결제 목록
GET    /payments/{payment_id}  # 결제 상세
POST   /payments/              # 결제 생성
PUT    /payments/{payment_id}  # 결제 수정
```

### 비용 (Expenses)
```
GET    /expenses/              # 비용 목록 (관리자)
GET    /expenses/{expense_id}  # 비용 상세 (관리자)
POST   /expenses/              # 비용 추가 (관리자)
PUT    /expenses/{expense_id}  # 비용 수정 (관리자)
DELETE /expenses/{expense_id}  # 비용 삭제 (관리자)
GET    /expenses/package/{package_id}/summary  # 패키지 비용 요약
```

### 가이드 (Guides)
```
GET    /guides/schedules       # 가이드 일정 목록 (관리자)
GET    /guides/schedules/{schedule_id}  # 일정 상세
POST   /guides/schedules       # 일정 생성 (관리자)
PUT    /guides/schedules/{schedule_id}  # 일정 수정 (관리자)
DELETE /guides/schedules/{schedule_id}  # 일정 삭제 (관리자)
GET    /guides/{guide_id}/my-schedules  # 내 일정
```

### 리뷰 (Reviews)
```
GET    /reviews/               # 리뷰 목록
GET    /reviews/{review_id}    # 리뷰 상세
POST   /reviews/               # 리뷰 작성
PUT    /reviews/{review_id}    # 리뷰 수정
DELETE /reviews/{review_id}    # 리뷰 삭제
GET    /reviews/booking/{booking_id}/review  # 예약 리뷰
```

### 분석 (Analytics)
```
GET    /analytics/packages/{package_id}      # 패키지 분석
GET    /analytics/financial-report           # 재정 리포트
GET    /analytics/dashboard-summary          # 대시보드 요약 (관리자)
```

---

## 🗄️ 데이터베이스 모델

### 1. User (사용자)
```python
- id (PK)
- email (UNIQUE)
- username (UNIQUE)
- hashed_password
- full_name
- phone
- role: admin, staff, guide, customer
- is_active
- created_at, updated_at
```

### 2. TravelPackage (여행 패키지)
```python
- id (PK)
- name
- description
- destination
- duration_days
- price_per_person
- max_participants
- included_services
- itinerary
- difficulty_level
- start_date, end_date
- is_active
- created_at, updated_at
```

### 3. Booking (예약)
```python
- id (PK)
- package_id (FK)
- customer_id (FK)
- number_of_participants
- total_price
- status: pending, confirmed, completed, cancelled
- special_requests
- booking_date, confirmation_date
- created_at, updated_at
```

### 4. Payment (결제)
```python
- id (PK)
- booking_id (FK)
- amount
- payment_method
- status: unpaid, partial, paid, refunded
- transaction_id
- payment_date, due_date
- notes
- created_at, updated_at
```

### 5. GuideSchedule (가이드 일정)
```python
- id (PK)
- guide_id (FK)
- package_id (FK)
- start_date, end_date
- daily_rate
- status
- notes
- created_at, updated_at
```

### 6. Expense (비용)
```python
- id (PK)
- package_id (FK)
- category
- description
- amount
- vendor
- expense_date
- receipt_url
- created_at, updated_at
```

### 7. Review (리뷰)
```python
- id (PK)
- booking_id (FK)
- author_id (FK)
- rating (1-5)
- title
- content
- guide_rating
- would_recommend
- created_at, updated_at
```

---

## 🔐 인증 및 보안

### JWT 토큰 기반 인증
```python
# 로그인
POST /auth/login
{
  "email": "user@example.com",
  "password": "password123"
}

# 응답
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}

# 인증된 요청
GET /auth/me
Headers: Authorization: Bearer eyJhbGc...
```

### 보안 기능
- ✅ 강력한 비밀번호 해싱 (Bcrypt)
- ✅ JWT 토큰 기반 인증
- ✅ CORS 설정
- ✅ 보안 헤더 (X-Content-Type-Options, X-Frame-Options 등)
- ✅ HTTPS 강제화 (Strict-Transport-Security)
- ✅ 역할 기반 접근 제어 (RBAC)
- ✅ 환경변수 기반 SECRET_KEY (운영 환경)
- ✅ 요청 ID 추적
- ✅ 상세 로깅

### 암호 요구사항
- 최소 8자
- 대문자 포함
- 소문자 포함
- 숫자 포함
- 특수 문자 포함

---

## 💡 사용 예시

### 1. 사용자 등록
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d {
    "email": "user@example.com",
    "username": "john_doe",
    "password": "SecurePass123!",
    "full_name": "John Doe",
    "role": "customer"
  }
```

### 2. 로그인
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d {
    "email": "user@example.com",
    "password": "SecurePass123!"
  }
```

### 3. 여행 패키지 조회
```bash
curl -X GET "http://localhost:8000/packages/" \
  -H "Content-Type: application/json"
```

### 4. 예약 생성
```bash
curl -X POST "http://localhost:8000/bookings/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d {
    "package_id": 1,
    "number_of_participants": 2,
    "special_requests": "Window seat preferred"
  }
```

### 5. 리뷰 작성
```bash
curl -X POST "http://localhost:8000/reviews/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d {
    "booking_id": 1,
    "rating": 5,
    "title": "Amazing experience",
    "content": "Great package, wonderful guide!",
    "guide_rating": 5,
    "would_recommend": true
  }
```

---

## 👨‍💻 개발

### 테스트 실행
```bash
# 모든 테스트
pytest

# 특정 테스트 파일
pytest tests/test_auth.py

# 상세 출력
pytest -v

# 커버리지 포함
pytest --cov=app
```

### 코드 스타일
```bash
# Black으로 포맷팅
black app/

# Flake8로 린팅
flake8 app/

# isort로 import 정렬
isort app/
```

### 데이터베이스 마이그레이션
```bash
# 새 마이그레이션 생성
alembic revision --autogenerate -m "Add new column"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 되돌리기
alembic downgrade -1
```

---

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에서 배포됩니다.

---

## 🤝 기여

버그 리포트, 기능 요청, Pull Request를 환영합니다!

---

## 📧 연락처

- 이메일: support@travelagency.com
- 웹사이트: www.travelagency.com

---

## 🙏 감사의 말

이 프로젝트는 다음의 훌륭한 라이브러리들을 사용합니다:

- FastAPI
- SQLAlchemy
- Pydantic
- Python-Jose
- Passlib
- Bcrypt

---

**최종 업데이트**: 2024년 11월 18일
**버전**: 1.0.0
**상태**: Production Ready ✅
