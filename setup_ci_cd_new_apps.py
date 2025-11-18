#!/usr/bin/env python3
"""
Setup CI/CD workflows for 30 new applications (61-90)
"""

from pathlib import Path

def create_ci_cd_workflow(app_num: int) -> str:
    """Create GitHub Actions workflow for application"""
    return f'''name: App {app_num:02d} - CI/CD Pipeline

on:
  push:
    branches: [main, develop]
    paths:
      - '{app_num:02d}_*/**'
      - '.github/workflows/app-{app_num:02d}.yml'
  pull_request:
    branches: [main, develop]
    paths:
      - '{app_num:02d}_*/**'

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: app-{app_num:02d}

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11']

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{{{ matrix.python-version }}}}
        uses: actions/setup-python@v4
        with:
          python-version: ${{{{ matrix.python-version }}}}
          cache: 'pip'

      - name: Install dependencies
        run: |
          cd {app_num:02d}_*
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Lint with Flake8
        run: |
          cd {app_num:02d}_*
          pip install flake8
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

      - name: Type check with mypy
        run: |
          cd {app_num:02d}_*
          pip install mypy
          mypy . --ignore-missing-imports || true

      - name: Run tests with pytest
        run: |
          cd {app_num:02d}_*
          pip install pytest pytest-cov pytest-asyncio
          pytest tests/ --cov=app --cov-report=xml --cov-report=html

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          flags: unittests
          name: app-{app_num:02d}
          fail_ci_if_error: false

  security:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd {app_num:02d}_*
          pip install -r requirements.txt

      - name: Run Bandit security check
        run: |
          cd {app_num:02d}_*
          pip install bandit
          bandit -r . -ll || true

      - name: Check dependencies with Safety
        run: |
          cd {app_num:02d}_*
          pip install safety
          safety check --json || true

  build-docker:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{{{ env.REGISTRY }}}}
          username: ${{{{ github.actor }}}}
          password: ${{{{ secrets.GITHUB_TOKEN }}}}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{{{ env.REGISTRY }}}}/${{{{ github.repository }}}}-${{{{ env.IMAGE_NAME }}}}
          tags: |
            type=semver,pattern={{{{version}}}}
            type=sha

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: {app_num:02d}_*
          push: true
          tags: ${{{{ steps.meta.outputs.tags }}}}
          labels: ${{{{ steps.meta.outputs.labels }}}}

  deploy:
    needs: build-docker
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy notification
        run: echo "Deployment ready for app-{app_num:02d}"
        # Add your deployment commands here
'''

def setup_ci_cd_workflows():
    """Create CI/CD workflows for all 30 new applications"""
    print("📦 Setting up CI/CD workflows for applications 61-90...")
    print("=" * 70)

    workflows_dir = Path("/home/user/02-python-app/.github/workflows")

    for app_num in range(61, 91):
        workflow_file = workflows_dir / f"app-{app_num:02d}.yml"
        workflow_content = create_ci_cd_workflow(app_num)
        workflow_file.write_text(workflow_content)
        print(f"[{app_num:02d}] CI/CD workflow created ✅")

    print("=" * 70)
    print(f"✨ Successfully created 30 CI/CD workflows (61-90)")
    print("\nWorkflow features:")
    print("  ✓ Python 3.11 testing")
    print("  ✓ Linting (Flake8)")
    print("  ✓ Type checking (mypy)")
    print("  ✓ Unit testing (pytest)")
    print("  ✓ Coverage reporting (Codecov)")
    print("  ✓ Security scanning (Bandit, Safety)")
    print("  ✓ Docker image building")
    print("  ✓ Push to container registry")

if __name__ == "__main__":
    setup_ci_cd_workflows()
