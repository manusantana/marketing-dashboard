from sqlalchemy.orm import Session
from db.models import Sale

def turnover_and_margin(db):
    sales = db.query(Sale).all()
    turnover = sum(s.amount for s in sales)   # ✅ amount
    margin = sum(s.margin for s in sales)     # ✅ margin
    return {
        "turnover": turnover,
        "margin": margin,
    }


