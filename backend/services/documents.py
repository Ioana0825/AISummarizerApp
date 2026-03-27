import os, json, uuid

# no new service function needed

from fastapi.responses import FileResponse
from fastapi import HTTPException
from datetime import datetime

from schemas.documents_schemas import DocumentResponse, DocumentCreateResponse, DocumentCreate

from sqlalchemy.orm import Session
from db.models import Document

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

type_mapping = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "txt": "text/plain"
}

def get_documents(db: Session):
    return db.query(Document).all()

def get_document_by_id(db: Session, doc_id: str):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


async def upload_document_service(file, title, fileType, db: Session):
    import re
    import os
    import uuid
    from fastapi import HTTPException
    from db.models import Document

    # Validate file extension
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=422, detail="File extension not allowed")

    # Generate UUID for document
    doc_id = str(uuid.uuid4())

    # Sanitize filename
    safe_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', file.filename)
    file_name = f"{doc_id}_{safe_filename}"
    full_path = os.path.join(UPLOAD_DIR, file_name)

    # Save file to disk
    content = await file.read()
    with open(full_path, "wb") as f_disk:
        f_disk.write(content)

    # Create DB record
    new_doc = Document(
        id=doc_id,
        title=title,
        fileType=file_extension,
        filePath=full_path,
        status="pending",
        #summary=None,
        #summaryType=None,
        #summaryGeneratedAt=None
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    from schemas.documents_schemas import DocumentCreateResponse
    return DocumentCreateResponse(
        id=doc_id,
        message="Document uploaded successfully"
    )


def delete_document_service(db: Session, doc_id: str):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if doc.filePath and os.path.exists(doc.filePath):
        try:
            os.remove(doc.filePath)
        except Exception:
            raise HTTPException(status_code=500, detail="Could not delete file")

    db.delete(doc)
    db.commit()
    return {"message": "Document deleted successfully"}



# summarizing

def generate_summary_from_text(text: str, summary_type: str) -> str:
    sentences = text.split(".")
    if summary_type == "concise":
        return ".".join(sentences[:2]).strip() + "."
    elif summary_type == "detailed":
        return ".".join(sentences[:5]).strip() + "."
    else:
        raise HTTPException(status_code=400, detail="Invalid summary type")


async def summarize_document_service(db: Session, doc_id: str, summary_type: str):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    fake_text = f"This is the content of document {doc.title}. It contains information about AI and machine learning. It explains concepts clearly. It provides examples. It concludes with future trends."
    summary = generate_summary_from_text(fake_text, summary_type)

    from db.mongo import summaries_collection

    await summaries_collection.update_one(
        {"documentId": doc.id},
        {
            "$set": {
                "documentId": doc.id,
                "summary": summary,
                "summaryType": summary_type,
                "generatedAt": datetime.utcnow()
            }
        },
        upsert=True
    )

    # ✅ update SQL status so the UI can show summarized
    doc.status = "summarized"
    db.commit()

    return {"message": "Summarization started", "documentId": doc.id}


async def get_summary_service(db, doc_id: str):
    from db.mongo import summaries_collection
    result = await summaries_collection.find_one({"documentId": doc_id})
    if not result:
        raise HTTPException(status_code=404, detail="Summary not found")

    return {
        "documentId": result["documentId"],
        "title": get_document_by_id(db, doc_id).title,
        "summary": result["summary"],
        "generatedAt": result["generatedAt"]
    }



async def regenerate_summary_service(db, doc_id: str, summary_type: str):
    return await summarize_document_service(db, doc_id, summary_type)
