from sqlalchemy.orm import Session
from db.models import Sale

def turnover_and_margin(db: Session):
    sales = db.query(Sale).all()
    turnover = sum(s.revenue for s in sales)
    margin = sum((s.revenue - s.cost) for s in sales)
    return {"turnover": turnover, "margin": margin}