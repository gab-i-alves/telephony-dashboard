from pydantic import BaseModel
from datetime import datetime

class CallBase(BaseModel):
    external_id: str
    start_time: datetime
    end_time: datetime | None
    duration: int
    source_number: str | None
    destination_number: str | None
    status_code: int | None = None
    call_status: str | None = None

class CallCreate(CallBase):
    pass

class Call(CallBase):
    id: int

    class Config:
        from_attributes = True