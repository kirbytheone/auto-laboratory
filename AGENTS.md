# AGENTS.md

## Project Purpose

Auto Laboratory is a production-style QA Automation and SDET engineering project.

The project combines:

- Django application development
- Django REST Framework
- pytest
- pytest-django
- Playwright with Python
- API testing
- Docker
- GitHub Actions
- future PostgreSQL integration
- future JWT and bearer-token authentication

The goal is to build realistic engineering experience and maintain a portfolio that demonstrates production-oriented QA Automation and SDET practices.

## Repository Architecture

### Django application

`django_app/config/`
- Django project configuration
- root URL routing
- settings
- ASGI and WSGI configuration

`django_app/accounts/`
- user registration
- authentication-related forms and views
- account templates and URLs

`django_app/tasks/`
- task domain models
- task CRUD
- comments and attachments
- permissions and filtering
- task REST API

### Test suites

`django_tests/`
- Django backend and integration tests
- model, view, permission, form, and API coverage

`playwright_tests/`
- browser automation with Playwright and pytest
- Page Object Model
- generated test data
- separate practice and Django application tests

`api_tests/`
- standalone API testing utilities and scenarios
- (Reserved for external HTTP API integration tests.)

## Review Priorities

When reviewing code, prioritize:

1. Correctness and regressions
2. Authentication and authorization behavior
3. Test isolation and repeatability
4. Django application responsibility boundaries
5. Playwright Page Object responsibilities
6. Stable and accessible locators
7. Secret exposure and unsafe configuration
8. CI and Docker compatibility
9. Missing negative and permission coverage
10. Readability, maintainability, and clear naming

## Django Guidelines

- Keep business domains separated into appropriate Django apps.
- Account functionality belongs in `accounts`.
- Task-related functionality belongs in `tasks`.
- Shared project configuration belongs in `config`.
- Prefer named URLs and `reverse()` over hardcoded application paths.
- Keep validation in forms or serializers where appropriate.
- Do not add a new Django app unless it represents a distinct business responsibility.
- Preserve authentication and permission checks when modifying views or APIs.
- Update backend tests when forms, serializers, models, URLs, or required fields change.

## Pytest Guidelines

- Tests must be independent and safe to run in any order.
- Avoid dependencies on manually created local database records.
- Prefer fixtures and generated test data over shared mutable state.
- Use descriptive test names that communicate behavior.
- Test both successful and negative behavior.
- Verify externally visible outcomes instead of implementation details where possible.
- Do not introduce unnecessary global fixtures.
- Keep fixture scope as narrow as practical.

## Playwright Guidelines

- Prefer accessible locators:
  - `get_by_role`
  - `get_by_label`
  - `get_by_text`
- Use IDs or `data-testid` only when they provide better stability or clarity.
- Keep page locators and UI actions inside Page Objects.
- Keep test-data generation outside Page Objects.
- Do not place destination-page locators in an unrelated Page Object.
- Use Playwright assertions with automatic waiting.
- Avoid arbitrary sleeps.
- Preserve test isolation between browser contexts and users.
- Store traces, screenshots, videos, and downloads in the configured artifact directories.

## Test Data and Secrets

- Synthetic passwords used only for generated test users are test data, not secrets.
- Real credentials, API keys, tokens, database passwords, and signing keys must not be committed.
- Secrets must come from environment variables, GitHub Actions secrets, Docker configuration, or a future secrets manager.
- `.env` must remain ignored.
- `.env.example` must contain placeholders only.
- Generated usernames and emails should remain unique between test runs.

## API Guidelines

- Validate status codes and response bodies.
- Cover unauthenticated and unauthorized access.
- Separate schema validation from business-rule validation.
- Keep serializers, permissions, and views focused on their responsibilities.
- Avoid test-only production endpoints unless explicitly protected and justified.
- Future JWT and bearer-token implementations must include refresh, expiration, invalid-token, and permission scenarios.

## Engineering Constraints

- Do not introduce abstractions without a current need.
- Do not replace readable code with unnecessary complexity.
- Do not exaggerate framework maturity or production readiness.
- Prefer incremental changes with focused pull requests.
- Preserve backward compatibility unless the change intentionally modifies the contract.
- When application behavior changes, update both backend and UI automation coverage where relevant.

## Pull Request Review Expectations

For each pull request:

- identify correctness bugs
- flag security or secret-handling risks
- identify brittle or order-dependent tests
- check whether application changes require test updates
- check whether Page Objects have mixed responsibilities
- identify missing negative or permission scenarios
- flag CI, Docker, dependency, or environment risks
- avoid purely stylistic comments unless they materially improve clarity
- provide concise, actionable feedback with file and line references

## Current Development Workflow

1. Create a focused feature branch.
2. Implement the feature.
3. Verify manually where appropriate.
4. Add or update automated tests.
5. Run relevant local suites.
6. Commit and push.
7. Open a pull request.
8. Run GitHub Actions.
9. Request Codex review.
10. Evaluate and address justified findings.
11. Merge into `main`.
12. Delete the completed feature branch.

## Account identity rules

- Username is required and unique.
- Email is required.
- Email is normalized before persistence.
- Email uniqueness is case-insensitive.
- The current form-level uniqueness validation will later be reinforced with 
- a database constraint through a custom user model.