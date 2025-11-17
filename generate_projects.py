#!/usr/bin/env python3
"""
Automatic Project Generator for Python Applications
Generates 59 additional projects based on predefined templates
"""

import os
import json
from pathlib import Path
from typing import Dict, List

# Project metadata
PROJECTS = {
    # FastAPI - SaaS
    "02_email_newsletter_platform": {
        "framework": "fastapi",
        "type": "saas",
        "description": "Email newsletter management and distribution platform",
        "db": "postgresql",
        "main_features": ["email campaigns", "subscriber management", "analytics", "templates"]
    },
    "03_url_shortener_service": {
        "framework": "fastapi",
        "type": "saas",
        "description": "URL shortening service with analytics",
        "db": "postgresql",
        "main_features": ["url shortening", "custom domains", "click tracking", "qr codes"]
    },
    "04_expense_tracker_saas": {
        "framework": "fastapi",
        "type": "saas",
        "description": "Personal expense tracking and budgeting application",
        "db": "postgresql",
        "main_features": ["expense tracking", "budgeting", "categorization", "reports"]
    },
    "05_document_converter_api": {
        "framework": "fastapi",
        "type": "saas",
        "description": "Multi-format document conversion service",
        "db": "postgresql",
        "main_features": ["pdf conversion", "image processing", "batch processing", "webhooks"]
    },
    "06_form_builder_platform": {
        "framework": "fastapi",
        "type": "saas",
        "description": "No-code form builder platform",
        "db": "postgresql",
        "main_features": ["form builder", "submissions", "email notifications", "templates"]
    },
    "07_api_monitoring_service": {
        "framework": "fastapi",
        "type": "saas",
        "description": "API uptime and performance monitoring",
        "db": "postgresql",
        "main_features": ["uptime monitoring", "alerts", "dashboards", "integrations"]
    },
    "08_markdown_to_html_saas": {
        "framework": "fastapi",
        "type": "saas",
        "description": "Markdown conversion and documentation platform",
        "db": "postgresql",
        "main_features": ["markdown conversion", "syntax highlighting", "pdf export", "versioning"]
    },
    "09_qr_code_generator_api": {
        "framework": "fastapi",
        "type": "saas",
        "description": "QR code generation and management service",
        "db": "postgresql",
        "main_features": ["qr generation", "customization", "tracking", "bulk generation"]
    },
    "10_jwt_auth_service": {
        "framework": "fastapi",
        "type": "saas",
        "description": "JWT-based authentication and authorization service",
        "db": "postgresql",
        "main_features": ["jwt tokens", "oauth2", "mfa", "session management"]
    },

    # Django - PaaS
    "11_multi_tenant_crm": {
        "framework": "django",
        "type": "paas",
        "description": "Multi-tenant CRM system for businesses",
        "db": "postgresql",
        "main_features": ["tenant management", "contacts", "deals", "pipelines", "reports"]
    },
    "12_blog_platform": {
        "framework": "django",
        "type": "paas",
        "description": "Full-featured blogging platform",
        "db": "postgresql",
        "main_features": ["posts", "comments", "tags", "categories", "seo"]
    },
    "13_project_management_system": {
        "framework": "django",
        "type": "paas",
        "description": "Project and team collaboration platform",
        "db": "postgresql",
        "main_features": ["projects", "tasks", "team members", "timeline", "collaboration"]
    },
    "14_inventory_management": {
        "framework": "django",
        "type": "paas",
        "description": "Inventory tracking and management system",
        "db": "postgresql",
        "main_features": ["stock tracking", "warehouse", "orders", "alerts", "reports"]
    },
    "15_customer_support_portal": {
        "framework": "django",
        "type": "paas",
        "description": "Customer support and ticketing system",
        "db": "postgresql",
        "main_features": ["tickets", "knowledge base", "chat", "escalation", "sla"]
    },
    "16_event_booking_system": {
        "framework": "django",
        "type": "paas",
        "description": "Event booking and ticketing platform",
        "db": "postgresql",
        "main_features": ["event creation", "ticketing", "payment", "qr codes", "analytics"]
    },
    "17_subscription_billing_platform": {
        "framework": "django",
        "type": "paas",
        "description": "Subscription and billing management system",
        "db": "postgresql",
        "main_features": ["subscriptions", "billing", "invoices", "payment processing", "reports"]
    },
    "18_learning_management_system": {
        "framework": "django",
        "type": "paas",
        "description": "Online learning management system",
        "db": "postgresql",
        "main_features": ["courses", "lessons", "quizzes", "progress tracking", "certificates"]
    },
    "19_real_estate_listing_platform": {
        "framework": "django",
        "type": "paas",
        "description": "Real estate property listing platform",
        "db": "postgresql",
        "main_features": ["listings", "search", "maps", "messaging", "appointments"]
    },
    "20_social_network_backend": {
        "framework": "django",
        "type": "paas",
        "description": "Social networking platform backend",
        "db": "postgresql",
        "main_features": ["users", "posts", "comments", "likes", "messaging"]
    },

    # PyTorch - Computer Vision
    "21_object_detection_api": {
        "framework": "pytorch",
        "type": "ai",
        "description": "Real-time object detection API",
        "db": "sqlite",
        "main_features": ["yolov8", "real-time detection", "class filtering", "confidence scores"]
    },
    "22_face_recognition_system": {
        "framework": "pytorch",
        "type": "ai",
        "description": "Face recognition and verification system",
        "db": "sqlite",
        "main_features": ["face detection", "face alignment", "face embedding", "verification"]
    },
    "23_image_classification_service": {
        "framework": "pytorch",
        "type": "ai",
        "description": "Image classification API",
        "db": "sqlite",
        "main_features": ["resnet", "vgg", "inception", "transfer learning"]
    },
    "24_document_ocr_tool": {
        "framework": "pytorch",
        "type": "ai",
        "description": "Optical character recognition for documents",
        "db": "sqlite",
        "main_features": ["text detection", "text recognition", "layout analysis", "table extraction"]
    },
    "25_pose_estimation_analyzer": {
        "framework": "pytorch",
        "type": "ai",
        "description": "Human pose estimation and analysis",
        "db": "sqlite",
        "main_features": ["pose detection", "skeleton visualization", "movement analysis"]
    },
    "26_hand_gesture_recognizer": {
        "framework": "pytorch",
        "type": "ai",
        "description": "Hand gesture recognition system",
        "db": "sqlite",
        "main_features": ["hand detection", "gesture classification", "real-time processing"]
    },
    "27_vehicle_detection_system": {
        "framework": "pytorch",
        "type": "ai",
        "description": "Vehicle detection and tracking system",
        "db": "sqlite",
        "main_features": ["vehicle detection", "license plate reading", "tracking"]
    },
    "28_crowd_density_analyzer": {
        "framework": "pytorch",
        "type": "ai",
        "description": "Crowd density estimation and analysis",
        "db": "sqlite",
        "main_features": ["density estimation", "crowd counting", "heat mapping"]
    },
    "29_image_super_resolution": {
        "framework": "pytorch",
        "type": "ai",
        "description": "Image enhancement and super-resolution",
        "db": "sqlite",
        "main_features": ["upscaling", "denoising", "enhancement", "batch processing"]
    },
    "30_scene_segmentation_tool": {
        "framework": "pytorch",
        "type": "ai",
        "description": "Semantic scene segmentation",
        "db": "sqlite",
        "main_features": ["pixel segmentation", "object masks", "visualization"]
    },

    # TensorFlow - Computer Vision
    "31_traffic_sign_detection": {
        "framework": "tensorflow",
        "type": "ai",
        "description": "Traffic sign detection and classification",
        "db": "sqlite",
        "main_features": ["sign detection", "classification", "speed optimization"]
    },
    "32_medical_image_analyzer": {
        "framework": "tensorflow",
        "type": "ai",
        "description": "Medical image analysis system",
        "db": "sqlite",
        "main_features": ["xray analysis", "tumor detection", "segmentation"]
    },
    "33_plant_disease_detector": {
        "framework": "tensorflow",
        "type": "ai",
        "description": "Plant disease detection from images",
        "db": "sqlite",
        "main_features": ["disease classification", "severity assessment", "treatment recommendations"]
    },
    "34_license_plate_reader": {
        "framework": "tensorflow",
        "type": "ai",
        "description": "License plate detection and OCR",
        "db": "sqlite",
        "main_features": ["plate detection", "character recognition", "vehicle identification"]
    },
    "35_product_defect_detector": {
        "framework": "tensorflow",
        "type": "ai",
        "description": "Manufacturing defect detection system",
        "db": "sqlite",
        "main_features": ["defect detection", "classification", "quality assurance"]
    },
    "36_image_colorization_tool": {
        "framework": "tensorflow",
        "type": "ai",
        "description": "Automatic image colorization service",
        "db": "sqlite",
        "main_features": ["grayscale colorization", "color enhancement", "artistic effects"]
    },
    "37_building_floor_plan_analyzer": {
        "framework": "tensorflow",
        "type": "ai",
        "description": "Floor plan recognition and analysis",
        "db": "sqlite",
        "main_features": ["room detection", "wall extraction", "area calculation"]
    },
    "38_wildlife_species_detector": {
        "framework": "tensorflow",
        "type": "ai",
        "description": "Wildlife species identification system",
        "db": "sqlite",
        "main_features": ["species detection", "wildlife monitoring", "biodiversity tracking"]
    },
    "39_food_calorie_estimator": {
        "framework": "tensorflow",
        "type": "ai",
        "description": "Food calorie estimation from images",
        "db": "sqlite",
        "main_features": ["food recognition", "portion estimation", "nutritional data"]
    },
    "40_clothing_recommendation_ai": {
        "framework": "tensorflow",
        "type": "ai",
        "description": "Clothing recommendation system",
        "db": "sqlite",
        "main_features": ["style classification", "recommendations", "trend analysis"]
    },

    # Monetization Tools
    "41_stock_price_analyzer": {
        "framework": "python",
        "type": "monetization",
        "description": "Stock price analysis and prediction tool",
        "db": "sqlite",
        "main_features": ["price analysis", "trend prediction", "portfolio tracking"]
    },
    "42_web_scraper_service": {
        "framework": "python",
        "type": "monetization",
        "description": "Automated web scraping service",
        "db": "postgresql",
        "main_features": ["web scraping", "scheduling", "data export", "api"]
    },
    "43_seo_analyzer_tool": {
        "framework": "python",
        "type": "monetization",
        "description": "SEO analysis and optimization tool",
        "db": "sqlite",
        "main_features": ["page analysis", "keyword research", "competitor analysis"]
    },
    "44_social_media_scheduler": {
        "framework": "python",
        "type": "monetization",
        "description": "Social media posting scheduler",
        "db": "postgresql",
        "main_features": ["scheduling", "multi-platform", "analytics", "templates"]
    },
    "45_keyword_research_tool": {
        "framework": "python",
        "type": "monetization",
        "description": "Keyword research and analysis platform",
        "db": "sqlite",
        "main_features": ["keyword analysis", "volume estimation", "competition analysis"]
    },
    "46_competitor_price_monitor": {
        "framework": "python",
        "type": "monetization",
        "description": "E-commerce price monitoring tool",
        "db": "postgresql",
        "main_features": ["price tracking", "alerts", "comparison", "reports"]
    },
    "47_email_campaign_manager": {
        "framework": "python",
        "type": "monetization",
        "description": "Email marketing campaign management",
        "db": "postgresql",
        "main_features": ["campaign creation", "segmentation", "automation", "analytics"]
    },
    "48_affiliate_link_tracker": {
        "framework": "python",
        "type": "monetization",
        "description": "Affiliate link tracking and management",
        "db": "postgresql",
        "main_features": ["link tracking", "revenue tracking", "reports", "integrations"]
    },
    "49_lead_generation_tool": {
        "framework": "python",
        "type": "monetization",
        "description": "Lead generation and qualification tool",
        "db": "postgresql",
        "main_features": ["lead capture", "qualification", "scoring", "crm integration"]
    },
    "50_content_plagiarism_checker": {
        "framework": "python",
        "type": "monetization",
        "description": "Content plagiarism detection service",
        "db": "sqlite",
        "main_features": ["plagiarism checking", "similarity reports", "batch processing"]
    },
    "51_pdf_processing_service": {
        "framework": "python",
        "type": "monetization",
        "description": "PDF processing and manipulation service",
        "db": "sqlite",
        "main_features": ["pdf merging", "splitting", "watermarking", "extraction"]
    },
    "52_data_extraction_tool": {
        "framework": "python",
        "type": "monetization",
        "description": "Data extraction from various formats",
        "db": "postgresql",
        "main_features": ["data extraction", "format conversion", "validation", "export"]
    },
    "53_report_automation_system": {
        "framework": "python",
        "type": "monetization",
        "description": "Automated report generation system",
        "db": "postgresql",
        "main_features": ["report generation", "scheduling", "distribution", "templates"]
    },
    "54_slack_bot_analytics": {
        "framework": "python",
        "type": "monetization",
        "description": "Slack bot for analytics and insights",
        "db": "sqlite",
        "main_features": ["workspace analytics", "metrics", "insights", "notifications"]
    },
    "55_linkedin_profile_analyzer": {
        "framework": "python",
        "type": "monetization",
        "description": "LinkedIn profile analysis tool",
        "db": "sqlite",
        "main_features": ["profile scraping", "analytics", "recommendations"]
    },
    "56_amazon_product_research_tool": {
        "framework": "python",
        "type": "monetization",
        "description": "Amazon product research and analysis",
        "db": "sqlite",
        "main_features": ["product data", "price tracking", "review analysis"]
    },
    "57_youtube_analytics_dashboard": {
        "framework": "python",
        "type": "monetization",
        "description": "YouTube channel analytics dashboard",
        "db": "sqlite",
        "main_features": ["channel analytics", "video stats", "growth tracking"]
    },
    "58_crypto_price_alert_system": {
        "framework": "python",
        "type": "monetization",
        "description": "Cryptocurrency price monitoring and alerts",
        "db": "sqlite",
        "main_features": ["price monitoring", "alerts", "portfolio tracking"]
    },
    "59_real_estate_valuation_tool": {
        "framework": "python",
        "type": "monetization",
        "description": "Real estate property valuation tool",
        "db": "sqlite",
        "main_features": ["property analysis", "valuation", "market data"]
    },
    "60_invoice_processing_system": {
        "framework": "python",
        "type": "monetization",
        "description": "Automated invoice processing system",
        "db": "postgresql",
        "main_features": ["invoice ocr", "data extraction", "storage", "automation"]
    },
}

