import contextlib
from fastapi import FastAPI
from app.core.database.session import engine, Base
from app.modules.inspect.router import router as inspect_router
from app.modules.feedback.router import router as feedback_router
from app.modules.transactions.router import router as transactions_router
from app.modules.transactions.models import Transaction

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB (create tables if they don't exist)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="ShopFloor Copilot",
    version="1.0.0",
    description="AI-assisted visual inspection and SOP agent.",
    lifespan=lifespan
)

app.include_router(inspect_router)
app.include_router(feedback_router)
app.include_router(transactions_router)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
