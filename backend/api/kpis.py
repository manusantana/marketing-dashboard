# backend/api/kpis.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from analytics.kpis import turnover_and_margin
from schemas.kpis import KpiBasicResponse

router = APIRouter(prefix="/kpis", tags=["KPIs"])

@router.get("/basic", response_model=KpiBasicResponse)
def kpis_basic(db: Session = Depends(get_db)):
    return turnover_and_margin(db)

