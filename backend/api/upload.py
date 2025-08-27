from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
import tempfile
import shutil
from db.session import get_db
from services.ingest import load_sales_from_excel

router = APIRouter()

@router.post("/excel")
async def upload_excel(file: UploadFile, db: Session = Depends(get_db)):
    # Guardar temporalmente el Excel
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # Procesar el Excel
    load_sales_from_excel(tmp_path, db)

    return {"status": "ok", "message": "Datos cargados correctamente"}
