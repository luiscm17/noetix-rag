# Neotix RAG

AI-powered document management system with autonomous agents.

## Tech Stack

- **Backend**: FastAPI (Python 3.13+)
- **Database**: PostgreSQL + SQLAlchemy
- **Vector DB**: Qdrant
- **Cache/Sessions**: Redis
- **Blob Storage**: Azure Blob Storage
- **Auth**: JWT with Redis blacklist

## Getting Started

```bash
# Install dependencies
uv sync

# Copy environment
cp .env.example .env

# Run migrations
uv run alembic upgrade head

# Start server
uv run uvicorn src.main:app --reload
```

## API Documentation

See [docs/API.md](docs/API.md) for complete API reference.

## Project Structure

```yml
src/
├── agents/          # AI agents (RAG, Teacher, Socratic, etc.)
├── api/            # FastAPI routes and schemas
├── application/    # Use cases
├── config/         # Settings
├── domain/         # Entities and interfaces
├── infrastructure/ # Repositories and services
└── rag/            # RAG pipeline
```

## Development

```bash
# Lint
uv run ruff check .

# Format
uv run ruff format .

# Test
uv run pytest tests/unit/
```
