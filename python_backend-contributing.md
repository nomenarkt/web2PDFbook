# 🧑‍💻 CONTRIBUTING GUIDELINES (Python / General Backend)

Welcome to this project! This document outlines how to contribute high-quality backend code using Clean Architecture, TDD, and production-grade engineering standards, adapted for Python or cross-language services.

---

## 🔰 Project Architecture

We use **Clean Architecture**:
```
/delivery     → Entry points: FastAPI views, Flask routes, etc.  
/usecase      → Business logic, application services  
/repository   → Persistence adapters: ORM/DB, cache, external APIs  
/domain       → Core entities, value objects, domain services  
```

- **delivery** → invokes **usecase** → which uses **repository**  
- Each layer is decoupled via interfaces/protocols or DI  
- **No cross-layer logic leakage**

---

## 🧠 Development Workflow Rules

### ✅ Implementation

- Only implement what The Architect or Project Owner defines  
- Follow specs exactly: routes, fields, validation, auth, etc.  
- Document assumptions in PRs if unclear  

### ✅ Git Commit & PR Standards

- Format Python code with `black`, `ruff`, `isort`
- Use [Conventional Commits](https://www.conventionalcommits.org/) e.g.  
  - `feat(api): add /refill endpoint`  
  - `fix(auth): correct token expiry logic`

---

## 🧪 Testing Requirements

### Unit Tests

- Every usecase, delivery, and utility module must be tested  
- Use `pytest` with `unittest.mock` or `pytest-mock`  
- Cover:
  - Happy path
  - Validation error
  - Unauthorized/missing token
  - Edge cases

### Integration Tests

- Use `httpx.AsyncClient` with `FastAPI` or `Flask` test clients  
- Include curl or Postman collections for manual QA  
- Example test command:
  ```bash
  pytest -v --cov=./ --cov-report=term-missing
  ```

### Test Locations

- Place test files in same structure under `/tests/`  
  ```
  /tests
    /delivery
    /usecase
    /repository
  ```

---

## 🔒 Security & Auth

- Every protected endpoint must use JWT auth
- Required claims: `user_id`, `email`, `role`
- Middleware must inject user info into `request.state` or `g`
- Authorization checks must enforce role access strictly

---

## 🚀 CI/CD & Automation

- Use **GitHub Actions** for:
  - Linting (`ruff`)
  - Testing (`pytest`)
  - Type checks (`mypy`)
  - Security checks (`bandit`, `safety`)

Example `test.yaml` job:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov
```

---

## 🧾 Documentation

- Each route must have example request/response (OpenAPI or Markdown)
- Inline docstrings for all usecases, models, and public functions
- Shared contracts defined via `pydantic.BaseModel` (for validation & docs)

---

## 🔄 Refactoring & Maintenance

- Refactor using patterns from _Refactoring_ (Fowler), _Clean Code_ (Martin)  
- Break large functions into smaller cohesive units  
- Avoid premature abstraction but ensure DRY and SRP  

---

By following this guide, you’ll ensure that all contributions are testable, maintainable, and production-ready across languages and services.

