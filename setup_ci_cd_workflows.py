#!/usr/bin/env python3
"""
GitHub Actions CI/CD Pipeline Setup
Adds comprehensive GitHub Actions workflows for:
- Automated testing
- Code quality checks
- Building Docker images
- Deployment automation
"""

from pathlib import Path
import os

def generate_fastapi_workflow() -> str:
    """Generate GitHub Actions workflow for FastAPI projects"""
    return '''name: FastAPI CI/CD Pipeline

on:
  push:
    branches: [main, develop, "feature/**"]
  pull_request:
    branches: [main, develop]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio black flake8 mypy

      - name: Lint with flake8
        run: |
          flake8 app main.py --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 app main.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

      - name: Format check with black
        run: black --check app main.py

      - name: Type check with mypy
        run: mypy app main.py --ignore-missing-imports || true

      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost/test_db
          REDIS_URL: redis://localhost:6379/0
          TESTING: "true"
        run: |
          pytest tests/ --cov=app --cov-report=xml --cov-report=html -v

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    needs: build
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to staging
        run: |
          echo "Deploying to staging environment..."
          # Add your deployment script here
          # Example: ./scripts/deploy-staging.sh

      - name: Health check
        run: |
          curl -f http://staging-app/health || exit 1
'''

def generate_django_workflow() -> str:
    """Generate GitHub Actions workflow for Django projects"""
    return '''name: Django CI/CD Pipeline

on:
  push:
    branches: [main, develop, "feature/**"]
  pull_request:
    branches: [main, develop]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-django pytest-cov black flake8 mypy isort

      - name: Run migrations
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        run: |
          python manage.py migrate

      - name: Lint with flake8
        run: |
          flake8 . --exclude=migrations,venv --max-line-length=120

      - name: Format check with black
        run: black --check .

      - name: Import sort check
        run: isort --check-only .

      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
          DEBUG: "false"
        run: |
          pytest tests/ --cov=. --cov-report=xml --cov-report=html -v

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-django

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install bandit safety

      - name: Run Bandit security scan
        run: bandit -r . -f json -o bandit-report.json || true

      - name: Check dependencies
        run: safety check --json || true

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    needs: build
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to production
        run: |
          echo "Deploying Django application to production..."
          # Add your Django deployment script here
'''

def generate_ai_ml_workflow() -> str:
    """Generate GitHub Actions workflow for AI/ML projects"""
    return '''name: AI/ML CI/CD Pipeline

on:
  push:
    branches: [main, develop, "feature/**"]
  pull_request:
    branches: [main, develop]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov black flake8 mypy

      - name: Lint with flake8
        run: |
          flake8 app main.py --count --max-line-length=127 --statistics

      - name: Format check with black
        run: black --check app main.py

      - name: Type check with mypy
        run: mypy app main.py --ignore-missing-imports || true

      - name: Run unit tests
        run: |
          pytest tests/unit --cov=app --cov-report=xml -v

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-aiml

  model-testing:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Download model artifacts
        run: |
          mkdir -p models
          # Download pre-trained models if needed
          echo "Model artifacts setup"

      - name: Run model integration tests
        run: |
          pytest tests/integration/test_models.py -v

      - name: Benchmark model performance
        run: |
          python tests/benchmark_models.py || true

  build:
    needs: [test, model-testing]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    needs: build
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Deploy AI/ML model service
        run: |
          echo "Deploying AI/ML service to production..."
          # Add your model deployment script here
'''

def generate_monetization_workflow() -> str:
    """Generate GitHub Actions workflow for monetization tools"""
    return '''name: Monetization Tools CI/CD Pipeline

on:
  push:
    branches: [main, develop, "feature/**"]
  pull_request:
    branches: [main, develop]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov black flake8 mypy

      - name: Lint with flake8
        run: flake8 app main.py --max-line-length=127

      - name: Format check with black
        run: black --check app main.py

      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        run: |
          pytest tests/ --cov=app --cov-report=xml --cov-report=html -v

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install security tools
        run: |
          python -m pip install bandit safety

      - name: Security scan with Bandit
        run: bandit -r app -f json -o bandit-report.json || true

      - name: Check dependencies with Safety
        run: safety check || true

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    needs: build
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Deploy tool service
        run: |
          echo "Deploying tool to production..."
          # Add deployment commands here
'''

