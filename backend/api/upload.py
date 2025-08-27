from fastapi import APIRouter, UploadFile, Depends
import shutil, os
from db.session import get_db
from sqlalchemy.orm import Session
from utils.excel_loader import load_excel_to_db

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_excel(file: UploadFile, db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    load_excel_to_db(file_path, db)
    return {"status": "ok", "filename": file.filename}