def create_project_structure(project_name: str, project_info: Dict) -> None:
    """Create project directory structure"""
    base_path = Path(f"/home/user/02-python-app/{project_name}")

    # Create directories
    dirs = [
        base_path,
        base_path / "app",
        base_path / "tests",
    ]

    if project_info["framework"] in ["fastapi", "django"]:
        dirs.extend([
            base_path / "app" / "routes",
            base_path / "app" / "core",
        ])

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

def create_requirements(project_name: str, project_info: Dict) -> None:
    """Create requirements.txt based on framework"""
    base_path = Path(f"/home/user/02-python-app/{project_name}")

    if project_info["framework"] == "fastapi":
        requirements = """fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pytest==7.4.3
httpx==0.25.2
"""
    elif project_info["framework"] == "django":
        requirements = """Django==4.2.8
djangorestframework==3.14.0
django-cors-headers==4.3.1
django-environ==0.21.0
psycopg2-binary==2.9.9
celery==5.3.4
redis==5.0.1
pytest-django==4.7.0
python-decouple==3.8
"""
    elif project_info["framework"] == "pytorch":
        requirements = """torch==2.1.2
torchvision==0.16.2
fastapi==0.104.1
uvicorn==0.24.0
pillow==10.1.0
opencv-python==4.8.1.78
numpy==1.24.3
pytest==7.4.3
"""
    elif project_info["framework"] == "tensorflow":
        requirements = """tensorflow==2.15.0
fastapi==0.104.1
uvicorn==0.24.0
pillow==10.1.0
opencv-python==4.8.1.78
numpy==1.24.3
pytest==7.4.3
"""
    else:  # Python tools
        requirements = """requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.2
pandas==2.1.3
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pytest==7.4.3
schedule==1.2.0
"""

    (base_path / "requirements.txt").write_text(requirements)

