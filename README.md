# Interview Intel — Knowledge Intelligence Backend

Backend service for the INTEL platform's knowledge-intelligence layer. Seniors submit interview experiences; juniors get AI-generated 8-week preparation plans grounded in real data.

## Prerequisites

- Python 3.11+
- Docker (for RabbitMQ)
- Ollama running locally with `llama3.2` and `nomic-embed-text` models pulled
- Supabase Postgres database with the `vector` extension enabled

## Setup

### 1. Clone and create virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your Supabase connection string and other settings
```

### 3. Start RabbitMQ

```bash
docker compose up -d
```

Management UI: http://localhost:15672 (guest/guest)

### 4. Pull Ollama models

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 5. Run database migration

```bash
alembic upgrade head
```

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/ingest/{id}` | Queue an experience for ingestion (stub) |
| GET | `/status/{id}` | Check ingestion status (stub) |
| POST | `/agent` | Ask for a preparation plan (stub) |

## Development

```bash
# Lint
ruff check app/ tests/

# Format
ruff format app/ tests/

# Test
pytest
```
