import os, json, uuid

# for AI
import requests
from dotenv import load_dotenv
load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

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



# generatin gsummary with AI==========================================================================

def extract_text_from_file(file_path: str, file_type: str) -> str:
    file_type = file_type.lower()

    if file_type == "txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    elif file_type == "pdf":
        import fitz
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif file_type == "docx":
        from docx import Document as DocxDocument
        doc = DocxDocument(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_type}")


def generate_summary_with_ai(text: str, summary_type: str) -> str:
    max_chars = 6000 if summary_type == "concise" else 12000
    truncated_text = text[:max_chars]

    if not truncated_text.strip():
        raise HTTPException(status_code=400, detail="Document appears to be empty or unreadable")

    if summary_type == "concise":
        prompt = (
            "Create a concise, study-friendly summary of the following document.\n\n"
            "Requirements:\n"
            "- Length: 5–8 bullet points (NOT paragraphs)\n"
            "- Each bullet: 1 short sentence\n"
            "- Focus only on key concepts, definitions, and main ideas\n"
            "- Remove examples, explanations, and minor details\n"
            "- Use clear, simple language for quick revision\n\n"
            "Format:\n"
            "- Bullet points only\n\n"
            f"Document:\n{truncated_text}\n\nConcise Study Summary:"
        )
    else:
        prompt = (
            "Create a detailed, structured study summary of the following document.\n\n"
            "Requirements:\n"
            "- Length: at least 3–6 sections\n"
            "- Include headings and subheadings\n"
            "- Explain key concepts clearly (like study notes)\n"
            "- Include definitions, explanations, and important details\n"
            "- Keep all important arguments and conclusions\n"
            "- Use bullet points where helpful\n"
            "- Add short examples ONLY if they clarify concepts\n\n"
            "Format:\n"
            "1. Title (based on the topic)\n"
            "2. Sections with headings\n"
            "3. Bullet points + short paragraphs\n\n"
            "Goal: The summary should be usable for learning and exam preparation.\n\n"
            f"Document:\n{truncated_text}\n\nDetailed Study Summary:"
        )
    API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.3"
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {
        "inputs": f"<s>[INST] {prompt} [/INST]",
        "parameters": {
            "max_new_tokens": 500 if summary_type == "concise" else 1500,
            "temperature": 0.3,
            "return_full_text": False,
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        return fallback_summary(text, summary_type)

    result = response.json()
    if isinstance(result, list) and len(result) > 0:
        return result[0].get("generated_text", "").strip()

    return fallback_summary(text, summary_type)


def fallback_summary(text: str, summary_type: str) -> str:
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if len(s.strip()) > 20]
    count = 3 if summary_type == "concise" else 8
    return ". ".join(sentences[:count]) + "." if sentences else "Could not generate summary."

#=====================================================================================================


async def summarize_document_service(db: Session, doc_id: str, summary_type: str):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # actual summary instead of fake text
    text = extract_text_from_file(doc.filePath, doc.fileType)
    summary = generate_summary_with_ai(text, summary_type)

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
