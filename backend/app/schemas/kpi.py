from pydantic import BaseModel
from datetime import datetime

class KpiResponse(BaseModel):
    total_calls: int
    answered_calls: int
    asr: float  
    acd: float 

class CallsByHour(BaseModel):
    hour: datetime
    total_calls: int