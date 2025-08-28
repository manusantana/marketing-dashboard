import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session
from db.models import Sale  # ya lo usas en analytics
from datetime import datetime

def _normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=lambda c: str(c).strip().lower())
    # Normaliza nombres esperados: date, customer, product, amount, margin, quantity
    mapping = {
        "fecha": "date", "cliente": "customer", "producto": "product",
        "importe": "amount", "margen": "margin", "cantidad": "quantity",
    }
    df = df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    for col in ("amount", "margin"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    return df

def _bulk_upsert_sales(df: pd.DataFrame, db: Session):
    # Inserción simple (MVP). Si luego quieres upsert real, lo cambiamos.
    records = []
    for _, r in df.iterrows():
        s = Sale(
            date=r.get("date"),
            customer=r.get("customer"),
            product=r.get("product"),
            amount=float(r.get("amount", 0) or 0),
            margin=float(r.get("margin", 0) or 0),
            quantity=int(r.get("quantity", 0) or 0),
        )
        records.append(s)
    db.add_all(records)
    db.commit()

def load_sales_from_excel(path: Path, db: Session):
    df = pd.read_excel(path)
    df = _normalize_df(df)
    _bulk_upsert_sales(df, db)
    return df

def load_sales_from_csv(path: Path, db: Session):
    df = pd.read_csv(path)
    df = _normalize_df(df)
    _bulk_upsert_sales(df, db)
    return df
