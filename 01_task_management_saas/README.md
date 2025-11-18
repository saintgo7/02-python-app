# Task Management SaaS

## 📋 프로젝트 소개

**Task Management SaaS**는 사용자가 자신의 할일을 효율적으로 관리할 수 있는 웹 기반 서비스입니다. 이 프로젝트는 FastAPI를 기반으로 한 현대적인 REST API 설계 패턴을 따르며, 엔터프라이즈급 기능들을 포함하고 있습니다.

### 주요 특징
- ✅ JWT 기반 사용자 인증
- ✅ 개인별 할일 관리 (CRUD)
- ✅ 우선순위 및 마감일 설정
- ✅ 할일 완료 상태 추적
- ✅ RESTful API
- ✅ PostgreSQL 지원
- ✅ Docker & Docker Compose
- ✅ AWS 배포 가능
- ✅ 단위 테스트 포함

---

## 🛠 기술 스택

| 기술 | 버전 | 목적 |
|------|------|------|
| **FastAPI** | 0.104.1 | 웹 프레임워크 |
| **SQLAlchemy** | 2.0.23 | ORM |
| **PostgreSQL** | 15 | 데이터베이스 |
| **Python** | 3.11 | 프로그래밍 언어 |
| **JWT** | - | 인증 토큰 |
| **Docker** | - | 컨테이너화 |

---

## 📁 프로젝트 구조

```
01_task_management_saas/
├── main.py                    # FastAPI 애플리케이션 진입점
├── config.py                  # 설정 파일
├── requirements.txt           # Python 의존성
├── Dockerfile                 # Docker 이미지 정의
├── docker-compose.yml         # Docker Compose 설정
├── .env.example              # 환경 변수 예시
├── .gitignore                # Git 무시 파일
├── README.md                 # 프로젝트 문서
│
├── app/                      # 애플리케이션 코드
│   ├── __init__.py
│   ├── models.py            # SQLAlchemy 데이터베이스 모델
│   ├── schemas.py           # Pydantic 요청/응답 스키마
│   │
│   ├── core/                # 핵심 모듈
│   │   ├── __init__.py
│   │   ├── database.py      # 데이터베이스 연결
│   │   └── security.py      # JWT 인증 및 비밀번호 해싱
│   │
│   └── routes/              # API 라우트
│       ├── __init__.py
│       ├── auth.py          # 인증 관련 엔드포인트
│       ├── users.py         # 사용자 관리 엔드포인트
│       └── tasks.py         # 할일 관리 엔드포인트
│
└── tests/                   # 테스트 코드
    ├── __init__.py
    └── test_main.py         # 단위 테스트
```

---

## 🚀 설치 및 실행 방법

### 필수 요구사항
- Python 3.11 이상
- PostgreSQL 또는 SQLite
- Docker (선택사항)

### 방법 1: 로컬 개발 환경

#### 1단계: 저장소 클론 및 디렉토리 이동
```bash
cd 01_task_management_saas
```

#### 2단계: Python 가상환경 생성
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3단계: 의존성 설치
```bash
pip install -r requirements.txt
```

#### 4단계: 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 열어 필요한 값 수정
```

#### 5단계: 데이터베이스 초기화
```bash
python -c "from app.core.database import init_db; init_db()"
```

#### 6단계: 애플리케이션 실행
```bash
uvicorn main:app --reload
```

애플리케이션이 실행되면 http://localhost:8000 에 접속할 수 있습니다.

---

### 방법 2: Docker를 사용한 배포

#### 1단계: Docker 이미지 빌드
```bash
docker build -t task-management-saas .
```

#### 2단계: Docker Compose로 실행 (권장)
```bash
docker-compose up -d
```

이 명령어는 다음을 자동으로 설정합니다:
- PostgreSQL 데이터베이스 컨테이너
- FastAPI 애플리케이션 컨테이너
- 네트워크 및 데이터 볼륨

#### 3단계: 컨테이너 로그 확인
```bash
docker-compose logs -f app
```

#### 4단계: 서비스 중지
```bash
docker-compose down
```

---

## 📚 API 문서

### 자동 생성 문서
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 주요 API 엔드포인트

#### 인증 (Authentication)

**사용자 등록**
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

**응답 (201 Created)**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**사용자 로그인**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**응답 (200 OK)**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

#### 할일 관리 (Tasks)

**할일 목록 조회**
```http
GET /api/tasks?skip=0&limit=10&is_completed=false
Authorization: Bearer {access_token}
```

**응답 (200 OK)**
```json
[
  {
    "id": 1,
    "title": "프로젝트 제안서 작성",
    "description": "클라이언트를 위한 새로운 프로젝트 제안서",
    "is_completed": false,
    "priority": "high",
    "user_id": 1,
    "due_date": "2024-01-20T17:00:00",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
]
```

**할일 생성**
```http
POST /api/tasks
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "새로운 할일",
  "description": "상세 설명",
  "priority": "medium",
  "due_date": "2024-01-25T17:00:00"
}
```

**할일 업데이트**
```http
PUT /api/tasks/1
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "수정된 할일",
  "is_completed": true
}
```

**할일 삭제**
```http
DELETE /api/tasks/1
Authorization: Bearer {access_token}
```

#### 사용자 관리 (Users)

**현재 사용자 정보 조회**
```http
GET /api/users/me
Authorization: Bearer {access_token}
```

**사용자 정보 업데이트**
```http
PUT /api/users/me
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "full_name": "Updated Name",
  "password": "newpassword123"
}
```

**사용자 삭제**
```http
DELETE /api/users/me
Authorization: Bearer {access_token}
```

---

## 🧪 테스트 실행

### 단위 테스트 실행
```bash
# 모든 테스트 실행
pytest

