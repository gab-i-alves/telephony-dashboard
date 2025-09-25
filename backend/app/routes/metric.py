from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app import schemas, models
from app.core.database import get_db
from app.routes.auth import get_current_user
from app.services.metric import metric_service 

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