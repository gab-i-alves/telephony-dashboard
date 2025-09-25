from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from .. import models, schemas
from typing import List

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

call_repo = CallRepository()