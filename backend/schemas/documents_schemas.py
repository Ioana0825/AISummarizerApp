from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    fileType: str
    status: str
    fileSize: Optional[int] = None
    createdAt: datetime


class DocumentCreateResponse(BaseModel):
    id: str
    message: str


# Summarization

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
    summaryType: Optional[str] = None
    generatedAt: datetime


class SummaryRegenerateResponse(BaseModel):
    message: str
    documentId: str