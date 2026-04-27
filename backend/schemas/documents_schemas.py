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
    fileSize: Optional[int] = None  # file size in bytes
    createdAt: datetime


class DocumentCreateResponse(BaseModel):
    id: str
    message: str


class DocumentCreate(BaseModel):
    id: str
    title: str
    fileType: str
    filePath: str
    status: str


# Summarization

class SummaryType(str, Enum):
    concise = "concise"
    detailed = "detailed"


class SummaryRequest(BaseModel):
    summaryType: SummaryType


class SummaryStartResponse(BaseModel):
    message: str
    documentId: str
    estimatedSeconds: Optional[int] = None


class SummaryResponse(BaseModel):
    documentId: str
    title: str
    summary: str
    summaryType: Optional[str] = None
    generatedAt: datetime


class SummaryRegenerateResponse(BaseModel):
    message: str
    documentId: str
    estimatedSeconds: Optional[int] = None