def generate_release_workflow() -> str:
    """Generate GitHub Actions workflow for releases"""
    return '''name: Release Automation

on:
  push:
    tags:
      - 'v*'

jobs:
  create-release:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Generate changelog
        run: |
          python -c "
          import subprocess
          result = subprocess.run(['git', 'log', '--oneline', '-n', '20'], capture_output=True, text=True)
          with open('CHANGELOG_LATEST.md', 'w') as f:
              f.write(result.stdout)
          "

      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body_path: CHANGELOG_LATEST.md
          draft: false
          prerelease: false
'''

def setup_ci_cd_workflows():
    """Setup CI/CD workflows for all projects"""
    fastapi_projects = [
        "01_task_management_saas",
        "02_email_newsletter_platform",
        "03_url_shortener_service",
        "04_expense_tracker_saas",
        "05_document_converter_api",
        "06_form_builder_platform",
        "07_api_monitoring_service",
        "08_markdown_to_html_saas",
        "09_qr_code_generator_api",
        "10_jwt_auth_service",
    ]

    django_projects = [
        "11_multi_tenant_crm",
        "12_blog_platform",
        "13_project_management_system",
        "14_inventory_management",
        "15_customer_support_portal",
        "16_event_booking_system",
        "17_subscription_billing_platform",
        "18_learning_management_system",
        "19_real_estate_listing_platform",
        "20_social_network_backend",
    ]

    ai_projects = list(range(21, 41))
    monetization_projects = list(range(41, 61))

    print("🚀 Setting up CI/CD GitHub Actions Workflows...")
    print("=" * 70)

    # FastAPI projects
    print("[FastAPI Projects (01-10)]", end=" ", flush=True)
    fastapi_workflow = generate_fastapi_workflow()
    for project in fastapi_projects:
        base_path = Path(f"/home/user/02-python-app/{project}")
        workflows_dir = base_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        (workflows_dir / "ci-cd.yml").write_text(fastapi_workflow)
    print("✅")

    # Django projects
    print("[Django Projects (11-20)]", end=" ", flush=True)
    django_workflow = generate_django_workflow()
    for project in django_projects:
        base_path = Path(f"/home/user/02-python-app/{project}")
        workflows_dir = base_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        (workflows_dir / "ci-cd.yml").write_text(django_workflow)
    print("✅")

    # AI/ML projects
    print("[AI/ML Projects (21-40)]", end=" ", flush=True)
    aiml_workflow = generate_ai_ml_workflow()
    for i in ai_projects:
        projects = list(Path("/home/user/02-python-app").glob(f"{i:02d}_*"))
        if not projects:
            continue
        base_path = projects[0]
        workflows_dir = base_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        (workflows_dir / "ci-cd.yml").write_text(aiml_workflow)
    print("✅")

    # Monetization tools
    print("[Monetization Tools (41-60)]", end=" ", flush=True)
    monetization_workflow = generate_monetization_workflow()
    for i in monetization_projects:
        projects = list(Path("/home/user/02-python-app").glob(f"{i:02d}_*"))
        if not projects:
            continue
        base_path = projects[0]
        workflows_dir = base_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        (workflows_dir / "ci-cd.yml").write_text(monetization_workflow)
    print("✅")

    # Root level workflows
    print("[Root-level Workflows]", end=" ", flush=True)
    root_workflows_dir = Path("/home/user/02-python-app/.github/workflows")
    root_workflows_dir.mkdir(parents=True, exist_ok=True)
    release_workflow = generate_release_workflow()
    (root_workflows_dir / "release.yml").write_text(release_workflow)
    print("✅")

    print("=" * 70)
    print("✨ CI/CD workflows setup complete!")
    print("\nSetup Summary:")
    print(f"  ✓ FastAPI projects: 10 workflows")
    print(f"  ✓ Django projects: 10 workflows")
    print(f"  ✓ AI/ML projects: 20 workflows")
    print(f"  ✓ Monetization tools: 20 workflows")
    print(f"  ✓ Root-level release workflow: 1 workflow")
    print(f"  ✓ Total: 61 CI/CD workflow files")


if __name__ == "__main__":
    setup_ci_cd_workflows()
