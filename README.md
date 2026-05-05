# Auto Laboratory

QA automation project using Python, pytest, Selenium, Playwright, Django, and CI/CD(Jenkins).

## Current API testing stack

- Python
- pytest
- requests
- jsonschema

## API framework structure

```text
api_tests/
├── clients/
│   ├── base_client.py
│   └── jsonplaceholder_client.py
├── data/
│   └── post_payloads.py
├── schemas/
│   └── post_schema.py
├── tests/
│   └── test_posts.py
├── conftest.py
└── validators.py
```
## RUN TESTS
```Bash
pytest api_tests -v
```

