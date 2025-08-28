from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import tempfile
import shutil
from db.session import get_db
from services.ingest import load_sales_from_excel  # luego aquí podrás meter CSV

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Guardar temporalmente el archivo
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # 🔹 Procesar según extensión
    if file.filename.endswith(".xlsx"):
        load_sales_from_excel(tmp_path, db)
    elif file.filename.endswith(".csv"):
        # luego implementamos load_sales_from_csv
        raise NotImplementedError("Soporte para CSV todavía no implementado")
    else:
        raise ValueError("Formato de archivo no soportado")

    return {"status": "ok", "message": "Datos cargados correctamente"}