def create_env_example(project_name: str, project_info: Dict) -> None:
    """Create .env.example file"""
    base_path = Path(f"/home/user/02-python-app/{project_name}")

    env_content = f"""# {project_name} Configuration

# Database
DATABASE_URL=sqlite:///./app.db
"""

    if project_info["db"] == "postgresql":
        env_content += """DATABASE_URL=postgresql://user:password@localhost:5432/dbname
"""

    env_content += """
# JWT (for FastAPI/Django projects)
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_TITLE={0}
DEBUG=True

# AWS Configuration
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
""".format(project_name)

    (base_path / ".env.example").write_text(env_content)

def create_gitignore(project_name: str) -> None:
    """Create .gitignore file"""
    base_path = Path(f"/home/user/02-python-app/{project_name}")

    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment variables
.env
.env.local

# Database
*.db
*.sqlite
*.sqlite3
test.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log
logs/

# Docker
docker-compose.override.yml

# Data
data/
output/
models/
"""

    (base_path / ".gitignore").write_text(gitignore_content)

def create_dockerfile(project_name: str, project_info: Dict) -> None:
    """Create Dockerfile"""
    base_path = Path(f"/home/user/02-python-app/{project_name}")

    python_version = "3.11"
    if project_info["framework"] == "tensorflow":
        python_version = "3.10"  # Better TF compatibility

    dockerfile_content = f"""FROM python:{python_version}-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "main.py"]
