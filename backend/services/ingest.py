import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session
from db.models import Sale  # ya lo usas en analytics


def _normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=lambda c: str(c).strip().lower())
    # Normaliza nombres esperados: date, customer, product, amount, margin, quantity
    mapping = {
        "fecha": "date",
        "cliente": "customer",
        "producto": "product",
        "importe": "amount",
        "margen": "margin",
        "cantidad": "quantity",
    }
    df = df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date

    if "amount" in df.columns:
        df["amount"] = _coerce_money(df["amount"]).fillna(0.0)

    # margen en €:
    # - si margin_raw parece porcentaje (contiene % o <= 1/<=100), calcula sobre amount
    # - si margin_raw parece monetario, úsalo
    if "margin_raw" in df.columns:
        pct = _coerce_percent(df["margin_raw"])
        eur = _coerce_money(df["margin_raw"])
        # heurística: si hay más valores válidos como % que como €, usamos %
        use_pct = pct.notna().sum() >= eur.notna().sum()
        df["margin_eur"] = (df["amount"] * pct).where(use_pct, eur).fillna(0.0)
    else:
        df["margin_eur"] = 0.0

    if "discount_raw" in df.columns:
        df["discount_pct"] = _coerce_percent(df["discount_raw"]).fillna(0.0)

    if "quantity" in df.columns:
        df["quantity"] = (
            pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
        )
    return df


def _bulk_upsert_sales(df: pd.DataFrame, db: Session, batch_id: int, mode: str = "add"):
    """Insert sales in bulk assigning them to a batch."""
    # Inserción simple (MVP). Si luego quieres upsert real, lo cambiamos.
    if mode == "replace":
        db.query(Sale).delete()
        db.commit()

    records = []
    for _, r in df.iterrows():
        s = Sale(
            date=r.get("date"),
            customer=r.get("customer"),
            product=r.get("product"),
            amount=float(r.get("amount", 0) or 0),
            margin=float(r.get("margin", 0) or 0),
            quantity=int(r.get("quantity", 0) or 0),
            batch_id=batch_id,
        )
        records.append(s)
    db.add_all(records)
    db.commit()


def load_sales_from_excel(path: Path, db: Session, batch_id: int, mode: str = "add"):
    df = pd.read_excel(path)
    df = _normalize_df(df)
    _bulk_upsert_sales(df, db, batch_id, mode)
    return df


def load_sales_from_csv(path: Path, db: Session, batch_id: int, mode: str = "add"):
    df = pd.read_csv(path)
    df = _normalize_df(df)
    _bulk_upsert_sales(df, db, batch_id, mode)
    return df
