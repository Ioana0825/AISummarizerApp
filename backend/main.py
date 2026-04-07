import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.documents import documents_router

app = FastAPI()
from fastapi.responses import JSONResponse

@app.exception_handler(413)
async def request_entity_too_large(request, exc):
    return JSONResponse(status_code=413, content={"detail": "File too large. Maximum size is 25MB."})

# Allow uploads up to 25MB
from starlette.middleware import Middleware
import starlette

@app.middleware("http")
async def increase_upload_size(request, call_next):
    return await call_next(request)

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
