import pandas as pd
from sqlalchemy.orm import Session
from db.models import Sale

def load_sales_from_excel(file_path: str, db: Session):
    try:
        df = pd.read_excel(file_path)
        print("📥 Excel cargado con columnas:", df.columns.tolist())

        # Mapeo Excel → DB
        df = df.rename(columns={
            "T.AñoMes": "date",
            "C.Cliente": "customer",
            "A.Descripcion": "product",
            "Venta": "amount",
            "Margen": "margin",
            "Cantidad": "quantity"
        })

        # ⚠️ Filtrar solo columnas que nos interesan (las que existan)
        expected_cols = ["date", "customer", "product", "amount", "margin", "quantity"]
        available_cols = [c for c in expected_cols if c in df.columns]
        df = df[available_cols]

        print("✅ Columnas finales utilizadas:", df.columns.tolist())
        print("🔎 Primeras filas:", df.head().to_dict(orient="records"))

        # Insertar fila a fila
        for _, row in df.iterrows():
            sale = Sale(
                date=pd.to_datetime(row.get("date")).date() if pd.notna(row.get("date")) else None,
                customer=str(row.get("customer", "")),
                product=str(row.get("product", "")),
                amount=float(row.get("amount", 0) or 0),
                margin=float(row.get("margin", 0) or 0),
                quantity=int(row.get("quantity", 0) or 0),
            )
            db.add(sale)

        db.commit()
        print("🎉 Datos cargados correctamente")

    except Exception as e:
        print(f"❌ Error procesando Excel: {e}")
        raise
