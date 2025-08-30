 from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Request
 from sqlalchemy.orm import Session
 import tempfile, shutil
 from pathlib import Path
 from db.session import get_db
+from db.models import Batch, Sale
 from services.ingest import load_sales_from_excel, load_sales_from_csv
 from schemas.upload import UploadResponse
 
 # ⬇️ Prefijo aquí, NO en main.py
 router = APIRouter(prefix="/upload", tags=["Upload"])
 
 ALLOWED_EXTS = {".xlsx", ".xls", ".csv"}
 MAX_MB = 15  # límite opcional
 
 @router.post("/", response_model=UploadResponse)
 async def upload_file(
     request: Request,
     mode: str = "add",
     file: UploadFile = File(...),
     db: Session = Depends(get_db),
 ):
     if mode not in {"add", "replace"}:
         raise HTTPException(status_code=400, detail="Modo inválido")
     # 1) Validación de tamaño (si el header viene)
     cl = request.headers.get("content-length")
     if cl and int(cl) > MAX_MB * 1024 * 1024:
         raise HTTPException(status_code=413, detail=f"Archivo > {MAX_MB}MB")
 
     # 2) Validación de extensión
     ext = Path(file.filename).suffix.lower()
     if ext not in ALLOWED_EXTS:
         raise HTTPException(status_code=400, detail="Extensión no permitida")
 
     # 3) Guardar temporal y parsear
     with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
         shutil.copyfileobj(file.file, tmp)
         tmp_path = Path(tmp.name)
 
+    # 3b) Crear un nuevo batch
+    batch = Batch()
+    db.add(batch)
+    db.commit()
+    db.refresh(batch)
+
     try:
         if ext in {".xlsx", ".xls"}:
-            df = load_sales_from_excel(tmp_path, db, mode)
+            df = load_sales_from_excel(tmp_path, db, batch.id, mode)
         else:  # ".csv"
-            df = load_sales_from_csv(tmp_path, db, mode)
+            df = load_sales_from_csv(tmp_path, db, batch.id, mode)
     except Exception as e:
         raise HTTPException(status_code=400, detail=f"Error procesando archivo: {e}")
     finally:
         try:
             tmp_path.unlink(missing_ok=True)
         except:
             pass
 
     # 4) Respuesta tipada para la UI
     sample = df.head(5).to_dict(orient="records")
     return UploadResponse(
         status="ok",
         message="Datos cargados correctamente",
         rows=len(df),
         columns=list(df.columns),
         sample=sample,
     )
+
+
+@router.delete("/undo")
+def undo_last_upload(db: Session = Depends(get_db)):
+    batch = db.query(Batch).order_by(Batch.created_at.desc()).first()
+    if not batch:
+        raise HTTPException(status_code=404, detail="No hay batches previos para deshacer")
+
+    db.query(Sale).filter(Sale.batch_id == batch.id).delete()
+    db.delete(batch)
+    db.commit()
+
+    return {"status": "ok", "message": "Último batch eliminado"}
diff --git a/backend/db/models.py b/backend/db/models.py
index e436af7bc94d74137299acdc1110788c3db5f31a..940e15e27b55fa8c03d7a71699df901538347e19 100644
--- a/backend/db/models.py
+++ b/backend/db/models.py
@@ -1,13 +1,25 @@
-from sqlalchemy import Column, Integer, String, Date, Float
+from datetime import datetime
+from sqlalchemy import Column, Integer, String, Date, Float, DateTime, ForeignKey
+from sqlalchemy.orm import relationship
 from db.session import Base
 
+
+class Batch(Base):
+    __tablename__ = "batches"
+
+    id = Column(Integer, primary_key=True, index=True)
+    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
+    sales = relationship("Sale", back_populates="batch", cascade="all, delete-orphan")
+
 class Sale(Base):
     __tablename__ = "sales"
 
     id = Column(Integer, primary_key=True, index=True)
     date = Column(Date, index=True)          # T.AñoMes
     customer = Column(String, index=True)    # C.Cliente
     product = Column(String)                 # A.Descripcion
     amount = Column(Float)                   # Venta 💰
     margin = Column(Float)                   # Margen %
     quantity = Column(Integer)               # Cantidad
