"""Schemas for upload endpoints."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class UploadResponse(BaseModel):
    """Response returned after a successful upload."""

    status: str
    message: str
    rows: Optional[int] = None
    columns: Optional[List[str]] = None
    sample: Optional[List[Dict[str, Any]]] = None
    batch_id: Optional[str] = None


class UploadHistoryItem(BaseModel):
    """Single upload history record."""

    batch_id: str
    filename: str
    mode: str
    rows: int
    created_at: datetime
