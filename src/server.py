"""FastAPI app that keeps the RAG pipeline warm for low-latency usage."""

import os
import threading
import time
from collections import deque
from functools import lru_cache
from typing import Deque, Dict

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from main import create_pipeline
from src.rag_pipeline import RAGPipeline


class QueryRequest(BaseModel):
    prompt: str


class QueryResponse(BaseModel):
    content: str
    duration_seconds: float


class ErrorResponse(BaseModel):
    detail: str


def _build_pipeline() -> RAGPipeline:
    return create_pipeline()


@lru_cache(maxsize=1)
def get_pipeline() -> RAGPipeline:
    """Return a singleton pipeline instance."""
    return _build_pipeline()


app = FastAPI(title="Simple RAG Pipeline", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RateLimiter:
    """Simple in-memory sliding-window rate limiter."""

    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._events: Dict[str, Deque[float]] = {}
        self._lock = threading.Lock()

    def check(self, key: str) -> float:
        now = time.time()
        with self._lock:
            events = self._events.setdefault(key, deque())
            window_start = now - self.window_seconds
            while events and events[0] < window_start:
                events.popleft()

            if len(events) >= self.max_requests:
                return events[0] + self.window_seconds - now

            events.append(now)
        return 0.0


def _get_rate_limiter() -> RateLimiter:
    max_requests = int(os.environ.get("CHATBOT_RATE_LIMIT", "30"))
    window_seconds = int(os.environ.get("CHATBOT_RATE_WINDOW", "60"))
    return RateLimiter(max_requests=max_requests, window_seconds=window_seconds)


rate_limiter = _get_rate_limiter()


def enforce_rate_limit(request: Request) -> None:
    client_host = request.client.host if request.client else "anonymous"
    retry_after = rate_limiter.check(client_host)
    if retry_after > 0:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please retry later.",
            headers={"Retry-After": f"{max(1, int(retry_after))}"},
        )


@app.on_event("startup")
def _startup_event() -> None:
    # Warm the pipeline so the first request does not pay the cold start cost.
    get_pipeline()


@app.get("/health", response_model=QueryResponse)
def health_check() -> QueryResponse:
    start = time.perf_counter()
    return QueryResponse(content="ok", duration_seconds=time.perf_counter() - start)


@app.post("/query", response_model=QueryResponse, responses={500: {"model": ErrorResponse}})
def query(
    payload: QueryRequest,
    request: Request,
    _: None = Depends(enforce_rate_limit),
) -> QueryResponse:
    pipeline = get_pipeline()
    start = time.perf_counter()
    try:
        answer = pipeline.process_query(payload.prompt)
    except Exception as exc:  # pragma: no cover - surface error to caller
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    duration = time.perf_counter() - start
    return QueryResponse(content=answer, duration_seconds=duration)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
