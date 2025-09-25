from sqlalchemy.orm import Session
from sqlalchemy import desc, func, case, Date, cast
from sqlalchemy.dialects.postgresql import insert
from app import models, schemas
from typing import List, Dict, Any
from datetime import datetime as dta

class CallRepository:
    def create_call(self, db: Session, *, call_in: schemas.CallCreate) -> models.Call:
        db_call = models.Call(**call_in.model_dump())
        db.add(db_call)
        db.commit()
        db.refresh(db_call)
        return db_call

    def bulk_insert_calls(self, db: Session, *, calls_in: List[schemas.CallCreate]) -> None:
        if not calls_in:
            return

        calls_data = [c.model_dump() for c in calls_in]

        query = insert(models.Call).values(calls_data)
        
        query = query.on_conflict_do_nothing(
            index_elements=['external_id']
        )
        
        db.execute(query)
        db.commit()

    def get_calls(
        self, db: Session, *, skip: int = 0, limit: int = 100, 
        start_date: dta | None = None, end_date: dta | None = None
    ) -> List[models.Call]:
        query = db.query(models.Call)

        if start_date:
            query = query.filter(models.Call.start_time >= start_date)
        if end_date:
            query = query.filter(models.Call.start_time <= end_date)

        return query.order_by(desc(models.Call.start_time)).offset(skip).limit(limit).all()

    def get_calls_count(
        self, db: Session, *, 
        start_date: dta | None = None, end_date: dta | None = None
    ) -> int:
        query = db.query(models.Call)

        if start_date:
            query = query.filter(models.Call.start_time >= start_date)
        if end_date:
            query = query.filter(models.Call.start_time <= end_date)
            
        return query.count()

    def get_kpis(
        self, db: Session, *, 
        start_date: dta | None = None, end_date: dta | None = None
    ) -> Dict[str, Any]:
        query = db.query(
            func.count(models.Call.id).label("total_calls"),
            func.sum(
                case(
                    (models.Call.status_code == 200, 1),
                    else_=0
                )
            ).label("answered_calls"),
            func.avg(
                case(
                    (models.Call.status_code == 200, models.Call.duration),
                    else_=None
                )
            ).label("acd")        
        )

        if start_date:
            query = query.filter(models.Call.start_time >= start_date)
        if end_date:
            query = query.filter(models.Call.start_time <= end_date)
        
        results = query.one()
        
        total_calls = results.total_calls or 0
        answered_calls = results.answered_calls or 0
        acd = results.acd or 0.0

        asr = (answered_calls / total_calls * 100) if total_calls > 0 else 0.0

        return {
            "total_calls": total_calls,
            "answered_calls": answered_calls,
            "asr": round(asr, 2),
            "acd": round(float(acd), 2)
        }

    def get_calls_by_hour(
        self, db: Session, *, 
        start_date: dta | None = None, end_date: dta | None = None
    ) -> List[Dict[str, Any]]:
        hour_series = func.date_trunc('hour', models.Call.start_time)

        query = db.query(
            hour_series.label('hour'),
            func.count(models.Call.id).label('total_calls')
        ).group_by('hour').order_by('hour')

        if start_date:
            query = query.filter(models.Call.start_time >= start_date)
        if end_date:
            query = query.filter(models.Call.start_time <= end_date)

        return query.all()

    def get_calls_by_day(
        self, db: Session, *, 
        start_date: dta | None = None, end_date: dta | None = None
    ) -> List[Dict[str, Any]]:
        day_series = func.date_trunc('day', models.Call.start_time)
        query = db.query(
            day_series.label('day'),
            func.count(models.Call.id).label('total_calls')
        ).group_by('day').order_by('day')
        if start_date:
            query = query.filter(models.Call.start_time >= start_date)
        if end_date:
            query = query.filter(models.Call.start_time <= end_date)
        return query.all()

call_repo = CallRepository()