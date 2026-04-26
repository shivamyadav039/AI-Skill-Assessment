# Backend README

This is the FastAPI backend for the AI-Powered Skill Assessment Agent.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env

# Run development server
uvicorn app.main:app --reload
```

## Directory Structure

- `app/main.py` - Main FastAPI application & endpoints
- `app/agents/` - AI agent implementations
- `app/services/` - Business logic services
- `app/models/` - SQLAlchemy ORM models
- `app/schemas/` - Pydantic request/response schemas
- `app/db/` - Database utilities & migrations
- `app/utils/` - Helper functions
- `tests/` - Unit and integration tests

## API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI.

## Environment Variables

See `.env.example` for all configuration options.

## Next Steps

1. Implement NLP services for skill extraction
2. Integrate Claude/GPT API
3. Set up PostgreSQL database with pgvector
4. Implement assessment agents
5. Add RAG for resource curation
