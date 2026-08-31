# QA Automation Laboratory | Python API, UI & Django Test Framework

Portfolio project demonstrating practical QA automation engineering across API, UI, and backend testing.

This repository demonstrates API testing, UI automation, Django backend testing, 
and automated test reporting using Python-based tools.

## Current Status

This project is actively evolving with additional testing capabilities and framework integrations.

Implemented:
- DRF backend tests using pytest-django. External API contract tests will be added separately.
- Playwright UI tests
- Django task management web application
- Django model and view tests
- Django file attachment upload/download/delete test coverage
- Test screenshots and reports structure

In progress:
- Expanded Playwright end-to-end scenarios
- Authentication flow improvements

## Test Coverage

Current coverage includes:
- API response validation
- UI interaction testing
- Django model testing
- Django view testing
- Authentication access checks
- File upload/download/delete validation

## API Integration Tests

`api_tests` contains black-box HTTP tests for the running Auto Laboratory API.

These tests use:

- `pytest` for test execution and fixtures
- `requests` for real HTTP communication
- JWT authentication
- PostgreSQL-backed Django/DRF application

Unlike `django_tests`, these tests do not use Django internals such as ORM models, `APIClient`, `reverse()`, or Django settings.

### Local execution

Start PostgreSQL and the Django application first.

For Docker:

```bash
docker compose up --build -d

## Tech Stack

- Python
- pytest
- requests
- Playwright
- Django
- pytest-django
- pytest-html
- Git
- Page Object Model design
- PostgreSQL

## Database: PostgreSQL 17

Local development:
- PostgreSQL provided by Docker Compose
- Django may run locally against 127.0.0.1:5432
- Dockerized Django connects using POSTGRES_HOST=db

Required environment variables:
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT

Schema setup for docker startup:
```bash
docker compose up -d db
python django_app/manage.py migrate
python django_app/manage.py runserver
```
full container mode:
```bash
docker compose build
docker compose run --rm web python django_app/manage.py migrate
docker compose up
```
### DB RESET
!!!Deletes containers and the PostgreSQL named volume, permanently removing local development database data!!!
```bash
docker compose down -v
```

## Project Structure

```text
auto-laboratory/
├── api_tests/                # API automation with pytest + requests
├── playwright_tests/         # Playwright UI automation
├── django_app/
│   ├── config/              # Django project configuration
│   ├── tasks/               # Task manager application
│   ├── manage.py
├── django_tests/            # Django backend tests
├── utils/                   # Shared helpers/utilities
├── docs/
├── screenshots/
├── playwright-report/
├── playwright_downloads/
├── requirements.txt
├── pytest.ini
└── README.md
```

## How to Run Tests

Install dependencies:
```bash
pip install -r requirements.txt
```
Run all tests:
```bash
pytest
```
Run Django tests:
```bash
pytest django_tests
```
Run tests with HTML report:
```bash
pytest --html=reports/report.html --self-contained-html
```
## Purpose

The goal of this project is to show practical QA automation skills across backend, API, UI, and Django 
application testing.

This repository serves as a practical QA automation portfolio project demonstrating real-world testing approaches 
and framework design.