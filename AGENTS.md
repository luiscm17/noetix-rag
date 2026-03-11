# AGENTS.md - Agent Development Guidelines

## Project Overview

Python-based AI agent project using FastAPI and `agent-framework`. Supports multiple AI providers (OpenAI, Azure AI Foundry, Ollama).

- **Python**: 3.13+ | **Package Manager**: uv | **Framework**: FastAPI

---

## Build, Lint, and Test Commands

### Installation & Running

```bash
uv sync                                    # Install dependencies
uv run python main.py                      # Run main app
uv run uvicorn src.main:app --reload       # Run FastAPI server
```

### Linting & Type Checking

```bash
uv run ruff check .                        # Lint with ruff
uv run ruff format .                       # Format code
uv run mypy src/                           # Type check with mypy
```

### Testing

```bash
uv run pytest                              # Run all tests
uv run pytest tests/test_file.py           # Run single test file
uv run pytest tests/test_file.py::test_fn  # Run single test function
uv run pytest -k "pattern"                 # Run tests matching pattern
uv run pytest -v                           # Verbose output
uv run pytest -m "marker"                  # Run tests with specific marker
uv run pytest --tb=short                   # Shorter traceback output
uv run pytest --cov=src --cov-report=html  # With coverage
```

### Database Migrations (Alembic)

```bash
uv run alembic current                     # Check current migration
uv run alembic upgrade head                # Run all pending migrations
uv run alembic downgrade -1                # Rollback last migration
uv run alembic revision --autogenerate -m "create users table"  # Create new migration
```

### Development Workflow

```bash
uv run python main.py                      # Run main app
uv run uvicorn src.main:app --reload       # Run FastAPI server with hot reload
cp .env.example .env                       # Set up environment variables
```

---

## Before Committing

Always verify your changes before committing:

```bash
uv run ruff check .    # Lint
uv run ruff format .   # Format
uv run mypy src/       # Type check
uv run pytest          # Run tests
```

---

## Code Style Guidelines

### Imports
- Use **absolute imports**: `from config.settings import AgentSettings`
- Order: standard library → third-party → local application
- Use explicit relative imports for intra-package: `from . import module`
- **No wildcard imports** (`from x import *`)

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Functions/Variables | snake_case | `def get_settings()` |
| Classes | PascalCase | `class TeacherAgent` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES = 5` |
| Files (modules) | snake_case | `base_agent.py` |
| Async functions | `async def` | `async def build(...)` |

### Type Hints
- **Always use type hints** for parameters and return types
- Use `typing` module for complex types: `list[str] | None`, `dict[str, Any]`
- Avoid `Any` unless absolutely necessary

### Async/Await
- Use `async def` for I/O operations
- Always `await` async functions - never `.result()` or `.wait()`
- Use `asyncio` for concurrent operations when appropriate

### Docstrings
- Use triple double-quotes `"""`
- Present tense, third person
- Include Args/Returns/Raises for complex functions

### Error Handling
- Use specific exception types (`ValueError`, `RuntimeError`, etc.)
- Provide descriptive error messages
- Validate inputs at function entry points

### Class Structure
- Use ABC for interfaces with `@abstractmethod`
- Keep classes focused on single responsibility
- Use dependency injection for external services

---

## Project Structure

```
mh-agent/
├── src/
│   ├── agents/           # Agent implementations
│   ├── api/routes/      # FastAPI routes (health.py, documents.py)
│   ├── config/           # Configuration modules
│   │   └── settings.py  # DBSettings with DATABASE_URL
│   ├── domain/           # Domain layer (entities, interfaces, services)
│   ├── infrastructure/  # Repository implementations
│   │   └── db/
│   │       └── connection.py  # SQLAlchemy engine & session
│   └── main.py           # Application entry point
├── migrations/           # Alembic migrations
├── tests/                # Test files
├── alembic.ini          # Alembic configuration
├── pyproject.toml
├── .env
└── .python-version
```

---

## Architecture

This project follows **Clean Architecture** with domain-driven design principles:
- **Domain Layer**: Entities, interfaces, business rules (no external dependencies)
- **Infrastructure Layer**: Repository implementations, external services
- **API Layer**: FastAPI routes, dependency injection
- **Agents Layer**: AI agent implementations using `agent-framework`

---

## Skills

Available in `.agents/skills/`:
- `agent-orchestration` - Multi-agent coordination
- `ai-agents-architect` - Designing autonomous AI agents
- `microsoft-agent-framework` - Microsoft Agent Framework
- `rag-engineer` - Retrieval-Augmented Generation
- `architecture-patterns` - Clean Architecture, Hexagonal, DDD
- `brainstorming` - Feature creation and requirements
- `systematic-debugging` - Bug investigation and fixing

---

## Common Patterns

### Provider Pattern (AI Backends)
```python
class OpenAIProvider(BaseAgent):
    async def build(self, name: str, instructions: str, tools: list | None = None):
        client = OpenAIChatClient(
            model_id=AgentSettings.OPENAI_MODEL_ID,
            base_url=AgentSettings.OPENAI_ENDPOINT,
            api_key=AgentSettings.OPENAI_API_KEY,
        ).as_agent(name=name, instructions=instructions, tools=tools or [])
        return client
```

### Repository Pattern
```python
class BlobDocumentRepository(DocumentRepository):
    def __init__(self, container_client: ContainerClient):
        self._container = container_client
```

### Testing Async Agents
```python
@pytest.mark.asyncio
async def test_teacher_agent_run():
    agent = await teacher_agent()
    result = await agent.run("What is Python?")
    assert result is not None
```
