from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from analytics.kpis import turnover_and_margin

router = APIRouter()

@router.get("/basic")
def get_basic_kpis(db: Session = Depends(get_db)):
    return turnover_and_margin(db)