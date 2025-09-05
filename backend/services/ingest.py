# backend/services/ingest.py
import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session
from db.models import Sale


# ---------- helpers ----------
def _coerce_money(series: pd.Series) -> pd.Series:
    """Convierte '1.234,56 €' | '1,234.56' | '1234' a float."""
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce")
    s = series.astype(str)
    s = s.str.replace(r"[€$£]", "", regex=True).str.replace(r"\s+", "", regex=True)
    comma_decimal = s.str.contains(r",\d{1,2}$", na=False)
    s = s.where(
        ~comma_decimal,
        s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
    )
    s = s.where(comma_decimal, s.str.replace(",", "", regex=False))
    return pd.to_numeric(s, errors="coerce")


def _coerce_percent(series: pd.Series) -> pd.Series:
    """Convierte '12,5%' | '12.5%' | 0.125 | 12.5 a fracción 0..1."""
    if pd.api.types.is_numeric_dtype(series):
        s = pd.to_numeric(series, errors="coerce")
        # si parece 0..1 lo dejamos; si parece 0..100 lo pasamos a 0..1
        return s.where(s <= 1, s / 100.0)
    s = series.astype(str).str.strip()
    s = s.str.replace("%", "", regex=False)
    s = s.str.replace(r"\s+", "", regex=True)
    # normaliza coma decimal
    comma_decimal = s.str.contains(r",\d{1,2}$", na=False)
    s = s.where(
        ~comma_decimal,
        s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
    )
    s = s.where(comma_decimal, s.str.replace(",", "", regex=False))
    s = pd.to_numeric(s, errors="coerce")
    return s.where(s <= 1, s / 100.0)


def _join_cols(df: pd.DataFrame, cols: list[str], new_col: str):
    """Concatena columnas no vacías con ' | '."""
    existing = [c for c in cols if c in df.columns]
    if not existing:
        return

    def _row_join(row):
        vals = []
        for c in existing:
            v = row.get(c)
            if pd.notna(v) and str(v).strip():
                vals.append(str(v).strip())
        return " | ".join(vals) if vals else None

    df[new_col] = df.apply(_row_join, axis=1)


# ---------- normalización principal ----------
def _normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    # 1) columnas a minúsculas
    df = df.rename(columns=lambda c: str(c).strip().lower())

    # 2) mapping específico de tu Excel -> nombres "estándar internos"
    # (mantenemos columnas originales para construir compuestos)
    mapping = {
        "t.añomes": "date",
        "venta": "amount",
        "margen": "margin_raw",
        "dto. medio": "discount_raw",
        "cantidad": "quantity",
        # alias útiles si cambian encabezados
        "fecha": "date",
        "ventas": "amount",
        "dto medio": "discount_raw",
    }
    for src, dst in mapping.items():
        if src in df.columns:
            df = df.rename(columns={src: dst})

    # 3) componemos las claves de negocio (market, segment, customer, product)
    #    usando los nombres en minúsculas tal cual vienen del Excel
    _join_cols(df, ["c.mercado", "c.sociedad", "c.pais", "c.area"], "market")
    _join_cols(df, ["c.uen", "c.uen2", "c.segmento"], "segment")
    _join_cols(
        df, ["c.representante", "c.cliente", "c.conb2b", "c.tramoactual"], "customer"
    )
    _join_cols(
        df,
        ["a.familia", "a.subfamilia", "a.articulotipo1", "a.descripcion", "a.tipo"],
        "product",
    )

    # 4) tipos: fecha y métricas
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
        if use_pct:
            df["margin_eur"] = (df["amount"] * pct).fillna(0.0)
        else:
            df["margin_eur"] = eur.fillna(0.0)
    else:
        df["margin_eur"] = 0.0

    if "discount_raw" in df.columns:
        df["discount_pct"] = _coerce_percent(df["discount_raw"]).fillna(0.0)

    if "quantity" in df.columns:
        df["quantity"] = (
            pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
        )

    # 5) agrupación/deduplicado dentro del archivo
    group_keys = [
        c
        for c in ["date", "market", "segment", "customer", "product"]
        if c in df.columns
    ]
    agg = {}
    if "amount" in df.columns:
        agg["amount"] = "sum"
    if "margin_eur" in df.columns:
        agg["margin_eur"] = "sum"
    if "quantity" in df.columns:
        agg["quantity"] = "sum"

    # media ponderada de descuento por importe
    if "discount_pct" in df.columns and "amount" in df.columns:
        df["_disc_weight"] = df["discount_pct"] * df["amount"]
        agg["_disc_weight"] = "sum"
        agg["_amount_for_disc"] = (
            ("amount", "sum") if isinstance(agg["amount"], tuple) else "sum"
        )
        # truco: guardamos amount ya arriba; repetimos para denominador
        df["_amount_for_disc"] = df["amount"]

    if group_keys:
        df = df.groupby(group_keys, as_index=False).agg(agg)
        if "_disc_weight" in df.columns and "_amount_for_disc" in df.columns:
            denom = df["_amount_for_disc"].replace(0, pd.NA)
            df["discount_pct"] = (df["_disc_weight"] / denom).fillna(0.0)
            df = df.drop(columns=["_disc_weight", "_amount_for_disc"])

    return df


# ---------- inserción ----------
def _bulk_insert_sales(df: pd.DataFrame, db: Session, batch_id: str):
    """Inserta sin commit; el commit/rollback lo gestiona el endpoint (transacción)."""
    records: list[Sale] = []
    for _, r in df.iterrows():
        records.append(
            Sale(
                date=r.get("date"),
                customer=r.get("customer"),  # compuesto
                product=r.get("product"),  # compuesto
                amount=float(r.get("amount", 0) or 0),
                margin=float(r.get("margin_eur", 0) or 0),  # margen en €
                discount=float(r.get("discount_pct", 0) or 0),
                quantity=int(r.get("quantity", 0) or 0),
                batch_id=batch_id,
            )
        )
    if records:
        db.add_all(records)


# ---------- API para el endpoint ----------
def parse_sales_from_excel(path: Path) -> pd.DataFrame:
    """Parse an Excel file (``.xlsx``/``.xls``) into the normalized format.

    Pandas relies on different engines depending on the extension. Older
    ``.xls`` files require the ``xlrd`` package while modern ``.xlsx`` files use
    ``openpyxl``. Selecting the engine explicitly avoids pandas trying the wrong
    one and provides a clearer error message if the dependency is missing.
    """

    ext = path.suffix.lower()
    engine = "xlrd" if ext == ".xls" else "openpyxl"
    df = pd.read_excel(path, engine=engine)
    return _normalize_df(df)


def parse_sales_from_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return _normalize_df(df)


def bulk_insert_sales(df: pd.DataFrame, db: Session, batch_id: str):
    _bulk_insert_sales(df, db, batch_id=batch_id)  # sin commit
