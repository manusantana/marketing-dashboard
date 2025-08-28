# backend/schemas/kpis.py
from pydantic import BaseModel

class KpiBasicResponse(BaseModel):
    turnover: float
    margin: float
