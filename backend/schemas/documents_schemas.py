from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    fileType: str
    status: str
    createdAt: datetime
    #summary: Optional[str] = None
    #summaryType: Optional[str] = None
    #summaryGeneratedAt: Optional[datetime] = None

class DocumentCreateResponse(BaseModel):
    id: str
    message: str

class DocumentCreate(BaseModel):
    id: str
    title: str
    fileType: str
    filePath: str
    status: str

# summarizing
from enum import Enum

class SummaryType(str, Enum):
    concise = "concise"
    detailed = "detailed"

class SummaryRequest(BaseModel):
    summaryType: SummaryType

class SummaryStartResponse(BaseModel):
    message: str
    documentId: str

class SummaryResponse(BaseModel):
    documentId: str
    title: str
    summary: str
    generatedAt: datetime

class SummaryRegenerateResponse(BaseModel):
    message: str
