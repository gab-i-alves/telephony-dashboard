from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime as dta
from typing import List

from app import schemas, models
from app.core.database import get_db
from app.routes.auth import get_current_user
from app.services.call import call_service
from app.repositories.call import call_repo
from app.schemas.pagination import PaginatedResponse

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

@router.get("/", response_model=PaginatedResponse[schemas.Call])
def read_calls(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(100, ge=1, le=500, description="Registros por página"),
    start_date: dta | None = None,
    end_date: dta | None = None
):

    skip = (page - 1) * limit
    calls = call_repo.get_calls(db, skip=skip, limit=limit, start_date=start_date, end_date=end_date)
    total = call_repo.get_calls_count(db, start_date=start_date, end_date=end_date)
    
    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        data=calls
    )