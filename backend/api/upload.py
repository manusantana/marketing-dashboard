# backend/api/upload.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import tempfile, shutil
from pathlib import Path
from db.session import get_db
from services.ingest import load_sales_from_excel, load_sales_from_csv
from schemas.upload import UploadResponse

# ⬇️ Prefijo aquí, NO en main.py
router = APIRouter(prefix="/upload", tags=["Upload"])

ALLOWED_EXTS = {".xlsx", ".xls", ".csv"}
MAX_MB = 15  # límite opcional

@router.post("/", response_model=UploadResponse)
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
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

    try:
        if ext in {".xlsx", ".xls"}:
            df = load_sales_from_excel(tmp_path, db)
        else:  # ".csv"
            df = load_sales_from_csv(tmp_path, db)
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
