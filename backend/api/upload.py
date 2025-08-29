# backend/api/upload.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import tempfile, shutil
from pathlib import Path
from typing import Literal
import uuid

from db.session import get_db
from db.models import Sale, UploadHistory
from services.ingest import (
    parse_sales_from_excel, parse_sales_from_csv, bulk_insert_sales
)
from schemas.upload import UploadResponse

router = APIRouter(prefix="/upload", tags=["Upload"])

ALLOWED_EXTS = {".xlsx", ".xls", ".csv"}
MAX_MB = 15

@router.post("/", response_model=UploadResponse)
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    mode: Literal["append", "replace"] = "append",
    db: Session = Depends(get_db),
):
    # --- Validaciones básicas ---
    cl = request.headers.get("content-length")
    if cl and int(cl) > MAX_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"Archivo > {MAX_MB}MB")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTS:
        raise HTTPException(status_code=400, detail="Extensión no permitida")

    # --- Persistencia temporal ---
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = Path(tmp.name)

    try:
        # ========= PARSEO (termina aquí) =========
        if ext in {".xlsx", ".xls"}:
            df = parse_sales_from_excel(tmp_path)
        else:
            df = parse_sales_from_csv(tmp_path)
        # ========= FIN PARSEO =========
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error procesando archivo: {e}")
    finally:
        try: tmp_path.unlink(missing_ok=True)
        except: pass

    # --- Transacción atómica (empieza aquí) ---
    batch_id = str(uuid.uuid4())
    try:
        with db.begin():
            if mode == "replace":
                db.query(Sale).delete()
            bulk_insert_sales(df, db, batch_id=batch_id)  # sin commit interno
            db.add(UploadHistory(
                batch_id=batch_id,
                filename=file.filename,
                mode=mode,
                rows=len(df),
            ))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ingest fallido ({mode}): {e}")
    # --- Fin Transacción ---

    # --- Respuesta UI ---
    sample = df.head(5).to_dict(orient="records")
    action = "reemplazo" if mode == "replace" else "append"
    return UploadResponse(
        status="ok",
        message=f"Datos cargados correctamente ({action}).",
        rows=len(df),
        columns=list(df.columns),
        sample=sample,
        batch_id=batch_id,
    )
