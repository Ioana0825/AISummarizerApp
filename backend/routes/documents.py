import os

from fastapi import APIRouter, Form, UploadFile, File, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from starlette.responses import FileResponse

from schemas.documents_schemas import (
    DocumentResponse, DocumentCreateResponse,
    SummaryRequest, SummaryStartResponse, SummaryResponse, SummaryRegenerateResponse
)
from services.documents import (
    get_documents, get_document_by_id, upload_document_service,
    delete_document_service,
    summarize_document_service, get_summary_service, regenerate_summary_service
)
from db.session import get_db

documents_router = APIRouter(prefix="/documents")


# ------------------------------
# Document CRUD
# ------------------------------

@documents_router.get("", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return get_documents(db)


@documents_router.get("/{id}", response_model=DocumentResponse)
def get_documents_by_id(id: str, db: Session = Depends(get_db)):
    return get_document_by_id(db, id)


@documents_router.post("", response_model=DocumentCreateResponse)
async def upload_document(
    title: str = Form(...),
    file: UploadFile = File(..., max_size=25 * 1024 * 1024),
    fileType: str = Form(...),
    db: Session = Depends(get_db)
):
    # upload_document_service is async because reading file is async
    return await upload_document_service(file, title, fileType, db)

@documents_router.get("/{id}/file")
def download_document(id: str, db: Session = Depends(get_db)):
    """
    Download the actual file for a document.
    """
    doc = get_document_by_id(db, id)  # fetch from DB

    # Validate that file exists
    if not os.path.exists(doc.filePath):
        raise HTTPException(status_code=404, detail="File not found on disk")

    # Determine content type
    file_extension = doc.fileType.lower()
    content_type = {
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "txt": "text/plain"
    }.get(file_extension, "application/octet-stream")

    headers = {
        "Content-Disposition": f'attachment; filename="{doc.title}.{file_extension}"',
        "Content-Type": content_type
    }

    return FileResponse(path=doc.filePath, headers=headers)

# not required
@documents_router.get("/{id}/download")
def download_document_alias(id: str, db: Session = Depends(get_db)):
    return download_document(id, db)
#

@documents_router.delete("/{id}")
def delete_document(id: str, db: Session = Depends(get_db)):
    return delete_document_service(db, id)


# ------------------------------
# Summarization
# ------------------------------

@documents_router.post("/{id}/summarize", response_model=SummaryStartResponse)
async def summarize_document(
    id: str,
    payload: SummaryRequest = Body(...),
    db: Session = Depends(get_db)
):
    return await summarize_document_service(db, id, payload.summaryType.value)


@documents_router.get("/{id}/summary", response_model=SummaryResponse)
async def get_summary(id: str, db: Session = Depends(get_db)):
    summary = await get_summary_service(db, id)
    # Ensure generatedAt is datetime
    if isinstance(summary["generatedAt"], str):
        summary["generatedAt"] = datetime.fromisoformat(summary["generatedAt"])
    return summary


@documents_router.patch("/{id}/summary", response_model=SummaryRegenerateResponse)
async def regenerate_summary(
    id: str,
    payload: SummaryRequest = Body(...),
    db: Session = Depends(get_db)
):
    return await regenerate_summary_service(db, id, payload.summaryType.value)
