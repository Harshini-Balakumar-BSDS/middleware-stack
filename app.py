from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import time
from collections import defaultdict

app = FastAPI()

# ==========================================================
# CORS
# ==========================================================

from fastapi.middleware.cors import CORSMiddleware

ALLOWED_ORIGINS = [
    "https://app-4sakdd.example.com",
    "https://exam.sanand.workers.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],   # <-- add this too
)

# ==========================================================
# Rate Limiter
# ==========================================================

RATE_LIMIT = 10
WINDOW = 10

client_requests = defaultdict(list)

# ==========================================================
# Request Context Middleware
# ==========================================================

@app.middleware("http")
async def request_context(request: Request, call_next):

    request_id = request.headers.get("X-Request-ID")

    if request_id is None:
        request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    return response

# ==========================================================
# Rate Limiter Middleware
# ==========================================================

@app.middleware("http")
async def rate_limiter(request: Request, call_next):

    client_id = request.headers.get("X-Client-Id", "anonymous")

    now = time.time()

    timestamps = client_requests[client_id]

    timestamps[:] = [
        t for t in timestamps
        if now - t < WINDOW
    ]

    if len(timestamps) >= RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"}
        )

    timestamps.append(now)

    response = await call_next(request)

    return response

# ==========================================================
# Endpoint
# ==========================================================

@app.get("/ping")
async def ping(request: Request):
    return {
        "email": "23f3002183@ds.study.iitm.ac.in",
        "request_id": request.state.request_id
    }
