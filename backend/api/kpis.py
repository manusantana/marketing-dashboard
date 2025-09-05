# backend/api/kpis.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from analytics.kpis import get_basic_kpis, abc_by
from schemas.kpis import KpiAbcResponse, KpiBasicResponse

router = APIRouter(prefix="/kpis", tags=["KPIs"])


@router.get("/basic", response_model=KpiBasicResponse)
def kpis_basic(db: Session = Depends(get_db)):
    return get_basic_kpis(db)


@router.get("/abc/products", response_model=KpiAbcResponse)
def kpis_abc_products(db: Session = Depends(get_db)):
    return abc_by(db, "product")


@router.get("/abc/customers", response_model=KpiAbcResponse)
def kpis_abc_customers(db: Session = Depends(get_db)):
    return abc_by(db, "customer")