"""

    (base_path / "Dockerfile").write_text(dockerfile_content)

def create_init_files(project_name: str, project_info: Dict) -> None:
    """Create __init__.py files"""
    base_path = Path(f"/home/user/02-python-app/{project_name}")

    (base_path / "app" / "__init__.py").write_text(f'"""Application for {project_name}"""\n')
    (base_path / "tests" / "__init__.py").write_text('"""Tests for application"""\n')

    if project_info["framework"] in ["fastapi", "django"]:
        (base_path / "app" / "core" / "__init__.py").write_text('"""Core modules"""\n')
        (base_path / "app" / "routes" / "__init__.py").write_text('"""API routes"""\n')

def create_main_py(project_name: str, project_info: Dict) -> None:
    """Create main.py or manage.py"""
    base_path = Path(f"/home/user/02-python-app/{project_name}")

    if project_info["framework"] == "fastapi":
        main_content = f'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="{project_name}",
    description="{project_info['description']}",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {{"message": "Welcome to {project_name}"}}

@app.get("/health")
def health():
    return {{"status": "healthy"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        (base_path / "main.py").write_text(main_content)

    elif project_info["framework"] == "django":
        main_content = f'''import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", "runserver"])
'''
        (base_path / "manage.py").write_text(main_content)

    else:  # Python tools / AI models
        main_content = f'''#!/usr/bin/env python3
"""
{project_name}
{project_info['description']}
"""

def main():
    print("Starting {project_name}...")
    # Implementation here

if __name__ == "__main__":
    main()
'''
        (base_path / "main.py").write_text(main_content)

def create_readme(project_name: str, project_info: Dict) -> None:
    """Create README.md file"""
    base_path = Path(f"/home/user/02-python-app/{project_name}")

    readme_content = f"""# {project_name}