# 상세 출력
pytest -v

# 특정 테스트 파일 실행
pytest tests/test_main.py

# 커버리지 생성
pytest --cov=app tests/
```

### 테스트 예시
```bash
$ pytest -v

tests/test_main.py::TestHealth::test_health_check PASSED
tests/test_main.py::TestAuth::test_register PASSED
tests/test_main.py::TestAuth::test_register_duplicate_email PASSED
tests/test_main.py::TestAuth::test_login PASSED

======================== 4 passed in 0.25s ========================
```

---

## 🌐 AWS에 배포하기

### 선택지 1: AWS EC2

#### 1단계: EC2 인스턴스 생성
```bash
# AWS Management Console에서:
# - Ubuntu 22.04 LTS 선택
# - t3.micro 또는 더 큰 인스턴스 선택
# - 보안 그룹에서 포트 8000 열기
```

#### 2단계: 인스턴스에 SSH 접속
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

#### 3단계: 필수 소프트웨어 설치
```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3-pip python3-venv postgresql postgresql-contrib docker.io

# 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER
```

#### 4단계: 애플리케이션 배포
```bash
git clone <repository-url>
cd 01_task_management_saas

# 환경 변수 설정
cp .env.example .env
nano .env  # AWS 환경에 맞게 수정

# Docker Compose로 실행
docker-compose up -d
```

#### 5단계: 역방향 프록시 설정 (Nginx)
```bash
# Nginx 설치
sudo apt-get install -y nginx

# Nginx 설정 파일 생성
sudo nano /etc/nginx/sites-available/task-app
```

**Nginx 설정 파일 예시:**
```nginx
upstream task_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://task_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# 설정 활성화
sudo ln -s /etc/nginx/sites-available/task-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 선택지 2: AWS Elastic Beanstalk

#### 1단계: Elastic Beanstalk CLI 설치
```bash
pip install awsebcli
```

#### 2단계: 애플리케이션 초기화
```bash
eb init -p python-3.11 task-management
```

#### 3단계: 환경 생성 및 배포
```bash
eb create task-app-env
eb deploy
```

#### 4단계: 환경 변수 설정
```bash
eb setenv DATABASE_URL=your-rds-url SECRET_KEY=your-secret
```

### 선택지 3: AWS RDS + ECS

참고: 이 방식은 더 복잡하지만 확장성이 뛰어납니다.

---

## 💰 수익화 방안

### 1. SaaS 모델
- **기본 요금제**: 무료 (제한된 기능)
- **프로 요금제**: $9.99/월 (무제한 할일, 팀 협업)
- **엔터프라이즈 요금제**: 맞춤형 가격

### 2. API 접근 제한
```python
# 요금제별 API 호출 제한
FREE_TIER: 1,000 requests/month
PRO_TIER: 100,000 requests/month
ENTERPRISE: unlimited
```

### 3. 추가 기능 판매
- 할일 자동 동기화 ($2.99/월)
- 팀 협업 기능 ($4.99/월)
- 고급 분석 대시보드 ($6.99/월)

### 4. 엔터프라이즈 지원
- 1:1 기술 지원
- 맞춤형 통합
- SLA 보장
- 월별 상담

### 5. 수익 예측 (연간)
```
가정:
- 유저 10,000명
- 30% 전환율 (프로 요금제)
- 평균 요금: $9.99/월

월간 수익: 3,000명 × $9.99 = $29,970
연간 수익: $359,640
```

---

## 🔒 보안 고려사항

### 1. 비밀번호 보안
- ✅ bcrypt를 사용한 비밀번호 해싱
- ✅ 최소 8자 이상 권장
- ✅ 특수 문자 포함 권장

### 2. JWT 토큰
- ✅ 30분 만료 시간
- ✅ HTTPS 필수 (프로덕션)
- ✅ 환경 변수에서 SECRET_KEY 관리

### 3. 데이터베이스 보안
- ✅ 최소 권한 원칙 적용
- ✅ 정기적인 백업
- ✅ SSL 연결 사용

### 4. API 보안
- ✅ CORS 설정
- ✅ Rate limiting 추가 권장
- ✅ 입력 검증 (Pydantic)

### 보안 체크리스트
```
□ 프로덕션에서 DEBUG = False 설정
□ SECRET_KEY를 강력한 값으로 변경
□ HTTPS 활성화
□ 데이터베이스 정기 백업
□ 로깅 및 모니터링 설정
□ 주기적인 의존성 업데이트
```

---

## 📊 모니터링 및 로깅

### 구조 로깅 추가 예시
```python
# app/core/logging.py
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def info(self, message, **kwargs):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            **kwargs
        }
        self.logger.info(json.dumps(log_data))
```

### CloudWatch 통합
```python
# .env
CLOUDWATCH_LOG_GROUP=/aws/task-management
CLOUDWATCH_LOG_STREAM=app-logs
```

---

## 🤝 기여 가이드

버그 리포트나 기능 제안은 GitHub Issues로 제출해주세요.

### 개발 환경 설정
```bash
# 코드 스타일 검사
pip install black flake8
black app/
flake8 app/

# 타입 체크
pip install mypy
mypy app/
```

---

## 📄 라이선스

MIT License

---

## 📞 지원

- 📧 이메일: support@task-management.com
- 📚 문서: https://docs.task-management.com
- 🐛 이슈: GitHub Issues

---

## 🗓️ 로드맵

- [ ] 팀 협업 기능
- [ ] 모바일 앱
- [ ] 캘린더 통합 (Google Calendar, Outlook)
- [ ] 알림 기능 (이메일, Slack)
- [ ] 분석 대시보드
- [ ] GraphQL API
- [ ] 웹훅 지원

---

**마지막 업데이트**: 2024년 1월 15일
