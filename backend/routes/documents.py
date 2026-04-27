import os
import re
import json
from datetime import datetime, timezone

from fastapi import APIRouter, Form, UploadFile, File, Depends, Body, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from schemas.documents_schemas import (
    DocumentResponse, DocumentCreateResponse,
    SummaryRequest, SummaryStartResponse, SummaryResponse, SummaryRegenerateResponse,
)
from services.documents import (
    get_documents, get_document_by_id, upload_document_service,
    delete_document_service,
    summarize_document_service, get_summary_service, regenerate_summary_service,
    extract_text_from_file, stream_summary_tokens, _clean_ai_output,
)
from db.session import get_db
from db.models import Document
from db.mongo import summaries_collection

documents_router = APIRouter(prefix="/documents")


# --- Document CRUD ---

@documents_router.get("", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return get_documents(db)


@documents_router.get("/{id}", response_model=DocumentResponse)
def get_documents_by_id(id: str, db: Session = Depends(get_db)):
    return get_document_by_id(db, id)


@documents_router.post("", response_model=DocumentCreateResponse)
async def upload_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    fileType: str = Form(...),
    db: Session = Depends(get_db),
):
    return await upload_document_service(file, title, fileType, db)


@documents_router.get("/{id}/file")
def download_document(id: str, db: Session = Depends(get_db)):
    doc = get_document_by_id(db, id)

    if not os.path.exists(doc.filePath):
        raise HTTPException(status_code=404, detail="File not found on disk")

    content_type = {
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "txt": "text/plain",
    }.get(doc.fileType.lower(), "application/octet-stream")

    headers = {
        "Content-Disposition": f'attachment; filename="{doc.title}.{doc.fileType.lower()}"',
        "Content-Type": content_type,
    }
    return FileResponse(path=doc.filePath, headers=headers)


@documents_router.delete("/{id}")
def delete_document(id: str, db: Session = Depends(get_db)):
    return delete_document_service(db, id)


# --- Summarization (original non-streaming) ---

@documents_router.post("/{id}/summarize", response_model=SummaryStartResponse)
async def summarize_document(
    id: str,
    payload: SummaryRequest = Body(...),
    db: Session = Depends(get_db),
):
    return await summarize_document_service(db, id, payload.summaryType.value)


@documents_router.get("/{id}/summary", response_model=SummaryResponse)
async def get_summary(
    id: str,
    type: str = Query(default="concise", regex="^(concise|detailed)$"),
    db: Session = Depends(get_db),
):
    summary = await get_summary_service(db, id, type)
    if isinstance(summary["generatedAt"], str):
        summary["generatedAt"] = datetime.fromisoformat(summary["generatedAt"])
    return summary


@documents_router.patch("/{id}/summary", response_model=SummaryRegenerateResponse)
async def regenerate_summary(
    id: str,
    payload: SummaryRequest = Body(...),
    db: Session = Depends(get_db),
):
    return await regenerate_summary_service(db, id, payload.summaryType.value)


# --- Streaming summarization ---

@documents_router.post("/{id}/summarize-stream")
async def summarize_stream(
    id: str,
    payload: SummaryRequest = Body(...),
    db: Session = Depends(get_db),
):
    doc = db.query(Document).filter(Document.id == id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    text = extract_text_from_file(doc.filePath, doc.fileType)
    summary_type = payload.summaryType.value
    doc_id = doc.id

    sync_collection = summaries_collection.delegate

    def event_stream():
        collected_tokens = []

        for token in stream_summary_tokens(text, summary_type):
            collected_tokens.append(token)
            yield f"data: {json.dumps({'token': token})}\n\n"

        # Strip warning before saving
        raw = "".join(collected_tokens)
        raw = re.sub(r"^⚠️[^\n]+\n\n?", "", raw)
        full_summary = _clean_ai_output(raw)

        # Save per-type: store concise and detailed separately in the same doc
        sync_collection.update_one(
            {"documentId": doc_id},
            {
                "$set": {
                    "documentId": doc_id,
                    f"summaries.{summary_type}": {
                        "summary": full_summary,
                        "generatedAt": datetime.now(timezone.utc),
                    },
                }
            },
            upsert=True,
        )

        db.query(Document).filter(Document.id == doc_id).update({"status": "summarized"})
        db.commit()

        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )