import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes.documents import documents_router
from starlette.requests import Request
import uvicorn

# Increase multipart size limit
from starlette.formparsers import MultiPartParser
MultiPartParser.max_size = 21 * 1024 * 1024

app = FastAPI()

from fastapi import Request
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"[Validation Error] {exc.errors()}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

@app.exception_handler(413)
async def request_entity_too_large(request, exc):
    return JSONResponse(
        status_code=413,
        content={"detail": "File too large. Maximum size is 25MB."}
    )

from starlette.middleware import Middleware
from starlette.datastructures import UploadFile as StarletteUploadFile

app = FastAPI(
    max_request_body_size=20 * 1024 * 1024  # not a real param, ignore this line
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
        limit_concurrency=None,
        timeout_keep_alive=120,
    )
