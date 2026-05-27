# QA Automation Laboratory | Python API, UI & Django Test Framework

Portfolio project demonstrating practical QA automation engineering across API, UI, and backend testing.

This repository demonstrates API testing, UI automation, Django backend testing, 
and automated test reporting using Python-based tools.

## Current Status

This project is actively evolving with additional testing capabilities and framework integrations.

Implemented:
- API tests with pytest and requests
- Selenium UI tests
- Playwright UI tests
- Django task management web application
- Django model and view tests
- Django file attachment upload/download/delete test coverage
- Test screenshots and reports structure

In progress:
- HTML reporting
- CI/CD pipeline integration
- Django REST Framework API endpoints + tests
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

## Tech Stack

- Python
- pytest
- requests
- Selenium
- Playwright
- Django
- pytest-django
- pytest-html
- Git
- Page Object Model design

## Project Structure

```text
auto-laboratory/
├── api_tests/                # API automation with pytest + requests
├── selenium_tests/           # Selenium UI automation
├── playwright_tests/         # Playwright UI automation
├── django_app/
│   ├── config/              # Django project configuration
│   ├── tasks/               # Task manager application
│   ├── manage.py
│   └── db.sqlite3
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