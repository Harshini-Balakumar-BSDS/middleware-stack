
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
import uuid
import time

app = FastAPI()

# Change only these two values
EMAIL = "23f3002183@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-0x8nwl.example.com"

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Middleware ----------------
@app.middleware("http")
async def add_headers(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = str(process_time)

    return response

# ---------------- Endpoint ----------------
@app.get("/stats")
def stats(values: str = Query(...)):
    numbers = [int(x.strip()) for x in values.split(",")]

    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers)
    }
