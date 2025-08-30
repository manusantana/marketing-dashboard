from pydantic import BaseModel
from typing import List, Dict, Optional


class UploadResponse(BaseModel):
    status: str
    message: str
    rows: Optional[int] = None
    columns: Optional[List[str]] = None
    sample: Optional[List[Dict]] = None

    batch_id: Optional[int] = None
