from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from services.kpis import get_basic_kpis

router = APIRouter()

@router.get("/basic")
def read_basic_kpis(db: Session = Depends(get_db)):
    return get_basic_kpis(db)
