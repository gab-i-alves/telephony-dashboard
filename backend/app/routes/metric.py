from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app import schemas, models
from app.core.database import get_db
from app.routes.auth import get_current_user
from app.services.metric import metric_service 
from app.repositories.call import call_repo

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)

@router.get("/kpis", response_model=schemas.KpiResponse)
def read_kpis(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    start_date: datetime | None = None,
    end_date: datetime | None = None
):
    return metric_service.get_kpis(db, start_date=start_date, end_date=end_date)

@router.get("/calls_by_hour", response_model=List[schemas.CallsByHour])
def read_calls_by_hour(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    start_date: datetime | None = None,
    end_date: datetime | None = None
):
    return call_repo.get_calls_by_hour(db, start_date=start_date, end_date=end_date)

@router.get("/calls_by_day", response_model=List[schemas.CallsByHour])
def read_calls_by_day(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    start_date: datetime | None = None,
    end_date: datetime | None = None
):
    results = call_repo.get_calls_by_day(db, start_date=start_date, end_date=end_date)
    return [{"hour": r.day, "total_calls": r.total_calls} for r in results]