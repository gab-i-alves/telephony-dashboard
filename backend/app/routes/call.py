from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.database import get_db
from app.routes.auth import get_current_user
from app.services.call import call_service

router = APIRouter(
    prefix="/calls",
    tags=["Calls"]
)

@router.post("/ingest", status_code=200)
async def ingest_calls(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    result = await call_service.ingest_calls_from_external_api(db)
    return result