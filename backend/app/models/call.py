from sqlalchemy import Column, Integer, String, DateTime, Index
from app.core.database import Base

class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True)
    
    external_id = Column(String, unique=True, index=True, nullable=False)
    
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime)
    
    duration = Column(Integer, nullable=False) 
    
    source_number = Column(String, index=True) 
    destination_number = Column(String, index=True)
    
    status_code = Column(Integer)
    
    call_status = Column(String)

    __table_args__ = (Index('ix_call_time_range', 'start_time', 'end_time'),)