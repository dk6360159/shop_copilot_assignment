## first Step

From provide file in Email  gemini API key i am using Gemini LLM model here for response generation, put that api key .env.example file 


## Architecture

This project follows a strict Router-Service-Repository pattern. Features are encapsulated within modules in 

`app/modules/`.
Database interactions are performed asynchronously using SQLAlchemy and PostgreSQL.

FastAPI -> Module Router -> Module Service -> Transaction Repository -> Async PostgreSQL.

Every inspection produces an append-only audit record. Feedback updates an epsilon-greedy contextual bandit.


## Requirements

- Docker and docker-compose
- Docker Desktop


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


