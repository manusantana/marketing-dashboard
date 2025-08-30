from pydantic import BaseModel
from typing import List, Dict, Any

class KpiBasicResponse(BaseModel):
    turnover: float
    margin: float

class KpiAbcResponse(BaseModel):
    A: List[Dict[str, Any]]
    B: List[Dict[str, Any]]
    C: List[Dict[str, Any]]

class KpiChurnResponse(BaseModel):
    churn_rate: float
    active_customers: int
    lost_customers: int
    period_days: int
