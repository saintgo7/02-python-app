# 39_food_calorie_estimator

## 📋 프로젝트 소개

**39_food_calorie_estimator**는 Food calorie estimation from images

### 주요 기능
- ✅ Food Recognition
- ✅ Portion Estimation
- ✅ Nutritional Data


## 🛠 기술 스택

- **Framework**: TENSORFLOW
- **Database**: SQLITE
- **Python**: 3.11+
- **Docker**: Supported

## 📁 프로젝트 구조

```
39_food_calorie_estimator/
├── main.py                    # 애플리케이션 진입점
├── requirements.txt           # Python 의존성
├── Dockerfile                 # Docker 이미지
├── .env.example              # 환경 변수 예시
├── .gitignore                # Git 무시 파일
├── README.md                 # 프로젝트 문서
├── app/                      # 애플리케이션 코드
│   ├── __init__.py
│   ├── models.py
│   ├── schemas.py
│   └── core/
└── tests/                    # 테스트
    ├── __init__.py
    └── test_main.py
```

## 🚀 설치 및 실행

### 필수 요구사항
- Python 3.11+
- pip
- Docker (선택사항)

### 로컬 환경 설정

#### 1단계: 저장소 클론
```bash
cd 39_food_calorie_estimator
```

#### 2단계: 가상환경 생성
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

#### 3단계: 의존성 설치
```bash
pip install -r requirements.txt
```

#### 4단계: 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 열어서 필요한 값 수정
```

#### 5단계: 애플리케이션 실행
```bash
python main.py
```

### Docker 실행

```bash
# 이미지 빌드
docker build -t 39_food_calorie_estimator .

# 컨테이너 실행
docker run -p 8000:8000 39_food_calorie_estimator
```

## 🧪 테스트

```bash
# 모든 테스트 실행
pytest

# 상세 출력
pytest -v

# 특정 테스트 실행
pytest tests/test_main.py
```

## 📚 API 문서

자동 생성 문서:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🌐 AWS 배포

### EC2 배포

1. EC2 인스턴스 생성 (Ubuntu 22.04 LTS)
2. 필수 소프트웨어 설치:
```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3-pip docker.io
```

3. 애플리케이션 배포:
```bash
git clone <repository>
cd 39_food_calorie_estimator
docker-compose up -d
```

### RDS 연결

```python
# config.py 또는 .env에서
DATABASE_URL=postgresql://user:password@rds-endpoint:5432/database
```

## 💰 수익화 방안

1. **SaaS 모델**: 월별 구독 ($9.99-$99.99)
2. **API 접근**: 호출 기반 과금
3. **엔터프라이즈**: 맞춤형 솔루션
4. **지원 서비스**: 프리미엄 기술 지원

## 🔒 보안

- ✅ JWT 기반 인증
- ✅ 비밀번호 해싱 (bcrypt)
- ✅ HTTPS 권장
- ✅ 입력 검증
- ✅ SQL 인젝션 방지 (ORM 사용)

## 🤝 기여

버그 리포트나 기능 제안은 GitHub Issues로 제출해주세요.

## 📄 라이선스

MIT License

## 📞 지원

- 📧 이메일: support@example.com
- 📚 문서: https://docs.example.com

---

**마지막 업데이트**: 2024년 1월 15일
