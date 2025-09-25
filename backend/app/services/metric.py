from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories.call import call_repo
from app.schemas.kpi import KpiResponse

class MetricService:
    def get_kpis(
        self, db: Session, *, 
        start_date: datetime | None = None, end_date: datetime | None = None
    ) -> KpiResponse:
        
        kpi_data = call_repo.get_kpis(db, start_date=start_date, end_date=end_date)
        
        return KpiResponse(**kpi_data)

metric_service = MetricService()