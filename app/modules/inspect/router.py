from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database.session import get_db
from app.modules.inspect.schemas import InspectResponse
from app.modules.inspect.service import InspectionService
from app.modules.transactions.repository import TransactionRepository
from app.modules.transactions.service import TransactionService

router = APIRouter(prefix="", tags=["inspection"])

def get_inspection_service(db: AsyncSession = Depends(get_db)) -> InspectionService:
    repo = TransactionRepository(db)
    tx_service = TransactionService(repo)
    return InspectionService(tx_service)

@router.post("/inspect", response_model=InspectResponse)
async def inspect(
    query: str = Form(...),
    work_order_id: str | None = Form(default=None),
    image: UploadFile | None = File(default=None),
    service: InspectionService = Depends(get_inspection_service)
):
    if not query.strip():
        raise HTTPException(status_code=400, detail="query must not be empty")

    image_bytes = await image.read() if image else None
    image_name = image.filename if image else None

    try:
        result = await service.inspect(
            query=query,
            work_order_id=work_order_id,
            image_bytes=image_bytes,
            image_name=image_name,
        )
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