+    batch_id = Column(Integer, ForeignKey("batches.id"), index=True)
+    batch = relationship("Batch", back_populates="sales")
diff --git a/backend/migrations/versions/ee5df5cfa1d2_add_batches.py b/backend/migrations/versions/ee5df5cfa1d2_add_batches.py
new file mode 100644
index 0000000000000000000000000000000000000000..cb866fe026b034df0689f04f3b1336fdcc96096e
--- /dev/null
+++ b/backend/migrations/versions/ee5df5cfa1d2_add_batches.py
@@ -0,0 +1,41 @@
+"""add batches table and batch_id to sales
+
+Revision ID: ee5df5cfa1d2
+Revises: cdb7a72fc2d2
+Create Date: 2025-10-20 00:00:00.000000
+
+"""
+from typing import Sequence, Union
+
+from alembic import op
+import sqlalchemy as sa
+
+
+# revision identifiers, used by Alembic.
+revision: str = 'ee5df5cfa1d2'
+down_revision: Union[str, Sequence[str], None] = 'cdb7a72fc2d2'
+branch_labels: Union[str, Sequence[str], None] = None
+depends_on: Union[str, Sequence[str], None] = None
+
+
+def upgrade() -> None:
+    """Upgrade schema."""
+    op.create_table(
+        'batches',
+        sa.Column('id', sa.Integer(), nullable=False),
+        sa.Column('created_at', sa.DateTime(), nullable=False),
+        sa.PrimaryKeyConstraint('id')
+    )
+    op.create_index(op.f('ix_batches_id'), 'batches', ['id'], unique=False)
+    op.add_column('sales', sa.Column('batch_id', sa.Integer(), nullable=True))
+    op.create_index(op.f('ix_sales_batch_id'), 'sales', ['batch_id'], unique=False)
+    op.create_foreign_key(None, 'sales', 'batches', ['batch_id'], ['id'], ondelete='CASCADE')
+
+
+def downgrade() -> None:
+    """Downgrade schema."""
+    op.drop_constraint(None, 'sales', type_='foreignkey')
+    op.drop_index(op.f('ix_sales_batch_id'), table_name='sales')
+    op.drop_column('sales', 'batch_id')
+    op.drop_index(op.f('ix_batches_id'), table_name='batches')
+    op.drop_table('batches')
diff --git a/backend/services/ingest.py b/backend/services/ingest.py
index 244e80b74c0fd6acbeaa0db5d646b5cd5cdb084b..6ba3abb9ff6aa20e9edf8726e6d66872bc8cddb9 100644
--- a/backend/services/ingest.py
+++ b/backend/services/ingest.py
@@ -1,54 +1,64 @@
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
 
-def _bulk_upsert_sales(df: pd.DataFrame, db: Session, mode: str = "add"):
+def _bulk_upsert_sales(
+    df: pd.DataFrame, db: Session, batch_id: int, mode: str = "add"
+):
+    """Insert sales in bulk assigning them to a batch."""
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
+            batch_id=batch_id,
         )
         records.append(s)
     db.add_all(records)
     db.commit()
 
-def load_sales_from_excel(path: Path, db: Session, mode: str = "add"):
+
+def load_sales_from_excel(
+    path: Path, db: Session, batch_id: int, mode: str = "add"
+):
     df = pd.read_excel(path)
     df = _normalize_df(df)
-    _bulk_upsert_sales(df, db, mode)
+    _bulk_upsert_sales(df, db, batch_id, mode)
     return df
 
-def load_sales_from_csv(path: Path, db: Session, mode: str = "add"):
+
+def load_sales_from_csv(
+    path: Path, db: Session, batch_id: int, mode: str = "add"
+):
     df = pd.read_csv(path)
     df = _normalize_df(df)
-    _bulk_upsert_sales(df, db, mode)
+    _bulk_upsert_sales(df, db, batch_id, mode)
     return df
