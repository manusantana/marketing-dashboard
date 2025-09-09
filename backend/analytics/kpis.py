"""Analytics helpers for KPI calculations."""

from datetime import date, timedelta
from typing import Any, Dict, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from db.models import Sale
from services.google_analytics import fetch_orders_and_revenue as ga_fetch
from services.shopify import fetch_orders_and_revenue as shopify_fetch


def get_basic_kpis(db: Session) -> Dict[str, float]:
    """Compute core KPI values combining local sales and external sources."""
    sales = db.query(Sale).all()
    turnover_local = sum(s.amount for s in sales)
    margin = sum(s.margin for s in sales)
    discount = sum(s.amount * s.discount for s in sales)
    orders_local = len(sales)

    end = date.today()
    start = end - timedelta(days=30)
    ga_orders, ga_turnover = ga_fetch(start.isoformat(), end.isoformat())
    sh_orders, sh_turnover = shopify_fetch(start.isoformat(), end.isoformat())

    turnover = turnover_local + ga_turnover + sh_turnover
    orders = orders_local + ga_orders + sh_orders
    ticket_average = turnover / orders if orders else 0.0

    return {
        "turnover": float(turnover),
        "orders": int(orders),
        "ticket_average": float(ticket_average),
        "margin": float(margin),
        "discount": float(discount),
    }


def abc_by(db: Session, field: str) -> Dict[str, List[Dict[str, Any]]]:
    """Return ABC classification for the given Sale field."""
    column = getattr(Sale, field)
    rows = db.query(column, func.sum(Sale.amount).label("total")).group_by(column).all()
    rows = sorted(rows, key=lambda r: r[1], reverse=True)
    total = sum(r[1] for r in rows) or 1
    cumulative = 0
    result = {"A": [], "B": [], "C": []}

    for name, value in rows:
        cumulative += value
        ratio = cumulative / total
        entry = {"name": name, "value": float(value), "ratio": ratio}
        if ratio <= 0.8:
            result["A"].append(entry)
        elif ratio <= 0.95:
            result["B"].append(entry)
        else:
            result["C"].append(entry)

    return result
