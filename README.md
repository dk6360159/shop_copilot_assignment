# ShopFloor Copilot

AI-assisted visual inspection and SOP agent for the Forward-Deployed Engineer assignment.

## Architecture

This project follows a strict Router-Service-Repository pattern. Features are encapsulated within modules in `app/modules/`.
Database interactions are performed asynchronously using SQLAlchemy and PostgreSQL.

FastAPI -> Module Router -> Module Service -> Transaction Repository -> Async PostgreSQL.

Every inspection produces an append-only audit record. Feedback updates an epsilon-greedy contextual bandit.

## Requirements

- Docker and docker-compose
- Tesseract OCR installed and available on PATH (If running locally without Docker)
- Ollama installed and available on network/host

## Setup (Docker)

Ensure your Ollama service is running and accessible (e.g. at `http://host.docker.internal:11434` for Docker Desktop on Windows/Mac, or `http://localhost:11434` if using host network).
Adjust the `OLLAMA_BASE_URL` in `.env.example` if needed.

1. Create your `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Build and start the services:
   ```bash
   docker-compose up --build -d
   ```

This will start:
- A PostgreSQL database (`db`) on port 5432.
- The FastAPI application (`api`) on port 8000.

## Endpoints

Health:

```bash
curl http://127.0.0.1:8000/health
```

Inspection:

```bash
curl -X POST http://127.0.0.1:8000/inspect ^
  -F "query=Is this part within tolerance?" ^
  -F "work_order_id=WO-1001" ^
  -F "image=@data/images/surface_scratch.png"
```

Feedback:

```bash
curl -X POST http://127.0.0.1:8000/feedback ^
  -H "Content-Type: application/json" ^
  -d "{\"transaction_id\":\"YOUR_ID\",\"score\":1}"
```

Audit replay:

```bash
curl http://127.0.0.1:8000/transactions/YOUR_ID
```

## Scope
This repository intentionally avoids production authentication, multi-tenancy, cloud AI APIs, deep model training, and mobile UI because those are explicitly out of scope for the assignment.
