# 🚀 배포 가이드

Travel Agency ERP 시스템 배포 방법입니다.

## 📋 목차

- [환경 설정](#환경-설정)
- [Docker 배포](#docker-배포)
- [AWS 배포](#aws-배포)
- [성능 최적화](#성능-최적화)
- [모니터링](#모니터링)
- [문제 해결](#문제-해결)

---

## 🔧 환경 설정

### 운영 환경 (Production)

#### 필수 환경변수
```env
# 애플리케이션
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO

# 보안 (반드시 변경!)
SECRET_KEY=your-strong-secret-key-here-minimum-32-chars

# 데이터베이스
DATABASE_URL=postgresql://user:password@db-host:5432/travel_erp
DATABASE_POOL_SIZE=20
DATABASE_POOL_RECYCLE=3600

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Redis (선택사항)
REDIS_URL=redis://cache-host:6379/0

# AWS (선택사항)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key-id
AWS_SECRET_ACCESS_KEY=your-secret-key

# 이메일 (선택사항)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SENDER_EMAIL=noreply@yourdomain.com
```

#### 서버 요구사항
- CPU: 2+ cores
- RAM: 2GB+
- Disk: 10GB+
- OS: Ubuntu 20.04+, CentOS 8+, AWS Linux 2+

---

## 🐳 Docker 배포

### Dockerfile

```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  # FastAPI Application
  api:
    build: .
    container_name: travel_erp_api
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://postgres:${DB_PASSWORD}@db:5432/travel_erp
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    networks:
      - travel_network
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: travel_erp_db
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=travel_erp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - travel_network
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: travel_erp_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - travel_network
    restart: always
    command: redis-server --appendonly yes

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: travel_erp_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    networks:
      - travel_network
    restart: always

volumes:
  postgres_data:
  redis_data:

networks:
  travel_network:
    driver: bridge
```

### 배포 명령어

```bash
# 이미지 빌드
docker build -t travel-erp:latest .

# 컨테이너 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f api

# 데이터베이스 마이그레이션
docker-compose exec api alembic upgrade head

# 컨테이너 종료
docker-compose down
```

---

## ☁️ AWS 배포

### 1. AWS RDS PostgreSQL 설정

```bash
# RDS 데이터베이스 생성
aws rds create-db-instance \
  --db-instance-identifier travel-erp-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username postgres \
  --master-user-password YourPassword123! \
  --allocated-storage 20 \
  --publicly-accessible false
```

### 2. ElastiCache Redis 설정

```bash
# ElastiCache 클러스터 생성
aws elasticache create-cache-cluster \
  --cache-cluster-id travel-erp-cache \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1
```

### 3. EC2 인스턴스 배포

```bash
# EC2 인스턴스에 SSH 접속
ssh -i your-key.pem ec2-user@your-instance-ip

# 저장소 클론
git clone https://github.com/yourusername/travel-agency-erp.git
cd travel-agency-erp

# 환경 설정
cp .env.example .env
nano .env  # AWS RDS, ElastiCache 주소 입력

# 서비스 시작
sudo systemctl start travel-erp
sudo systemctl enable travel-erp
```

### 4. Elastic Beanstalk 배포

```bash
# EB CLI 설치
pip install awsebcli

# EB 초기화
eb init -p "Python 3.11" travel-erp

# 환경 생성
eb create production

# 배포
eb deploy

# 로그 확인
eb logs
```

### 5. CloudFront CDN 설정

```bash
# 정적 파일 S3에 업로드
aws s3 cp static/ s3://your-bucket/static/ --recursive

# CloudFront 배포 생성 (AWS 콘솔에서)
# S3: your-bucket
# Origin: api.yourdomain.com
# Cache behaviors: /docs*, /redoc*, /openapi.json
```

---

## ⚡ 성능 최적화

### 1. 데이터베이스 최적화

```sql
-- 인덱스 생성
CREATE INDEX idx_bookings_customer_id ON bookings(customer_id);
CREATE INDEX idx_bookings_package_id ON bookings(package_id);
CREATE INDEX idx_payments_booking_id ON payments(booking_id);
CREATE INDEX idx_expenses_package_id ON expenses(package_id);

-- 통계 업데이트
ANALYZE;

-- 쿼리 최적화 확인
EXPLAIN ANALYZE SELECT * FROM bookings WHERE customer_id = 1;
```

### 2. Redis 캐싱

```python
# 설정 예시
from redis import Redis

redis = Redis(host='redis-host', port=6379, db=0)

# 캐시 설정
CACHE_TTL = 3600  # 1시간

@router.get("/packages/")
async def list_packages(db: Session, redis: Redis):
    # 캐시 확인
    cached = await redis.get("packages:all")
    if cached:
        return json.loads(cached)

    # 데이터 조회
    packages = db.query(TravelPackage).all()

    # 캐시 저장
    await redis.setex(
        "packages:all",
        CACHE_TTL,
        json.dumps([p.to_dict() for p in packages])
    )

    return packages
```

### 3. 데이터베이스 연결 풀

```python
# settings.py에서 설정
DATABASE_POOL_SIZE = 20  # 동시 연결 수
DATABASE_POOL_RECYCLE = 3600  # 연결 재사용 주기
```

### 4. 응답 압축

```python
from fastapi.middleware.gzip import GZIPMiddleware

app.add_middleware(GZIPMiddleware, minimum_size=1000)
```

---

## 📊 모니터링

### 1. Prometheus & Grafana

```python
# main.py에 추가
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator import Instrumentator

# Prometheus 자동 계측
Instrumentator().instrument(app).expose(app)

# 커스텀 메트릭
request_count = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint']
)

request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)
```

### 2. 로깅 설정

```python
# Structured logging
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
```

### 3. 헬스 체크

```bash
# 정기적으로 확인
curl http://api.yourdomain.com/health

# CloudWatch 알람 설정
aws cloudwatch put-metric-alarm \
  --alarm-name api-health-check \
  --alarm-description "API health check alarm" \
  --metric-name APIHealthCheck \
  --namespace CustomMetrics
```

---

## 🔧 문제 해결

### 1. 데이터베이스 연결 오류

```bash
# PostgreSQL 연결 테스트
psql -h db-host -U postgres -d travel_erp

# 로그 확인
docker-compose logs db

# 연결 풀 재설정
# 환경변수 조정: DATABASE_POOL_SIZE, DATABASE_POOL_RECYCLE
```

### 2. 메모리 부족

```bash
# 메모리 사용량 확인
docker stats

# Gunicorn 워커 수 조정
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Redis 메모리 정리
redis-cli FLUSHALL
```

### 3. 느린 응답

```bash
# 느린 쿼리 로그 활성화
# PostgreSQL
SET log_min_duration_statement = 1000;

# Query 분석
EXPLAIN ANALYZE SELECT * FROM bookings;

# 인덱스 추가
CREATE INDEX idx_booking_date ON bookings(booking_date DESC);
```

### 4. SSL 인증서 오류

```bash
# Let's Encrypt 인증서 갱신
certbot renew --force-renewal

# Nginx 설정 확인
nginx -t

# 재시작
systemctl restart nginx
```

---

## 📈 확장성

### 1. 수평 확장 (Horizontal Scaling)

```yaml
# Docker Compose로 API 인스턴스 여러 개 실행
services:
  api-1:
    # API 인스턴스 1
  api-2:
    # API 인스턴스 2
  api-3:
    # API 인스턴스 3
  nginx:
    # 로드 밸런싱
```

### 2. 데이터베이스 복제 (Replication)

```bash
# Primary-Replica 구성
# Primary: 쓰기 작업
# Replica: 읽기 작업

# SQLAlchemy 설정
READ_DB_URL = "postgresql://user:password@read-replica:5432/travel_erp"
```

### 3. 마이크로서비스 분리

```
API Gateway
    ├── User Service
    ├── Package Service
    ├── Booking Service
    ├── Payment Service
    └── Analytics Service
```

---

## 체크리스트

배포 전 확인사항:

- [ ] 환경변수 설정 확인
- [ ] 데이터베이스 마이그레이션 완료
- [ ] SSL 인증서 설치
- [ ] 백업 정책 수립
- [ ] 모니터링 설정
- [ ] 로그 수집 설정
- [ ] 알림 규칙 설정
- [ ] 보안 그룹/방화벽 설정
- [ ] 부하 테스트 완료
- [ ] 성능 벤치마크 측정

---

**최종 업데이트**: 2024년 11월 18일
**상태**: Production Ready ✅
