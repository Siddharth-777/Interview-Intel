# Interview Intel — Development Conventions

## Architecture
- **Stack**: Python 3.11+, FastAPI, SQLAlchemy 2.0 async, pgvector, RabbitMQ (aio-pika), Ollama
- **DB**: Supabase Postgres via session pooler (port 5432). Vector extension is pre-enabled.
- **Layout**: `app/api/` (thin routers) → `app/services/` (business logic) → `app/models/` (SQLAlchemy) + `app/schemas/` (Pydantic)

## Rules
- Everything is async; no blocking calls in request handlers.
- All config goes through `app/core/config.py` (pydantic-settings). No hardcoded URLs or model names.
- Routers stay thin; logic lives in `services/`.
- All LLM output is parsed into Pydantic models; never trust raw model text.
- Use JSON mode for Ollama structured outputs.
- The agent must answer only from retrieved context and say so when data is insufficient; no hallucinated questions or sources.
- Never log or print secrets; never commit `.env`.
- Add or update tests for every service; mock Ollama and RabbitMQ in tests.
- Run `ruff check app/ tests/` and `pytest` before declaring any step done.
- Build in small steps and stop for review after each.

## Commands
```bash
# Lint
ruff check app/ tests/

# Format
ruff format app/ tests/

# Test
pytest

# Run server
uvicorn app.main:app --reload

# Run migration
alembic upgrade head

# Generate migration
alembic revision --autogenerate -m "description"
```
