#!/usr/bin/env python3
"""
Generate 30 More Applications (91-120)
Specialized domains: IoT, Education, Media, Social, Gaming, Logistics
"""

from pathlib import Path

def generate_app_structure(app_number: int, app_name: str, description: str, tech_stack: str):
    """Generate complete application structure"""

    main_py = f'''#!/usr/bin/env python3
"""
{app_name}
{description}
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={{"check_same_thread": False}} if "sqlite" in DATABASE_URL else {{}}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create FastAPI app
app = FastAPI(
    title="{app_name}",
    version="1.0.0",
    description="{description}"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    """Root endpoint"""
    return {{
        "message": "Welcome to {app_name}",
        "version": "1.0.0",
        "docs": {{"swagger": "/docs", "redoc": "/redoc"}}
    }}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {{"status": "healthy", "version": "1.0.0"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

    requirements = f'''fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.0
bcrypt==4.1.1
python-jose==3.3.0
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
black==23.12.0
flake8==6.1.0
mypy==1.7.1
'''

    dockerfile = '''FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

    docker_compose = f'''version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./test.db
    volumes:
      - .:/app
    command: uvicorn main:app --reload --host 0.0.0.0
'''

    env_example = '''APP_NAME=My App
APP_ENV=development
DEBUG=true
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=change-this-key
ALGORITHM=HS256
'''

    readme = f'''# {app_name}

{description}

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env.local
python main.py
```

## API

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT
'''

    return {
        'main.py': main_py,
        'requirements.txt': requirements,
        'Dockerfile': dockerfile,
        'docker-compose.yml': docker_compose,
        '.env.example': env_example,
        'README.md': readme
    }

def create_additional_apps_phase2():
    """Create 30 more applications (91-120)"""

    base_path = Path("/home/user/02-python-app")

    # Application definitions for Phase 2
    apps = [
        # IoT & Smart Devices (91-96)
        (91, "IoT Device Management Platform",
         "MQTT-based IoT device management with real-time data collection and analytics"),
        (92, "Smart Home Automation System",
         "Home automation control system with voice integration and scheduling"),
        (93, "Environmental Monitoring System",
         "Air quality, temperature, and pollution monitoring with alerts"),
        (94, "Industrial IoT Analytics",
         "Factory equipment monitoring with predictive maintenance"),
        (95, "Energy Consumption Tracker",
         "Real-time energy monitoring for buildings and homes"),
        (96, "Connected Vehicle Management",
         "Fleet tracking and vehicle diagnostics platform"),

        # Education & Learning (97-102)
        (97, "Online Course Platform",
         "Complete e-learning platform with video streaming and quizzes"),
        (98, "Student Performance Analytics",
         "Advanced analytics for tracking student progress and outcomes"),
        (99, "Virtual Classroom Manager",
         "Real-time classroom management with interactive features"),
        (100, "Exam & Assessment System",
         "Online testing platform with proctoring and instant grading"),
        (101, "Educational Content Recommender",
         "AI-powered personalized learning content recommendations"),
        (102, "Language Learning Platform",
         "Interactive language learning with AI pronunciation analysis"),

        # Media & Entertainment (103-108)
        (103, "Video Streaming Platform",
         "Netflix-like video streaming with adaptive bitrate and recommendations"),
        (104, "Podcast Management System",
         "Podcast hosting, distribution, and analytics platform"),
        (105, "Music Streaming Service",
         "Spotify-like music streaming with playlists and recommendations"),
        (106, "Photo Sharing Network",
         "Instagram-like photo sharing with filters and social features"),
        (107, "Content Moderation System",
         "AI-powered content moderation for user-generated content"),
        (108, "Digital Rights Management",
         "Copyright and DRM protection for digital content"),

        # Social & Community (109-114)
        (109, "Community Forum Platform",
         "Reddit-like community forum with voting and moderation"),
        (110, "Social Networking Platform",
         "Facebook-like social network with posts, friends, and messaging"),
        (111, "Dating Match Engine",
         "Tinder-like matching algorithm with personalized recommendations"),
        (112, "Interest-based Groups",
         "Discord-like communities with channels and real-time chat"),
        (113, "Event Networking Platform",
         "LinkedIn-like professional networking for events"),
        (114, "Knowledge Sharing Platform",
         "Stack Overflow-like Q&A and knowledge sharing"),

        # Gaming & Entertainment (115-118)
        (115, "Game Backend Services",
         "Game server with player management and leaderboards"),
        (116, "Multiplayer Game Lobby",
         "Real-time game matching and lobby system"),
        (117, "In-Game Analytics Platform",
         "Game analytics and user behavior tracking"),
        (118, "NFT Marketplace",
         "Blockchain-based NFT trading platform"),

        # Logistics & Supply Chain (119-120)
        (119, "Supply Chain Tracking System",
         "Real-time supply chain and logistics tracking"),
        (120, "Last-Mile Delivery Optimizer",
         "Route optimization for delivery services"),
    ]

    print("🚀 Generating 30 More Applications (91-120)...")
    print("=" * 70)

    for app_num, app_name, description in apps:
        app_dir = base_path / f"{app_num:02d}_{app_name.lower().replace(' ', '_').replace('-', '_')}"
        app_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        (app_dir / "app").mkdir(exist_ok=True)
        (app_dir / "app" / "models").mkdir(exist_ok=True)
        (app_dir / "app" / "schemas").mkdir(exist_ok=True)
        (app_dir / "app" / "routes").mkdir(exist_ok=True)
        (app_dir / "app" / "services").mkdir(exist_ok=True)
        (app_dir / "tests").mkdir(exist_ok=True)

        # Create __init__.py files
        (app_dir / "app" / "__init__.py").write_text("")
        (app_dir / "app" / "models" / "__init__.py").write_text("")
        (app_dir / "app" / "schemas" / "__init__.py").write_text("")
        (app_dir / "app" / "routes" / "__init__.py").write_text("")
        (app_dir / "app" / "services" / "__init__.py").write_text("")
        (app_dir / "tests" / "__init__.py").write_text("")
        (app_dir / "tests" / "conftest.py").write_text("import pytest\n\n@pytest.fixture\ndef mock_db():\n    pass\n")

        # Generate and write files
        files = generate_app_structure(app_num, app_name, description, "FastAPI")

        for filename, content in files.items():
            (app_dir / filename).write_text(content)

        # Create .gitignore
        (app_dir / ".gitignore").write_text("""__pycache__/
*.py[cod]
.pytest_cache/
.coverage
.venv
venv/
.env.local
db.sqlite3
""")

        print(f"[{app_num:02d}] {app_name:<50} ✅")

    print("=" * 70)
    print(f"✨ Successfully generated 30 more applications (91-120)")
    print("\nApplications created:")
    print("  • IoT & Smart Devices (91-96): 6 applications")
    print("  • Education & Learning (97-102): 6 applications")
    print("  • Media & Entertainment (103-108): 6 applications")
    print("  • Social & Community (109-114): 6 applications")
    print("  • Gaming & Entertainment (115-118): 4 applications")
    print("  • Logistics & Supply Chain (119-120): 2 applications")
    print("\nTotal new projects: 30")
    print("Total ecosystem size: 120 backend + 20 frontend = 140 total applications")

if __name__ == "__main__":
    create_additional_apps_phase2()
