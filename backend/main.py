import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.formparsers import MultiPartParser
from routes.documents import documents_router

# Increase multipart size limit to handle files up to 20MB
MultiPartParser.max_size = 21 * 1024 * 1024

app = FastAPI(
    title="AI Study Summarizer",
    description="Microservice for summarizing course documents using AI",
    version="1.0.0",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"[Validation Error] {exc.errors()}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.exception_handler(413)
async def request_entity_too_large(request: Request, exc):
    return JSONResponse(
        status_code=413,
        content={"detail": "File too large. Maximum size is 20MB."}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router, prefix="/api", tags=["documents"])

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        timeout_keep_alive=120,
    )