import os, json, uuid
# for AI
import requests
from services.rag import store_document_chunks, retrieve_best_chunks, retrieve_all_chunks_ordered
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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


def generate_summary_with_ai(text: str, summary_type: str, doc_id: str) -> str:
    if not text.strip():
        raise HTTPException(status_code=400, detail="Document appears to be empty or unreadable")

    # Step 1: Chunk and store in ChromaDB
    store_document_chunks(doc_id, text)

    # Step 2: Retrieve chunks
    if summary_type == "concise":
        chunks = retrieve_best_chunks(doc_id, "main ideas key concepts important points summary", n_results=8)
    else:
        chunks = retrieve_all_chunks_ordered(doc_id)

    if not chunks:
        return fallback_summary(text, summary_type)

    # Step 3: Build context from retrieved chunks
    combined_text = "\n\n---\n\n".join(chunks)
    max_chars = 8000 if summary_type == "concise" else 20000
    combined_text = combined_text[:max_chars]

    # Step 4: Generate summary with Ollama (local)
    if summary_type == "concise":
        prompt = (
            "Create a concise, study-friendly summary based on the following key sections from a document.\n\n"
            "Requirements:\n"
            "- Length: 5-8 bullet points\n"
            "- Each bullet: 1 short sentence\n"
            "- Focus only on key concepts, definitions, and main ideas\n"
            "- Use clear, simple language for quick revision\n"
            "- IMPORTANT: Write the summary in the SAME LANGUAGE as the document\n\n"
            f"Document sections:\n{combined_text}\n\nConcise Study Summary:"
        )
    else:
        prompt = (
            "Create a detailed, structured study summary based on the following sections from a document.\n\n"
            "Requirements:\n"
            "- Length: at least 3-6 sections\n"
            "- Include headings and subheadings\n"
            "- Explain key concepts clearly like study notes\n"
            "- Include definitions, explanations, and important details\n"
            "- Use bullet points where helpful\n"
            "- The summary should be usable for learning and exam preparation\n"
            "- IMPORTANT: Write the summary in the SAME LANGUAGE as the document\n\n"
            f"Document sections:\n{combined_text}\n\nDetailed Study Summary:"
        )

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.1:8b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 500 if summary_type == "concise" else 1500,
            }
        }, timeout=120)

        if response.status_code == 200:
            result = response.json()
            return result["response"].strip()
        else:
            print(f"Ollama error: {response.status_code} - {response.text}")
            return fallback_summary(text, summary_type)

    except Exception as e:
        print(f"Ollama exception: {e}")
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
    summary = generate_summary_with_ai(text, summary_type, doc_id)

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