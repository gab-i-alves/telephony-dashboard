from pydantic import BaseModel

class KpiResponse(BaseModel):
    total_calls: int
    answered_calls: int
    asr: float  
    acd: float 