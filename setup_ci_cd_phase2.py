#!/usr/bin/env python3
"""
Setup CI/CD workflows for 30 more applications (91-120)
"""

from pathlib import Path

def create_ci_cd_workflow(app_num: int) -> str:
    """Create GitHub Actions workflow for application"""
    return f'''name: App {app_num:02d} - CI/CD

on:
  push:
    branches: [main, develop]
    paths:
      - '{app_num:02d}_*/**'
  pull_request:
    branches: [main, develop]
    paths:
      - '{app_num:02d}_*/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      - name: Install dependencies
        run: |
          cd {app_num:02d}_*
          pip install -r requirements.txt pytest pytest-cov pytest-asyncio
      - name: Lint
        run: |
          cd {app_num:02d}_*
          flake8 . || true
      - name: Type check
        run: |
          cd {app_num:02d}_*
          mypy . --ignore-missing-imports || true
      - name: Run tests
        run: |
          cd {app_num:02d}_*
          pytest tests/ --cov=app --cov-report=xml

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd {app_num:02d}_*
          pip install -r requirements.txt bandit safety
      - name: Bandit
        run: |
          cd {app_num:02d}_*
          bandit -r . -ll || true
      - name: Safety
        run: |
          cd {app_num:02d}_*
          safety check || true
'''

def setup_ci_cd_workflows():
    """Create CI/CD workflows for all 30 new applications"""
    print("📦 Setting up CI/CD workflows for applications 91-120...")
    print("=" * 70)

    workflows_dir = Path("/home/user/02-python-app/.github/workflows")

    for app_num in range(91, 121):
        workflow_file = workflows_dir / f"app-{app_num:02d}.yml"
        workflow_content = create_ci_cd_workflow(app_num)
        workflow_file.write_text(workflow_content)
        print(f"[{app_num:02d}] CI/CD workflow created ✅")

    print("=" * 70)
    print(f"✨ Successfully created 30 CI/CD workflows (91-120)")

if __name__ == "__main__":
    setup_ci_cd_workflows()
