# AGENTS.md - Agent Development & Operations Guidelines

## Project Overview

This repository houses a production-ready Python-based AI agent system using FastAPI. It supports multiple AI providers: OpenAI, Azure AI Foundry, and Ollama.

- **Python**: 3.13+
- **Package Manager**: [uv](https://github.com/astral-sh/uv) *(faster pip replacement)*
- **Web Framework**: FastAPI
    
---

## Build, Lint & Test Commands

All commands assume you run from the workspace root directory.

### Environment Setup
```bash
uv sync                             # Install all dependencies
cp .env.example .env                # Create your .env if it doesn't exist
# (Edit .env to provide API keys etc as needed)
```

### Running the Application
```bash
uv run python -m src.main           # Run main app (production style)
uv run uvicorn src.main:app --reload # Local dev hot-reload
```

### Linting, Formatting, Type-checking
```bash
uv run ruff check .                 # Lint with ruff
uv run ruff format .                # Auto-format with ruff
uv run mypy src/                    # Type check with mypy
```

### Testing
```bash
uv run pytest                             # Run all tests
uv run pytest tests/unit/                 # Unit tests (recommended, fast)
uv run pytest tests/test_file.py          # Run single test file
uv run pytest tests/test_file.py::test_fn # Run single test function
uv run pytest -k "pattern"                # Run tests matching pattern/substring
uv run pytest -v                          # Verbose output
uv run pytest --cov=src --cov-report=term-missing  # With coverage
```

### Database Migrations (Alembic)
```bash
uv run alembic current                    # Show current migration
uv run alembic upgrade head               # Run all migrations
uv run alembic downgrade -1               # Roll back one migration
uv run alembic revision --autogenerate -m "msg"  # New migration from changes
```

### Pre-Commit Routine
```bash
uv run ruff check . && \
uv run ruff format . && \
uv run mypy src/ && \
uv run pytest tests/unit/
```

---

## Code Style Guidelines

Follow these rules for maximum compatibility with agent automation and peer developers:

### Imports
- Use **absolute imports** for cross-package imports: `from src.config.settings import AuthSettings`
- **Import Order:** standard library > third-party > local application modules
- For intra-package, use explicit relative imports: `from . import module`
- **Avoid wildcard imports** (`from x import *`)
- Remove unused imports aggressively

### Naming Conventions

| Element          | Convention               | Example                   |
|------------------|--------------------------|---------------------------|
| Functions/Vars   | snake_case               | `def get_settings()`      |
| Classes          | PascalCase               | `class UserRepository`    |
| Constants        | UPPER_SNAKE_CASE         | `MAX_RETRIES = 5`         |
| Files            | snake_case               | `base_agent.py`           |
| Interfaces (Ports)| PascalCase with `I`     | `class IUserRepository`   |

### Type Hints & Async
- **Always** use type hints for all public and private functions
- Use `Optional[X]` for optional arguments, not just `X | None`
- For I/O ops, use `async def` and always `await` (`never .result()`)
- Mark async tests with `@pytest.mark.asyncio` so they're picked up
- Configure `asyncio_mode = "auto"` in `pytest.ini_options` (already set)

### Formatting & Style
- Max line length: **100** (`pyproject.toml` enforced by ruff/mypy)
- Prefer single quotes, except for docstrings
- Blank lines per PEP8; run `uv run ruff format .`
- Place all type-only imports under `if TYPE_CHECKING:` blocks

### Pydantic Models
- Use `model_config = ConfigDict(...)` (not legacy `class Config`)
- Example:
    ```python
    class User(BaseModel):
        model_config = ConfigDict(from_attributes=True)
        user_id: Optional[int] = Field(default=None)
        email: EmailStr
    ```

### Error Handling
- Use specific built-in exceptions (e.g., `ValueError`, `RuntimeError`, not plain `Exception`)
- Give meaningful, actionable error messages
- Validate external input at function entrypoint and API boundary

---

## Clean Architecture & Project Structure

```
src/
├── config/           # Settings, DI containers, etc.
├── domain/           # Entities, interfaces (ports/abstractions)
├── application/      # Use cases (business logic)
├── infrastructure/   # Adapters: repo impls, services, I/O
├── api/routes/       # FastAPI endpoint definitions
└── agents/           # Autonomous agent modules

tests/
├── unit/             # Fast unit tests, no ext. deps
├── integration/      # Tests: DB/Azurite (requires running infra)
├── http/             # REST Client/E2E tests
migrations/           # Alembic migrations
```

- **Interface pattern**: `class IUserRepository(ABC): ...`
- **Use case pattern**: see below.

```python
class RegisterUserUseCase:
    def __init__(self, user_repo: IUserRepository, hasher: IPasswordHasher):
        self._user_repo = user_repo
    def execute(self, req: RegisterUserRequest) -> RegisterUserResponse:
        ...
```

### Dependency Injection
```python
def get_user_repository(session: Session = Depends(get_db)) -> IUserRepository:
    return UserRepository(session)
```

---

## Testing Guidance for Agents

- Mock external services when writing unit tests (repos, hashing, I/O)
- Target use cases, entities, and services in unit tests -- should NOT require DB/services
- Integration tests: require PostgreSQL and Azurite, override dependencies as needed
- Use FastAPI `TestClient` plus `app.dependency_overrides` for HTTP and integration level tests

### Mocking Pattern
```python
app.dependency_overrides[get_user_repository] = lambda: mock_repo
```
- Always clear dependency overrides in `teardown_method` to prevent test cross-talk
- Use **unique emails/usernames** to avoid DB conflicts in test runs

---

## Common Issues & Gotchas

- Always run `alembic upgrade head` after model changes + migration generation
- Alembic configuration: import your models in `migrations/env.py`:
    ```python
    from src.infrastructure.db import models
    ```
- If agent errors mention missing env vars, check your `.env` is present and populated
- Ensure all secrets/API keys are in `.env` and **never** committed to VCS
- Automated agents: always verify test and lint status after code edits

---

## Agentic Workflow Tips

- All commands here are safe for automation and agentic operation
- Agents: If your environment changes, rerun `uv sync`
- Test iteratively, frequently, and thoroughly
- Format and lint after every code edit; do not skip
- If you detect new environment variables, update `.env.example` for others/agents
- Project has agent skills in `.agents/skills/` — use the `skill` tool to load them for specialized tasks

---

For further help, see the documentation in `src/` or ask a human reviewer for conventions not covered here.
