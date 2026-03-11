# AGENTS.md - Agent Development Guidelines

## Project Overview

Python-based AI agent project using FastAPI. Supports multiple AI providers (OpenAI, Azure AI Foundry, Ollama).

- **Python**: 3.13+ | **Package Manager**: uv | **Framework**: FastAPI

---

## Build, Lint, and Test Commands

### Installation & Running

```bash
uv sync                                    # Install dependencies
uv run python -m src.main                 # Run main app
uv run uvicorn src.main:app --reload      # Run FastAPI with hot reload
cp .env.example .env                      # Set up environment variables
```

### Linting & Type Checking

```bash
uv run ruff check .                       # Lint with ruff
uv run ruff format .                      # Format code
uv run mypy src/                          # Type check with mypy
```

### Testing

```bash
uv run pytest                             # Run all tests
uv run pytest tests/unit/                 # Run unit tests only (recommended)
uv run pytest tests/test_file.py          # Run single test file
uv run pytest tests/test_file.py::test_fn # Run single test function
uv run pytest -k "pattern"                # Run tests matching pattern
uv run pytest -v                          # Verbose output
```

### Database Migrations (Alembic)

```bash
uv run alembic current                    # Check current migration
uv run alembic upgrade head               # Run all pending migrations
uv run alembic downgrade -1               # Rollback last migration
uv run alembic revision --autogenerate -m "message"  # Create new migration
```

---

## Before Committing

Always verify your changes before committing:

```bash
uv run ruff check . && uv run ruff format . && uv run mypy src/ && uv run pytest tests/unit/
```

---

## Code Style Guidelines

### Imports
- Use **absolute imports**: `from src.config.settings import AuthSettings`
- Order: standard library → third-party → local application
- Use explicit relative imports for intra-package: `from . import module`
- **No wildcard imports** (`from x import *`)

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Functions/Variables | snake_case | `def get_settings()` |
| Classes | PascalCase | `class UserRepository` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES = 5` |
| Files | snake_case | `base_agent.py` |
| Interfaces (Ports) | PascalCase with `I` prefix | `class IUserRepository` |

### Type Hints & Async
- **Always use type hints** for parameters and return types
- Use `Optional[X]` for compatibility: `Optional[str]`
- Use `async def` for I/O operations, always `await` - never `.result()`
- Mark async test functions with `@pytest.mark.asyncio`

### Pydantic Models
- Use `model_config = ConfigDict(...)` instead of `class Config`
- Example:
```python
class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: Optional[int] = Field(default=None)
    email: EmailStr
```

### Docstrings
- Use triple double-quotes `"""`
- Present tense, third person
- Keep brief for simple functions

### Error Handling
- Use specific exception types (`ValueError`, `RuntimeError`, etc.)
- Provide descriptive error messages
- Validate inputs at function entry points

---

## Project Structure (Clean Architecture)

```
mh-agent/
├── src/
│   ├── config/                      # Settings, dependencies
│   ├── domain/                     # Entities, interfaces (ports)
│   ├── application/use_cases/     # Business logic
│   ├── infrastructure/             # Adapters (repositories, services)
│   ├── api/routes/                 # FastAPI endpoints
│   └── agents/                     # AI Agents
├── tests/
│   ├── unit/                       # Fast, no external deps
│   ├── integration/                # Requires PostgreSQL + Azurite
│   └── http/                       # REST Client tests
├── migrations/                     # Alembic
├── pyproject.toml
└── .env
```

### Key Patterns

**Interface Pattern** (domain → infrastructure):
```python
# domain/interfaces/user_repository.py
class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]: pass
```

**Use Case Pattern**:
```python
class RegisterUserUseCase:
    def __init__(self, user_repo: IUserRepository, hasher: IPasswordHasher):
        self._user_repo = user_repo
    
    def execute(self, request: RegisterUserRequest) -> RegisterUserResponse:
        pass
```

**Dependency Injection** (FastAPI):
```python
def get_user_repository(session: Session = Depends(get_db)) -> IUserRepository:
    return UserRepository(session)
```

---

## Testing Guidelines

### Unit Tests
- Use mocks for external services (repositories, hashers)
- Test use cases, services, entities, interfaces
- Run fast, no external dependencies

### Integration Tests
- Use FastAPI TestClient with `app.dependency_overrides`
- Require PostgreSQL and Azurite running

### Mocking Pattern
```python
from src.config.dependencies import get_user_repository, get_password_hasher

def test_register_success(self):
    mock_repo = Mock()
    mock_hasher = Mock()
    
    app.dependency_overrides[get_user_repository] = lambda: mock_repo
    app.dependency_overrides[get_password_hasher] = lambda: mock_hasher
```

---

## Common Issues

### Migrations
- Run `alembic upgrade head` after creating new models
- Import models in `migrations/env.py`: `from src.infrastructure.db import models`

### Test Failures
- Clear `app.dependency_overrides` in `teardown_method`
- Use unique emails in tests to avoid DB conflicts

### Pydantic Deprecation
- Use `ConfigDict` instead of `class Config`
- Use `field_validator` for validation