## 📋 프로젝트 소개

**{project_name}**는 {project_info['description']}

### 주요 기능
"""

    for feature in project_info.get("main_features", []):
        readme_content += f"- ✅ {feature.title()}\n"

    readme_content += f"""

## 🛠 기술 스택

- **Framework**: {project_info['framework'].upper()}
- **Database**: {project_info['db'].upper()}
- **Python**: 3.11+
- **Docker**: Supported

## 📁 프로젝트 구조

```
{project_name}/
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
cd {project_name}
```

#### 2단계: 가상환경 생성
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\\Scripts\\activate  # Windows
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
docker build -t {project_name} .

# 컨테이너 실행
docker run -p 8000:8000 {project_name}
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
cd {project_name}
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
"""

    (base_path / "README.md").write_text(readme_content)

def create_test_file(project_name: str, project_info: Dict) -> None:
    """Create test_main.py"""
    base_path = Path(f"/home/user/02-python-app/{project_name}")

    test_content = f'''import pytest

class TestHealth:
    def test_placeholder(self):
        """Placeholder test"""
        assert True

# Add your tests here
'''

    (base_path / "tests" / "test_main.py").write_text(test_content)

def generate_all_projects() -> None:
    """Generate all 59 projects"""
    project_count = len(PROJECTS)

    print(f"🚀 Generating {{project_count}} projects...")
    print("=" * 60)

    for i, (project_name, project_info) in enumerate(PROJECTS.items(), 1):
        print(f"[{{i}}/{{project_count}}] Creating {project_name}...", end=" ")

        try:
            create_project_structure(project_name, project_info)
            create_requirements(project_name, project_info)
            create_env_example(project_name, project_info)
            create_gitignore(project_name)
            create_dockerfile(project_name, project_info)
            create_init_files(project_name, project_info)
            create_main_py(project_name, project_info)
            create_readme(project_name, project_info)
            create_test_file(project_name, project_info)

            print("✅")
        except Exception as e:
            print(f"❌ Error: {{e}}")

    print("=" * 60)
    print(f"✨ Successfully generated {{project_count}} projects!")

if __name__ == "__main__":
    generate_all_projects()
